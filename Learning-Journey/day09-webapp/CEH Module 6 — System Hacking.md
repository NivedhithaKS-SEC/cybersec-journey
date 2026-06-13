# CEH Module 6 — System Hacking

## 4 Stages of System Hacking
1. Gaining Access — cracking passwords, exploiting vulnerabilities
2. Escalating Privileges — moving from user → admin → root
3. Maintaining Access — backdoors, rootkits
4. Clearing Logs — removing evidence

## Password Cracking Types
- Dictionary Attack — tries words from a wordlist (rockyou.txt)
- Brute Force — tries every possible combination
- Rainbow Table — uses pre-computed hash lookups
- Credential Stuffing — uses leaked username/password combos

## Tools Used
- John the Ripper — password cracking
- Hashcat — GPU-based cracking (faster)
- Hydra — online brute force (SSH, FTP, HTTP)
- Mimikatz — dumps Windows credentials from memory

## Privilege Escalation
- Horizontal — user A accessing user B's data (same level)
- Vertical — user → admin (moving up levels)

## Common PrivEsc Techniques
- SUID binaries (Linux) — files that run as root
- Misconfigured sudo — sudo -l shows what you can run
- Kernel exploits — old kernels have known vulns
- Weak service permissions (Windows)

## Maintaining Access
- Backdoor — hidden entry point left by attacker
- Rootkit — hides malware from the OS itself
- Netcat listener — simple reverse shell

## Clearing Tracks
- Clear bash history: history -c
- Delete log files: /var/log/auth.log
- Timestomping — changing file timestamps