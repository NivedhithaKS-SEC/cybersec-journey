# Day 15 — Web App Hacking + HTB Starting Point

> **60-Day Cybersecurity Journey** | [GitHub Profile](https://github.com/NivedhithaKS-SEC/cybersec-journey)

---

## What I covered today

| Task | Topic | Status |
|------|-------|--------|
| CEH Module 12 | Evading IDS, Firewalls & Honeypots | [ ] |
| CEH Module 13 | Hacking Web Servers | [ ] |
| DVWA Lab | Reflected XSS + Stored XSS (Low/Medium/High) | [ ] |
| PortSwigger | 3 XSS Labs (Reflected, Stored, DOM) | [ ] |
| Python | JSON parsing + API call script | [ ] |
| Hack The Box | Account setup + Starting Point Tier 0 | [ ] |

---

## Files in This Folder

| File | Description |
|------|-------------|
| `ceh-module12-notes.md` | IDS/Firewall/Honeypot evasion — full notes + commands |
| `ceh-module13-notes.md` | Web server attacks — directory traversal, banner grabbing, tools |
| `xss-lab-notes.md` | XSS lab notes — DVWA + PortSwigger step-by-step |
| `python-json-notes.md` | JSON concepts + real API examples |
| `ip_info.py` | IP geolocation tool (Python + JSON + API calls) |
| `htb-starting-point.md` | HTB Starting Point walkthrough — Meow, Fawn, Dancing, Redeemer |
| `screenshots/` | Lab evidence — XSS alerts, PortSwigger solved banners, HTB flags |

---

## Tool Built Today

### ip_info.py — IP Geolocation Tool
```bash
python3 ip_info.py 8.8.8.8           # Single IP lookup
python3 ip_info.py -f ips.txt        # Batch from file
python3 ip_info.py 8.8.8.8 -v        # Verbose (raw JSON)
python3 ip_info.py 1.1.1.1 -o out.json  # Save to JSON
```
Fetches country, city, ISP, ASN, timezone for any IP. Uses free `ipapi.co` API.

---

## Key Learnings

### XSS Types
- **Reflected XSS** — payload in URL, affects only users who click crafted link
- **Stored XSS** — payload saved to DB, fires for every visitor automatically
- **DOM XSS** — payload processed by client-side JavaScript, server never sees it

### Web Server Attacks
- **Directory traversal** — `../../../etc/passwd` accesses files outside web root
- **Banner grabbing** — `curl -I target.com` reveals server version for CVE research
- **Misconfigurations** — exposed `.git`, `.env`, default creds, dangerous HTTP methods

### IDS Evasion
- **Fragmentation** — `nmap -f` splits packets so IDS can't match signature
- **Decoy scan** — `nmap -D RND:10` hides real attacker IP in 10 fake ones
- **Slow scan** — `nmap -T0` spreads scan over hours, below rate-based IDS thresholds

---

## PortSwigger Labs Completed

| Lab | Type | Payload | Result |
|-----|------|---------|--------|
| Lab 1 — Reflected XSS, nothing encoded | Reflected | `<script>alert(1)</script>` | [ ] |
| Lab 2 — Stored XSS, nothing encoded | Stored | `<script>alert(1)</script>` | [ ] |
| Lab 3 — DOM XSS in document.write | DOM | `"><svg onload=alert(1)>` | [ ] |

---

## HTB Starting Point Progress

| Machine | Concept | Flag |
|---------|---------|------|
| Meow | Telnet + blank credentials | [ ] |
| Fawn | FTP anonymous login | [ ] |
| Dancing | SMB null session | [ ] |
| Redeemer | Redis unauthenticated | [ ] |

---

*Part of my 60-day cybersecurity learning journey.*  
*GitHub: [NivedhithaKS-SEC/cybersec-journey](https://github.com/NivedhithaKS-SEC/cybersec-journey)*
