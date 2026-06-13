# ============================================================
# Email Security Watchdog v3 — Industrial Grade
# Auto-scans all incoming mail, scores threats, moves spam,
# sends real-time sidebar notifications
# ============================================================

from flask import Flask, jsonify, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import datetime
import os
import threading
import json

app = Flask(__name__)

# ── Global state ──────────────────────────────────────────
scan_lock = threading.Lock()
notification_queue = []   # Live notifications for SSE / polling
MAX_NOTIFICATIONS = 50

DB_PATH = "watchdog.db"

# ── Database ──────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scanned_emails (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id    TEXT UNIQUE,
            sender        TEXT,
            subject       TEXT,
            received_at   TEXT,
            scanned_at    TEXT,
            risk_score    INTEGER,
            verdict       TEXT,
            flags         TEXT,
            action_taken  TEXT,
            raw_headers   TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            level      TEXT,
            title      TEXT,
            message    TEXT,
            sender     TEXT,
            subject    TEXT,
            score      INTEGER,
            read       INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_notification(level, title, message, sender="", subject="", score=0):
    """Persist a notification and add to live queue."""
    now = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO notifications (created_at, level, title, message, sender, subject, score)
        VALUES (?,?,?,?,?,?,?)
    """, (now, level, title, message, sender, subject, score))
    conn.commit()
    conn.close()

    notification_queue.append({
        "time": now,
        "level": level,
        "title": title,
        "message": message,
        "sender": sender,
        "subject": subject,
        "score": score
    })
    if len(notification_queue) > MAX_NOTIFICATIONS:
        notification_queue.pop(0)

# ── Scan trigger ──────────────────────────────────────────
def run_scan():
    """Called by scheduler every 60 s. Thread-safe."""
    if scan_lock.locked():
        return
    with scan_lock:
        try:
            from watchdog import scan_inbox
            results = scan_inbox()
            for r in results:
                if r["verdict"] in ("HIGH RISK", "MEDIUM RISK"):
                    level = "danger" if r["verdict"] == "HIGH RISK" else "warning"
                    flags_list = json.loads(r.get("flags", "[]")) if isinstance(r.get("flags"), str) else r.get("flags", [])
                    reason = "; ".join(flags_list[:3]) if flags_list else "Suspicious patterns detected"
                    action_label = "🗑 Moved to Trash" if r["verdict"] == "HIGH RISK" else "⭐ Starred for Review"
                    add_notification(
                        level=level,
                        title=f"🚨 {r['verdict']} — {action_label}",
                        message=reason,
                        sender=r.get("sender", ""),
                        subject=r.get("subject", ""),
                        score=r.get("risk_score", 0)
                    )
                elif r["verdict"] == "LOW RISK":
                    add_notification(
                        level="info",
                        title="✅ Clean Email Scanned",
                        message="No threats detected",
                        sender=r.get("sender", ""),
                        subject=r.get("subject", ""),
                        score=r.get("risk_score", 0)
                    )
        except Exception as e:
            print(f"[!] Scan error: {e}")
            add_notification("error", "⚠ Scan Error", str(e))

# ── Scheduler ─────────────────────────────────────────────
scheduler = BackgroundScheduler()
scheduler.add_job(run_scan, 'interval', seconds=60, id='mail_scan')

# ── Routes ────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/scan', methods=['POST'])
def manual_scan():
    """Trigger an immediate scan."""
    thread = threading.Thread(target=run_scan)
    thread.daemon = True
    thread.start()
    return jsonify({"status": "scan_started"})

@app.route('/api/stats')
def stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM scanned_emails")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM scanned_emails WHERE verdict='HIGH RISK'")
    high = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM scanned_emails WHERE verdict='MEDIUM RISK'")
    medium = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM scanned_emails WHERE verdict='LOW RISK'")
    low = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM scanned_emails WHERE action_taken='moved_to_spam'")
    moved = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM scanned_emails WHERE DATE(scanned_at)=DATE('now')")
    today = c.fetchone()[0]
    c.execute("SELECT scanned_at FROM scanned_emails ORDER BY scanned_at DESC LIMIT 1")
    row = c.fetchone()
    last_scan = row[0] if row else "Never"
    conn.close()
    return jsonify({
        "total": total, "high": high, "medium": medium,
        "low": low, "moved_to_spam": moved, "today": today,
        "last_scan": last_scan,
        "scheduler_running": scheduler.running
    })

@app.route('/api/emails')
def emails():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    verdict_filter = request.args.get('verdict', '')
    offset = (page - 1) * per_page

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    base_q = "FROM scanned_emails"
    params = []
    if verdict_filter:
        base_q += " WHERE verdict=?"
        params.append(verdict_filter)

    c.execute(f"SELECT COUNT(*) {base_q}", params)
    total_count = c.fetchone()[0]

    c.execute(f"""
        SELECT id, message_id, sender, subject, received_at, scanned_at,
               risk_score, verdict, flags, action_taken
        {base_q}
        ORDER BY scanned_at DESC
        LIMIT ? OFFSET ?
    """, params + [per_page, offset])
    rows = c.fetchall()
    conn.close()

    emails_list = []
    for row in rows:
        flags = json.loads(row[8]) if row[8] else []
        emails_list.append({
            "id": row[0], "message_id": row[1], "sender": row[2],
            "subject": row[3], "received_at": row[4], "scanned_at": row[5],
            "risk_score": row[6], "verdict": row[7],
            "flags": flags, "action_taken": row[9]
        })

    return jsonify({"emails": emails_list, "total": total_count, "page": page, "per_page": per_page})

@app.route('/api/notifications')
def notifications():
    since = request.args.get('since', '')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if since:
        c.execute("""
            SELECT id, created_at, level, title, message, sender, subject, score, read
            FROM notifications WHERE created_at > ? ORDER BY created_at DESC LIMIT 30
        """, (since,))
    else:
        c.execute("""
            SELECT id, created_at, level, title, message, sender, subject, score, read
            FROM notifications ORDER BY created_at DESC LIMIT 30
        """)
    rows = c.fetchall()
    conn.close()
    return jsonify([{
        "id": r[0], "time": r[1], "level": r[2], "title": r[3],
        "message": r[4], "sender": r[5], "subject": r[6],
        "score": r[7], "read": r[8]
    } for r in rows])

@app.route('/api/notifications/mark_read', methods=['POST'])
def mark_read():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE notifications SET read=1")
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route('/api/analyze', methods=['POST'])
def analyze_manual():
    """Manual header paste analysis."""
    data = request.json
    raw = data.get('headers', '')
    if not raw:
        return jsonify({"error": "No headers provided"}), 400
    from analyzer_engine import parse_raw_headers, analyze_headers
    headers = parse_raw_headers(raw)
    result = analyze_headers(headers)
    return jsonify(result)

@app.route('/api/email/<int:email_id>/headers')
def get_headers(email_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT raw_headers, sender, subject, verdict, risk_score, flags FROM scanned_emails WHERE id=?", (email_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "raw_headers": row[0] or "",
        "sender": row[1], "subject": row[2],
        "verdict": row[3], "risk_score": row[4],
        "flags": json.loads(row[5]) if row[5] else []
    })

# ── Boot ──────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()

    print("=" * 60)
    print("  EMAIL SECURITY WATCHDOG v3")
    print("  Industrial-grade inbox monitoring")
    print("  http://127.0.0.1:5000")
    print("=" * 60)

    # Check Gmail auth
    if not os.path.exists('token.pickle'):
        print("\n[!] token.pickle not found.")
        print("    Run:  python gmail_auth.py  first\n")
    else:
        scheduler.start()
        print("[*] Scheduler started — scanning every 60 seconds")
        print("[*] Running first scan now...\n")
        thread = threading.Thread(target=run_scan)
        thread.daemon = True
        thread.start()

    app.run(debug=False, host='0.0.0.0', port=5000)
