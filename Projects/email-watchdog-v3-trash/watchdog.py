# ============================================================
# watchdog.py — Gmail fetch + analyze + action engine
# Actions: HIGH RISK → Trash | MEDIUM RISK → Starred
# After each scan: sends a summary notification email to user
# ============================================================

import pickle
import sqlite3
import datetime
import json
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from analyzer_engine import analyze_headers

DB_PATH    = "watchdog.db"
TOKEN_PATH = "token.pickle"

HEADER_NAMES = [
    'From', 'To', 'Reply-To', 'Reply-to', 'Subject', 'Date',
    'Received', 'Received-SPF', 'Authentication-Results',
    'ARC-Authentication-Results', 'DKIM-Signature',
    'Return-Path', 'Message-ID', 'X-Mailer', 'X-Original-From',
    'X-Google-DKIM-Signature', 'X-Forwarded-To', 'Delivered-To'
]

# ── Gmail service ─────────────────────────────────────────
def get_gmail_service():
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError("token.pickle not found. Run gmail_auth.py first.")
    with open(TOKEN_PATH, 'rb') as f:
        creds = pickle.load(f)
    return build('gmail', 'v1', credentials=creds)

def get_user_email(service) -> str:
    try:
        profile = service.users().getProfile(userId='me').execute()
        return profile.get('emailAddress', '')
    except Exception:
        return ''

# ── Database ──────────────────────────────────────────────
def is_already_scanned(message_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM scanned_emails WHERE message_id=?", (message_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def save_result(message_id, sender, subject, received_at,
                result, action_taken, raw_headers_text=""):
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
            (sender or "")[:500],
            (subject or "")[:500],
            received_at,
            datetime.datetime.now().isoformat(),
            result['score'],
            result['verdict'],
            json.dumps(result['flags']),
            action_taken,
            (raw_headers_text or "")[:5000]
        ))
        conn.commit()
    except Exception as e:
        print(f"    [!] DB save error: {e}")
    finally:
        conn.close()

def headers_to_text(headers_list: list) -> str:
    return "\n".join(f"{h['name']}: {h['value']}" for h in headers_list)

# ── Gmail actions ─────────────────────────────────────────
def move_to_trash(service, message_id: str) -> bool:
    """Use Gmail's native trash() API — cleanest way to delete."""
    try:
        service.users().messages().trash(
            userId='me', id=message_id
        ).execute()
        print(f"         ✓ Moved to TRASH")
        return True
    except Exception as e:
        print(f"    [!] Could not move to trash: {e}")
        import traceback; traceback.print_exc()
        return False

def star_message(service, message_id: str):
    """Star medium-risk emails for manual review."""
    try:
        service.users().messages().modify(
            userId='me', id=message_id,
            body={'addLabelIds': ['STARRED']}
        ).execute()
    except Exception:
        pass

# ── Notification email ────────────────────────────────────
def _action_label(action: str) -> str:
    return {
        'moved_to_trash':  '🗑 Moved to Trash',
        'starred_warning': '⭐ Starred for Review',
        'clean':           '✅ Clean',
        'trash_failed':    '⚠ Trash Failed',
    }.get(action, action)

def _rows_html(email_list, row_bg):
    if not email_list:
        return ('<tr><td colspan="4" style="padding:12px 16px;color:#666;'
                'font-style:italic;font-size:12px">None this scan</td></tr>')
    out = ''
    for e in email_list:
        flags = (e.get('flags') or [])[:3]
        flags_html = ''.join(
            f'<div style="font-size:10px;color:#999;margin-top:3px">• {f}</div>'
            for f in flags
        )
        sc = e.get('score', 0)
        score_color = ('#ff4757' if sc >= 60 else
                       '#ffa502' if sc >= 40 else '#2ed573')
        out += f"""
        <tr style="background:{row_bg};border-bottom:1px solid #222">
          <td style="padding:10px 14px;font-size:12px;color:#ccc;max-width:180px;
                     word-break:break-word">{(e.get('sender') or '')[:55]}</td>
          <td style="padding:10px 14px;font-size:12px;color:#ddd;max-width:220px">
            {(e.get('subject') or '')[:65]}{flags_html}
          </td>
          <td style="padding:10px 14px;font-size:13px;font-weight:700;
                     color:{score_color};white-space:nowrap">{sc}/100</td>
          <td style="padding:10px 14px;font-size:11px;color:#aaa;
                     white-space:nowrap">{_action_label(e.get('action',''))}</td>
        </tr>"""
    return out

