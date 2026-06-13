# Email Security Watchdog v3

Industrial-grade Gmail inbox monitor. Automatically scans all incoming mail, scores phishing risk, moves threats to spam, and delivers real-time notifications.

## Features
- Auto-scans **all folders** (inbox, spam, promotions) every 60 seconds
- 15+ detection checks: SPF/DKIM/DMARC, brand spoofing, Reply-To mismatch, urgency patterns, suspicious TLDs
- **Automatic spam action** — HIGH RISK emails moved to Gmail spam instantly
- **Live notification sidebar** — real-time alerts showing what was caught and why
- Manual header paste analyzer
- Email detail view with raw headers
- Paginated email log with filtering by verdict

## Setup
```bash
pip install -r requirements.txt
python gmail_auth.py    # one-time OAuth2 setup
python app.py
```
Open http://127.0.0.1:5000

## Files
| File | Purpose |
|------|---------|
| `app.py` | Flask app, scheduler, API routes |
| `analyzer_engine.py` | 15+ check phishing detection engine |
| `watchdog.py` | Gmail API fetch + spam actions |
| `gmail_auth.py` | One-time OAuth2 authentication |
| `templates/dashboard.html` | Full dark industrial UI |

## Built by
Nivedhitha KS | Cybersecurity Portfolio
