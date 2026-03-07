## CEH Module 3 — Scanning Networks 📡

##What is Scanning?
Scanning is Phase 2 of ethical hacking. After footprinting (finding info), you now actively touch the target to find:
Which hosts are alive on the network
Which ports are open
Which services are running
Which OS the target uses
Which vulnerabilities exist

Think of it like this:
Footprinting = Watching a building from outside
Scanning     = Walking up and knocking on every door

## Three Types of Scanning
1. Network Scanning
Finding live hosts on a network. Who's online?
bashnmap -sn 192.168.1.0/24        # Ping sweep — find live hosts
2. Port Scanning
Finding open ports on a live host. Which doors are unlocked?
bashnmap -p 1-1024 192.168.1.1     # Scan ports 1-1024
nmap -p- 192.168.1.1           # Scan ALL 65535 ports
3. Vulnerability Scanning
Finding weaknesses in open services. Which doors have broken locks?
bashnmap --script vuln 192.168.1.1  # Run vulnerability scripts

## 🤝 TCP 3-Way Handshake — MUST KNOW

Every TCP connection follows this exact sequence. Understanding this is the foundation of ALL port scanning.
```
Client          Server
  |                |
  |---- SYN ------>|   "Hey, can we talk?"
  |                |
  |<-- SYN-ACK ----|   "Yes, I'm listening!"
  |                |
  |---- ACK ------>|   "Great, let's connect."
  |                |
  [Connection established]
Why this matters for scanning: Different scan types manipulate or break this handshake in different ways to stay stealthy or gather info.

## Port Scanning Techniques
1. TCP Connect Scan (-sT)
Completes the full 3-way handshake.
bashnmap -sT target

✅ Most reliable — works without root/admin
❌ Easily detected — full connection logged by target
Your Python port scanner uses this method (connect_ex())

2. SYN Scan / Stealth Scan (-sS) ← Most Popular
Sends SYN, gets SYN-ACK, then sends RST (reset) instead of ACK. Never completes the handshake.
bashnmap -sS target    # Requires root/admin
```
```
Client          Server
  |---- SYN ------>|
  |<-- SYN-ACK ----|   Port is OPEN
  |---- RST ------>|   "Never mind." (stays stealthy)

✅ Stealthy — many firewalls/logs miss incomplete connections
✅ Faster than TCP Connect
❌ Requires root privileges

3. UDP Scan (-sU)
Scans UDP ports — no handshake because UDP is connectionless.
bashnmap -sU target

DNS (port 53), DHCP (67/68), SNMP (161) use UDP
❌ Very slow — no response can mean open OR filtered
Important for finding services TCP scans miss

4. NULL Scan (-sN)
Sends a packet with no flags set at all.
bashnmap -sN target

Open port → no response
Closed port → RST response
Used to bypass some firewalls. Doesn't work on Windows.

5. FIN Scan (-sF)
Sends only the FIN flag (normally used to close connections).
bashnmap -sF target

Same logic as NULL — closed port responds with RST
Bypasses some stateless firewalls

6. XMAS Scan (-sX)
Sends FIN + PSH + URG flags — "lights up like a Christmas tree."
bashnmap -sX target

Same behavior as NULL and FIN
Named XMAS because all flags are "lit"

Quick Comparison Table
Scan TypeFlags SentOpen Port ResponseStealthy?Needs Root?TCP ConnectSYNSYN-ACK❌ No❌ NoSYN/StealthSYNSYN-ACK + RST✅ Yes✅ YesUDPNoneNo response➖ Medium✅ YesNULLNoneNo response✅ Yes✅ YesFINFINNo response✅ Yes✅ YesXMASFIN+PSH+URGNo response✅ Yes✅ Yes

🖥️ OS Fingerprinting
Nmap guesses the target OS by analyzing how it responds to packets. Two methods:
Active OS Fingerprinting (-O)
Sends specially crafted packets and analyzes the response.
bashnmap -O target
Looks at: TTL values, TCP window size, packet behavior
Passive OS Fingerprinting
Doesn't send probes — just sniffs existing traffic silently. Tool: p0f
TTL Values (memorize these!)
OSTTL ValueWindows128Linux64Cisco Router255Solaris255
When you ping a target and see TTL=64 → likely Linux. TTL=128 → likely Windows.

🔎 Service Version Detection
Nmap can identify what software and version is running on an open port.
bashnmap -sV target
```
Example output:
```
22/tcp  open  ssh     OpenSSH 8.2p1 Ubuntu
80/tcp  open  http    Apache httpd 2.4.41
Why it matters: If Apache 2.4.41 has a known CVE, you now have a direct attack path.

🔥 Nmap Scripting Engine (NSE)
Nmap has 600+ built-in scripts for deeper scanning.
bashnmap -sC target                    # Run default scripts
nmap --script vuln target          # Check for vulnerabilities
nmap --script http-title target    # Get webpage titles
nmap --script banner target        # Grab service banners
Scripts are stored in /usr/share/nmap/scripts/ on Kali.

⚡ Important Nmap Flags (Memorize)
FlagMeaning-sSSYN/Stealth scan-sTTCP Connect scan-sUUDP scan-sVVersion detection-sCDefault scripts-OOS 
detection-AAggressive (OS + version + scripts + traceroute)-p 80Scan specific port-p 1-1024Scan port 
range-p-Scan all 65535 ports-T4Faster timing (T0=slowest, T5=fastest)-oN fileSave output to file-vVerbose output-PnSkip ping, assume host is up

🛡️ Countermeasures (Defender Side)
CEH tests both attack AND defense. Know these:
Against port scanning:

Firewall rules to block unsolicited SYN packets
IDS/IPS to detect scan patterns
Port knocking — ports only open after specific sequence

Against OS fingerprinting:

Modify TTL values in OS config
Use tools like scrub to normalize packets

Against banner grabbing:

Disable or falsify service banners
Apache: set ServerTokens Prod to hide version


📋 CEH Exam Key Points
These are high-frequency exam topics:

SYN scan = Half-open scan = Stealth scan — all the same thing
ICMP Echo = Ping — used in ping sweeps
Port states: Open, Closed, Filtered (firewall blocking)
Well-known ports: 0–1023 | Registered: 1024–49151 | Dynamic: 49152–65535
Nmap default scan = SYN scan if root, TCP Connect if not root
-A flag = OS detection + version + scripts + traceroute combined
Hping3 = alternative to nmap, used for crafting custom packets
Netcat = "Swiss army knife" — can scan ports, create backdoors, transfer files


🔧 Other Scanning Tools (CEH Syllabus)
ToolUseNmapThe gold standard port scannerHping3Custom packet crafting, ping sweepsNetcat (nc)Port scanning, 
banner grabbing, file transferMasscanFastest port scanner — scans entire internetAngry IP ScannerGUI-based, Windows-friendlyZenmapGUI version of Nmap