def build_notification_html(user_email, trashed, starred, clean):
    now_str = datetime.datetime.now().strftime('%d %b %Y at %I:%M %p')
    total   = len(trashed) + len(starred) + len(clean)

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0a0a0a;
             font-family:'Segoe UI',Arial,sans-serif">
<div style="max-width:680px;margin:0 auto;padding:24px 16px">
<div style="background:#111;border-radius:12px;overflow:hidden;
            border:1px solid #222">

  <!-- Header -->
  <div style="background:linear-gradient(135deg,#0f2027 0%,#1a3a4a 100%);
              padding:26px 30px;border-bottom:2px solid #00e5c8">
    <div style="font-size:11px;color:#00e5c8;letter-spacing:.12em;
                font-weight:700;margin-bottom:10px">
      ● EMAIL SECURITY WATCHDOG v3
    </div>
    <div style="font-size:20px;font-weight:700;color:#fff;margin-bottom:6px">
      🛡 Scan Report — {now_str}
    </div>
    <div style="font-size:12px;color:#aaa">
      Mailbox: <strong style="color:#ddd">{user_email}</strong>
      &nbsp;·&nbsp;
      {total} email{'s' if total!=1 else ''} scanned this run
    </div>
  </div>

  <!-- Summary bar -->
  <table style="width:100%;border-collapse:collapse;
                border-bottom:1px solid #222">
    <tr>
      <td style="padding:18px;text-align:center;
                 border-right:1px solid #222;background:#1a0a0a">
        <div style="font-size:32px;font-weight:800;color:#ff4757;
                    line-height:1">{len(trashed)}</div>
        <div style="font-size:10px;color:#888;margin-top:4px;
                    text-transform:uppercase;letter-spacing:.07em">
          Moved to Trash
        </div>
      </td>
      <td style="padding:18px;text-align:center;
                 border-right:1px solid #222;background:#1a1400">
        <div style="font-size:32px;font-weight:800;color:#ffa502;
                    line-height:1">{len(starred)}</div>
        <div style="font-size:10px;color:#888;margin-top:4px;
                    text-transform:uppercase;letter-spacing:.07em">
          Starred for Review
        </div>
      </td>
      <td style="padding:18px;text-align:center;background:#0a1a0a">
        <div style="font-size:32px;font-weight:800;color:#2ed573;
                    line-height:1">{len(clean)}</div>
        <div style="font-size:10px;color:#888;margin-top:4px;
                    text-transform:uppercase;letter-spacing:.07em">
          Clean
        </div>
      </td>
    </tr>
  </table>

  <!-- Trashed -->
  <div style="padding:16px 20px 6px">
    <div style="font-size:11px;font-weight:700;color:#ff4757;
                text-transform:uppercase;letter-spacing:.08em">
      🗑 HIGH RISK — Moved to Trash ({len(trashed)})
    </div>
  </div>
  <table style="width:100%;border-collapse:collapse">
    <thead>
      <tr style="background:#1a1a1a">
        <th style="padding:7px 14px;font-size:9px;color:#555;text-align:left;
                   text-transform:uppercase;letter-spacing:.07em">Sender</th>
        <th style="padding:7px 14px;font-size:9px;color:#555;text-align:left;
                   text-transform:uppercase;letter-spacing:.07em">Subject / Flags</th>
        <th style="padding:7px 14px;font-size:9px;color:#555;text-align:left;
                   text-transform:uppercase;letter-spacing:.07em">Score</th>
        <th style="padding:7px 14px;font-size:9px;color:#555;text-align:left;
                   text-transform:uppercase;letter-spacing:.07em">Action</th>
      </tr>
    </thead>
    <tbody>{_rows_html(trashed, '#160808')}</tbody>
  </table>

  <!-- Starred -->
  <div style="padding:16px 20px 6px;margin-top:6px">
    <div style="font-size:11px;font-weight:700;color:#ffa502;
                text-transform:uppercase;letter-spacing:.08em">
      ⭐ MEDIUM RISK — Starred for Review ({len(starred)})
    </div>
  </div>
  <table style="width:100%;border-collapse:collapse">
    <thead>
      <tr style="background:#1a1a1a">
        <th style="padding:7px 14px;font-size:9px;color:#555;text-align:left;
                   text-transform:uppercase;letter-spacing:.07em">Sender</th>
        <th style="padding:7px 14px;font-size:9px;color:#555;text-align:left;
                   text-transform:uppercase;letter-spacing:.07em">Subject / Flags</th>
        <th style="padding:7px 14px;font-size:9px;color:#555;text-align:left;
                   text-transform:uppercase;letter-spacing:.07em">Score</th>
        <th style="padding:7px 14px;font-size:9px;color:#555;text-align:left;
                   text-transform:uppercase;letter-spacing:.07em">Action</th>
      </tr>
    </thead>
    <tbody>{_rows_html(starred, '#141000')}</tbody>
  </table>

  <!-- What the tool did -->
  <div style="padding:20px 24px;background:#0d1117;border-top:1px solid #222;
              margin-top:10px">
    <div style="font-size:11px;font-weight:700;color:#00e5c8;
                text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px">
      What Your Watchdog Did
    </div>
    <div style="font-size:12px;color:#888;line-height:1.9">
      {"✅ <span style='color:#ccc'>No threats detected this scan. Your inbox is clean.</span>" if not trashed and not starred else ""}
      {f"🗑 <span style='color:#ccc'>Permanently moved <strong style=color:#ff4757>{len(trashed)}</strong> high-risk email(s) to Trash. These emails showed signs of brand impersonation, Reply-To mismatch, or failed SPF/DKIM/DMARC checks.</span><br>" if trashed else ""}
      {f"⭐ <span style='color:#ccc'>Starred <strong style=color:#ffa502>{len(starred)}</strong> medium-risk email(s) for your manual review. These showed mild suspicious signals but were not deleted.</span><br>" if starred else ""}
      {f"✅ <span style='color:#ccc'>{len(clean)} email(s) passed all checks and were left untouched.</span>" if clean else ""}
    </div>
  </div>

  <!-- Footer -->
  <div style="padding:18px 24px;background:#0a0a0a;border-top:1px solid #1a1a1a;
              text-align:center">
    <div style="font-size:11px;color:#444">
      This is an automated report from your Email Security Watchdog.
      &nbsp;·&nbsp;
      View full dashboard at
      <a href="http://127.0.0.1:5000"
         style="color:#00e5c8;text-decoration:none">127.0.0.1:5000</a>
    </div>
    <div style="font-size:10px;color:#2a2a2a;margin-top:8px;letter-spacing:.05em">
      EMAIL SECURITY WATCHDOG v3 · Built by Nivedhitha KS
    </div>
  </div>

