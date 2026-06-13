# ============================================================
# watchdog.py — Gmail fetch + analyze + action engine
# Scans ALL folders (inbox, spam, promotions, etc.)
# ============================================================

import pickle
import sqlite3
import datetime
import json
import os
import base64
import re
from googleapiclient.discovery import build
from analyzer_engine import analyze_headers, parse_raw_headers

DB_PATH = "watchdog.db"
TOKEN_PATH = "token.pickle"

HEADER_NAMES = [
    'From', 'To', 'Reply-To', 'Reply-to', 'Subject', 'Date',
    'Received', 'Received-SPF', 'Authentication-Results',
    'ARC-Authentication-Results', 'DKIM-Signature',
    'Return-Path', 'Message-ID', 'X-Mailer', 'X-Original-From',
    'X-Google-DKIM-Signature', 'X-Forwarded-To', 'Delivered-To'
]

def get_gmail_service():
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError("token.pickle not found. Run gmail_auth.py first.")
    with open(TOKEN_PATH, 'rb') as f:
        creds = pickle.load(f)
    return build('gmail', 'v1', credentials=creds)

def is_already_scanned(message_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM scanned_emails WHERE message_id=?", (message_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def save_result(message_id, sender, subject, received_at, result, action_taken, raw_headers_text=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT OR IGNORE INTO scanned_emails
            (message_id, sender, subject, received_at, scanned_at,
             risk_score, verdict, flags, action_taken, raw_headers)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            message_id,
            sender[:500] if sender else "",
            subject[:500] if subject else "",
            received_at,
            datetime.datetime.now().isoformat(),
            result['score'],
            result['verdict'],
            json.dumps(result['flags']),
            action_taken,
            raw_headers_text[:5000]
        ))
        conn.commit()
    except Exception as e:
        print(f"    [!] DB save error: {e}")
    finally:
        conn.close()

def move_to_spam(service, message_id: str) -> bool:
    """Move a message to spam — removes ALL inbox/category labels, adds SPAM."""
    try:
        # Get current labels on this message
        msg = service.users().messages().get(
            userId='me', id=message_id, format='minimal'
        ).execute()
        current_labels = msg.get('labelIds', [])
        print(f"         Current labels: {current_labels}")

        # Remove every non-spam label so Gmail moves it out of inbox
        labels_to_remove = [l for l in current_labels if l in [
            'INBOX', 'UNREAD',
            'CATEGORY_PROMOTIONS', 'CATEGORY_SOCIAL',
            'CATEGORY_UPDATES', 'CATEGORY_FORUMS', 'CATEGORY_PERSONAL',
            'IMPORTANT', 'STARRED'
        ]]

        modify_body = {'addLabelIds': ['SPAM']}
        if labels_to_remove:
            modify_body['removeLabelIds'] = labels_to_remove

        service.users().messages().modify(
            userId='me',
            id=message_id,
            body=modify_body
        ).execute()
        print(f"         ✓ Moved to SPAM successfully (removed: {labels_to_remove})")
        return True
    except Exception as e:
        print(f"    [!] Could not move to spam: {e}")
        import traceback; traceback.print_exc()
        return False

def flag_message(service, message_id: str):
    """Add a STARRED label to flagged medium-risk emails."""
    try:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'addLabelIds': ['STARRED']}
        ).execute()
    except Exception:
        pass

def headers_to_text(headers_list: list) -> str:
    """Convert list of {name, value} dicts to raw header text."""
    lines = []
    for h in headers_list:
        lines.append(f"{h['name']}: {h['value']}")
    return "\n".join(lines)

def scan_inbox() -> list:
    """
    Scan ALL mail (inbox + spam + all folders) from last 3 days.
    Returns list of analysis result dicts.
    """
    print(f"\n[*] Scan started: {datetime.datetime.now().strftime('%H:%M:%S')}")
    results = []

    try:
        service = get_gmail_service()
    except Exception as e:
        print(f"[!] Gmail auth error: {e}")
        return results

    try:
        # Scan ALL mail — no labelIds filter, covers inbox, spam, promotions, all
        response = service.users().messages().list(
            userId='me',
            q='newer_than:3d',   # Last 3 days, all folders
            maxResults=50
        ).execute()

        messages = response.get('messages', [])
        print(f"[*] Found {len(messages)} messages to check")

        for msg_ref in messages:
            msg_id = msg_ref['id']

            if is_already_scanned(msg_id):
                continue

            try:
                # Fetch metadata headers
                full_msg = service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='metadata',
                    metadataHeaders=HEADER_NAMES
                ).execute()

                headers_list = full_msg.get('payload', {}).get('headers', [])
                headers_dict = {h['name']: h['value'] for h in headers_list}
                raw_headers_text = headers_to_text(headers_list)

                # Extract key fields
                sender  = headers_dict.get('From', headers_dict.get('from', ''))
                subject = headers_dict.get('Subject', headers_dict.get('subject', ''))
                date    = headers_dict.get('Date', headers_dict.get('date', ''))

                print(f"  → Analyzing: {subject[:60]!r} from {sender[:50]!r}")

                # Run analysis
                result = analyze_headers(headers_dict)
                result['sender']  = sender
                result['subject'] = subject
                result['message_id'] = msg_id

                action_taken = 'clean'

                if result['verdict'] == 'HIGH RISK':
                    moved = move_to_spam(service, msg_id)
                    action_taken = 'moved_to_spam' if moved else 'high_risk_unmoved'
                    print(f"     Score: {result['score']} → HIGH RISK — {'MOVED TO SPAM ✓' if moved else 'move FAILED'}")
                elif result['verdict'] == 'MEDIUM RISK':
                    flag_message(service, msg_id)
                    action_taken = 'starred_warning'
                    print(f"     Score: {result['score']} → MEDIUM RISK — starred")
                else:
                    print(f"     Score: {result['score']} → clean")

                save_result(msg_id, sender, subject, date, result, action_taken, raw_headers_text)
                result['action_taken'] = action_taken
                results.append(result)

            except Exception as e:
                print(f"    [!] Error on message {msg_id}: {e}")
                continue

    except Exception as e:
        print(f"[!] Gmail list error: {e}")

    print(f"[*] Scan complete — {len(results)} new emails processed\n")
    return results
