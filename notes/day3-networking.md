*# Day 3 — Networking Fundamentals + Nmap*



*## OSI Model (7 Layers)*

*- Layer 1 Physical: cables, signals, bits*

*- Layer 2 Data Link: MAC addresses, ARP, Ethernet*

*- Layer 3 Network: IP addressing, routing (nmap, ping, traceroute)*

*- Layer 4 Transport: TCP (reliable, 3-way handshake) / UDP (fast)*

*- Layer 5 Session: opens and closes connections*

*- Layer 6 Presentation: encryption/decryption, TLS/SSL*

*- Layer 7 Application: HTTP, DNS, FTP — what users see*



*## TCP vs UDP*

*- TCP: SYN → SYN-ACK → ACK (reliable, slower)*

*- UDP: no handshake (fast, used for DNS/video/gaming)*



*## Key Ports*

*- 21 FTP | 22 SSH | 23 Telnet | 25 SMTP*

*- 53 DNS | 80 HTTP | 443 HTTPS | 3389 RDP*



*## DNS Tools*

*- dig google.com +short       → quick IP lookup*

*- dig google.com +trace       → full resolution chain*

*- nslookup google.com         → basic lookup*

*- whois google.com            → domain ownership*



*## Kali Linux Lab Results*

*- My IP: 192.168.1.7 (VirtualBox eth0)*

*- MAC: 08:00:27:b4:a1:05*

*- ping google.com: 0% packet loss, ~21ms from Kerala*

*- traceroute: 9 hops — Kerala Vision ISP → Google Jakarta*

*- nmap 192.168.1.0/24: 5 live devices found*

*- Router 192.168.1.1: port 53 and 80 open*

*- dig +trace: watched full DNS chain live*



*## Python — Loops*

*- for loop: for i in range(1, 101)*

*- while loop: runs until condition is false*

*- % modulo operator: checks divisibility*

*- FizzBuzz.py: completed successfully*

*- PortScannerUsingLoops.py: completed successfully*