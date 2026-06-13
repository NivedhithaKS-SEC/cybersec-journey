# 🔍 Port Scanner v1.0

A Python TCP port scanner built as part of my **60-Day Cybersecurity Journey** (Day 5).

---

## What It Does

Scans a target host for **open TCP ports** in a given range (default: 1–1024).  
For each open port, it prints:
- The port number
- The associated service name (e.g., `http`, `ssh`, `ftp`)

---

## How It Works

1. Resolves the target hostname to an IP address using `socket.gethostbyname()`
2. Loops through ports 1–1024
3. For each port, attempts a **TCP connection** using `socket.connect_ex()`
4. If the connection returns `0` (success) → port is **OPEN**
5. Looks up the service name via `socket.getservbyport()`

---

## Usage

```bash
# Scan default target (scanme.nmap.org) ports 1-1024
python3 port_scanner_v1.py

# Scan a specific target
python3 port_scanner_v1.py scanme.nmap.org

# Scan a custom port range
python3 port_scanner_v1.py scanme.nmap.org 1 500
```

### Example Output

```
=======================================================
  Port Scanner v1.0 — by Nivedhitha KS
=======================================================
  Target   : scanme.nmap.org (45.33.32.156)
  Range    : 1 – 1024
  Started  : 2025-06-01 10:45:02
=======================================================
  [OPEN] Port 22     —  ssh
  [OPEN] Port 80     —  http

=======================================================
  Scan complete. 2 open port(s) found.
  Finished : 2025-06-01 10:46:18
=======================================================
```

---

## Requirements

- Python 3.x
- No external libraries — uses only the built-in `socket` module

---

## ⚠️ Legal & Ethical Use

> Only scan hosts you own or have **explicit written permission** to scan.  
> Unauthorized port scanning may be illegal in your jurisdiction.  
> The default test target `scanme.nmap.org` is provided by the Nmap project and is **legal to scan**.

---

## What's Next (v2.0 Ideas)

- [ ] Multi-threading for faster scans
- [ ] Banner grabbing (identify software versions)
- [ ] UDP port scanning
- [ ] Export results to CSV/JSON
- [ ] Integrate with Nmap via `python-nmap` library

---

## Author

**Nivedhitha KS** — 60-Day Cybersecurity Journey  
🔗 [GitHub](https://github.com/NivedhithaKS-SEC/cybersec-journey)  
📅 Built on Day 5 of 60