</div>
</div>
</body>
</html>"""


def send_notification_email(service, user_email, trashed, starred, clean):
    """Send one consolidated HTML report email after each scan."""
    if not trashed and not starred:
        print("[*] All clean — no notification email sent")
        return

    try:
        html = build_notification_html(user_email, trashed, starred, clean)

        msg            = MIMEMultipart('alternative')
        count_str      = f"{len(trashed)} deleted, {len(starred)} flagged"
        msg['Subject'] = (f"🛡 Watchdog Report: {count_str} — "
                          f"{datetime.datetime.now().strftime('%d %b %Y %H:%M')}")
        msg['From']    = f"Email Security Watchdog <{user_email}>"
        msg['To']      = user_email
        msg['X-Watchdog-Notification'] = 'true'   # so we don't re-scan this

        msg.attach(MIMEText(html, 'html'))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().messages().send(
            userId='me', body={'raw': raw}
        ).execute()
        print(f"[+] Notification email sent to {user_email}")

    except Exception as e:
        print(f"[!] Notification email failed: {e}")
        import traceback; traceback.print_exc()


# ── Main scan ─────────────────────────────────────────────
def scan_inbox() -> list:
    """
    Scans ALL folders (inbox, spam, promotions...) from last 3 days.
    HIGH RISK   → moved to Trash  → appears in notification email
    MEDIUM RISK → starred         → appears in notification email
    After scan  → sends one HTML summary email to user's mailbox
    """
    print(f"\n[*] Scan started: {datetime.datetime.now().strftime('%H:%M:%S')}")
    results      = []
    trashed_list = []
    starred_list = []
    clean_list   = []

    try:
        service    = get_gmail_service()
        user_email = get_user_email(service)
        print(f"[*] Authenticated as: {user_email}")
    except Exception as e:
        print(f"[!] Gmail auth error: {e}")
        return results

    try:
        response = service.users().messages().list(
            userId='me',
            q='newer_than:3d -subject:"Watchdog Report"',
            maxResults=50
        ).execute()

        messages = response.get('messages', [])
        print(f"[*] Found {len(messages)} messages to check")

        for msg_ref in messages:
            msg_id = msg_ref['id']
            if is_already_scanned(msg_id):
                continue

            try:
                full_msg = service.users().messages().get(
                    userId='me', id=msg_id,
                    format='metadata',
                    metadataHeaders=HEADER_NAMES
                ).execute()

                headers_list = full_msg.get('payload', {}).get('headers', [])
                headers_dict = {h['name']: h['value'] for h in headers_list}
                raw_text     = headers_to_text(headers_list)

                # Skip our own watchdog notification emails
                if headers_dict.get('X-Watchdog-Notification') == 'true':
                    print(f"  → Skipping watchdog notification")
                    continue

                sender  = headers_dict.get('From',    headers_dict.get('from',    ''))
                subject = headers_dict.get('Subject', headers_dict.get('subject', ''))
                date    = headers_dict.get('Date',    headers_dict.get('date',    ''))

                print(f"  → Analyzing: {subject[:60]!r} from {sender[:50]!r}")

                result           = analyze_headers(headers_dict)
                result['sender'] = sender
                result['subject']= subject

                action_taken = 'clean'

                if result['verdict'] == 'HIGH RISK':
                    ok = move_to_trash(service, msg_id)
                    action_taken = 'moved_to_trash' if ok else 'trash_failed'
                    print(f"     Score: {result['score']} → HIGH RISK — "
                          f"{'TRASHED ✓' if ok else 'FAILED'}")
                    trashed_list.append({
                        'sender':  sender,  'subject': subject,
                        'score':   result['score'],
                        'flags':   result['flags'],
                        'action':  action_taken
                    })

                elif result['verdict'] == 'MEDIUM RISK':
                    star_message(service, msg_id)
                    action_taken = 'starred_warning'
                    print(f"     Score: {result['score']} → MEDIUM RISK — starred")
                    starred_list.append({
                        'sender':  sender,  'subject': subject,
                        'score':   result['score'],
                        'flags':   result['flags'],
                        'action':  action_taken
                    })

                else:
                    print(f"     Score: {result['score']} → clean")
                    clean_list.append({
                        'sender':  sender, 'subject': subject,
                        'score':   result['score'],
                        'flags':   [], 'action': 'clean'
                    })

                save_result(msg_id, sender, subject, date,
                            result, action_taken, raw_text)
                result['action_taken'] = action_taken
                results.append(result)

            except Exception as e:
                print(f"    [!] Error on {msg_id}: {e}")
                continue

    except Exception as e:
        print(f"[!] Gmail list error: {e}")

    print(f"[*] Done — Trashed: {len(trashed_list)} | "
          f"Starred: {len(starred_list)} | Clean: {len(clean_list)}\n")

    # Send one consolidated email report
    send_notification_email(service, user_email,
                            trashed_list, starred_list, clean_list)
    return results
