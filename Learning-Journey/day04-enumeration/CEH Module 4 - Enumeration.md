# CEH Module 4: ENUMERATION

## What is Enumeration?
Enumeration is Step 3 in the ethical hacking methodology. After scanning (Day 5), you now extract detailed information from discovered services — usernames, shares, group info, banners, DNS records.

## CEH EXAM TIP
Enumeration happens AFTER scanning. It requires an active connection to the target. This is often tested on CEH exams — know the order: Recon → Scanning → Enumeration → Gaining Access.
## Banner Grabbing
Capturing service banners to identify software version, OS, and configuration. Done via Telnet, Netcat, or Nmap NSE scripts. Two types: Active (connect directly) and Passive (sniff traffic).

## SNMP Enumeration
Simple Network Management Protocol. Port 161/UDP. If community string is "public" (default), attackers can dump network device info, running processes, open ports. Tool: snmpwalk.

## LDAP Enumeration
Lightweight Directory Access Protocol. Port 389. Used by Active Directory. Can reveal usernames, groups, org structure. Tool: ldapsearch.

## NetBIOS Enumeration
Port 137-139. Reveals Windows computer names, logged-in users, and shared resources. Tool: nbtstat (Windows) or nbtscan (Linux).

## DNS Enumeration
Zone transfers can expose all DNS records. Tools: dig, nslookup, fierce. A successful zone transfer = goldmine of subdomains and IPs.

## NFS / SMB Enumeration
Network File System (2049) and SMB (445) can expose shared folders. Tools: showmount, smbclient, enum4linux.