# Day 14 — Week 2 Review

> **60-Day Cybersecurity Journey** | [GitHub](https://github.com/NivedhithaKS-SEC/cybersec-journey)

---

## What I completed today

### TryHackMe Rooms

| Room | Points | Status |
|------|--------|--------|
| OWASP Top 10 | — | ✅ Badge earned |
| Monitoring Active Directory | 104 | ✅ Completed |
| Writing Pentest Reports | 48 | ✅ Completed |

**Streak:** 2 days active

---

### CEH Cheat Sheet

- **File:** `ceh-cheatsheet.md` (21 KB)
- Covers CEH Modules 1–11 with commands, tables, and tool references
- Includes: Quick Reference ports table, Nmap flags, Metasploit workflow, Meterpreter commands, password attack types, Hydra/John/Hashcat syntax, OWASP vulnerability table, social engineering tactics, DoS types, session hijacking methods

---

### Portfolio Project — Email Header Analyzer

> A live web app for detecting phishing and email spoofing via raw email header analysis.

**Live demo:** https://email-header-analyzer-4snb.onrender.com  
**Repo:** https://github.com/NivedhithaKS-SEC/email-header-analyzer

**Stack:** Python 3, Flask, HTML/CSS

**What it does:**
- SPF / DKIM / DMARC authentication checks
- Reply-To mismatch detection
- Display name spoofing detection
- Urgency language analysis
- Mail routing hop analysis
- Risk score 0–100 with phishing verdict

**Files:**
```
email-header-analyzer/
├── app.py              # Flask backend (11 KB)
├── templates/          # HTML frontend
├── requirements.txt    # Dependencies
├── render.yaml         # Deployment config (Render)
└── README.md
```

**Skills demonstrated:**  
`Flask` · `Email security` · `SPF/DKIM/DMARC` · `Phishing detection` · `Python` · `Web app deployment`

**Why this matters:**  
Email header analysis is a real-world skill used in SOC analyst roles, incident response, and phishing investigations. This tool automates what security analysts do manually when triaging suspicious emails.

---

## Day 14 Stats

| Metric | Count |
|--------|-------|
| TryHackMe points earned today | ~152 |
| Running TryHackMe total | 630+ |
| Rooms completed today | 3 |
| Badges earned today | 1 (OWASP Top 10) |
| Files committed | 2 (cheat sheet + project) |
| Live deployed tools | 1 |

---

## Key learnings today

**Monitoring Active Directory**  
- Windows Event IDs to monitor: 4624 (logon), 4625 (failed logon), 4720 (account created), 4732 (added to group)
- Tools: Event Viewer, Sysmon, Windows Defender for Identity
- Attack patterns: Pass-the-Hash, Kerberoasting, Golden Ticket attacks leave specific event trails

**Writing Pentest Reports**  
- Report structure: Executive Summary → Scope → Methodology → Findings → Risk Ratings → Recommendations → Appendix
- Each finding needs: Title, CVSS score, Description, Evidence (screenshot), Impact, Recommendation
- Write for two audiences: executives (plain English) and technical team (commands + proof)
- CVSS scoring: Base Score = Exploitability + Impact metrics

**OWASP Top 10**  
- A01: Broken Access Control (most common — IDOR, privilege escalation)
- A02: Cryptographic Failures (HTTP, weak ciphers, hardcoded keys)
- A03: Injection (SQLi, command injection, LDAP injection)
- A07: Identification & Auth Failures (brute force, weak session tokens)
- A10: SSRF (Server-Side Request Forgery — new in 2021)

---

## Week 2 Summary (Days 8–14)

| Day | Topic | Key Tool/Skill |
|-----|-------|---------------|
| Day 8 | Vulnerability Scanning | Nessus, Nikto |
| Day 9 | Web App Security | SQLmap, manual SQLi |
| Day 10 | Burp Suite | HTTP interception, repeater |
| Day 11 | Subdomain Enumerator | Python tool built |
| Day 12 | Wireshark + Sniffing | PCAP analysis, tcpdump |
| Day 13 | Recon + Port Scanner v2 | nmap automation, VDP submission |
| Day 14 | Review + AD + Reports | CEH cheat sheet, Email Analyzer deployed |

**Week 2 highlight:** Built and deployed a live phishing detection tool at a public URL.

---

## Week 3 Plan (Days 15–21)

| Priority | Topic | Why |
|----------|-------|-----|
| High | Linux Privilege Escalation | Core pentesting skill, needed for CTFs |
| High | Active Directory Attacks | Pass-the-Hash, Kerberoasting — enterprise focus |
| High | More Web App Attacks | XSS, CSRF, File Upload vulnerabilities |
| Medium | CTF Practice | Apply everything learned, earn more points |
| Medium | VDP Follow-up | Check status of first submission, submit second |
| Low | Windows Basics | Complement AD knowledge |

**TryHackMe goal for Week 3:** 800+ points  
**GitHub goal:** 50+ total commits  
**VDP goal:** 2nd submission done

---

*Part of my 60-day cybersecurity learning journey.*  
*GitHub: [NivedhithaKS-SEC/cybersec-journey](https://github.com/NivedhithaKS-SEC/cybersec-journey)*
