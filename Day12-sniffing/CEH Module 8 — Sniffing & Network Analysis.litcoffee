# CEH Module 8 — Sniffing & Network Analysis

## What is Sniffing?
Capturing network packets as they travel across a network.
Like a wiretap on a phone line — everything passing through
can be read if not encrypted.

## Types of Sniffing

### Passive Sniffing
- Listen only — no packets injected
- Works on HUB-based networks
- Harder to detect
- Example: Plugging into a network and listening

### Active Sniffing
- Injects packets to redirect traffic
- Works on SWITCH-based networks
- More detectable
- Techniques: ARP poisoning, MAC flooding

## ARP Poisoning (ARP Spoofing)
Most important MITM technique — must know for CEH!

### How it works:
1. Attacker sends fake ARP replies to victim
2. Victim's ARP table updated with attacker's MAC
3. Victim sends traffic to attacker instead of router
4. Attacker forwards it (so victim doesn't notice)
5. Attacker reads ALL traffic in between

### ARP Poisoning Attack Flow:
```
Victim thinks: Router = 192.168.1.1 (real MAC)
After attack:  Router = 192.168.1.1 (ATTACKER MAC)
All traffic now flows through attacker!
```

## MAC Flooding
- Floods switch with fake MAC addresses
- Switch runs out of memory (CAM table overflow)
- Switch starts broadcasting to all ports (acts like a hub)
- Attacker can now sniff all traffic
- Tool: macof

## MITM (Man-in-the-Middle) Attack
Attacker positions themselves between two communicating parties.
```
Normal:   Victim ←→ Router ←→ Internet
MITM:     Victim ←→ Attacker ←→ Router ←→ Internet
```

Attacker can:
- Read all unencrypted traffic
- Steal credentials
- Inject malicious content
- Capture session cookies

## Protocols Vulnerable to Sniffing
| Protocol | Port | Risk |
|----------|------|------|
| HTTP | 80 | Passwords visible in plain text |
| FTP | 21 | Username/password cleartext |
| Telnet | 23 | Everything cleartext |
| SMTP | 25 | Email content visible |
| DNS | 53 | Queries visible |
| HTTPS | 443 | ENCRYPTED — safe |
| SSH | 22 | ENCRYPTED — safe |

## Wireshark Filters (Important for CEH)
```
http                    — show only HTTP traffic
dns                     — show only DNS queries
tcp.port == 80          — traffic on port 80
ip.addr == 192.168.1.1  — traffic to/from IP
http.request.method == "POST" — login attempts
tcp.flags.syn == 1      — TCP SYN packets (new connections)
```

## Tools Used for Sniffing
- **Wireshark** — GUI packet analyzer
- **tcpdump** — command line packet capture
- **Ettercap** — MITM + ARP poisoning
- **Bettercap** — modern MITM framework
- **dsniff** — credential sniffing

## Countermeasures
- Use HTTPS everywhere (HTTP sends passwords in plain text!)
- Use SSH instead of Telnet
- VPN for all sensitive traffic
- Dynamic ARP Inspection (DAI) on switches
- Use encrypted protocols only
- HTTPS Everywhere browser extension