#!/usr/bin/env python3
"""
PCAP Analyzer — Day 12
Author: Nivedhitha K.S
GitHub: github.com/NivedhithaKS-SEC

Analyzes network packet data to find:
- Suspicious IP addresses
- HTTP login attempts  
- DNS queries
- Credential exposure

NOTE: Full PCAP parsing requires scapy + a .pcap file (run on Kali).
This Windows demo shows the analysis logic using simulated packet data.
"""

import re
from collections import Counter
from datetime import datetime

def print_banner():
    print("""
╔══════════════════════════════════════════════╗
║         PCAP ANALYZER v1.0                   ║
║         Day 12 — Network Sniffing            ║
║         Author: Nivedhitha K.S               ║
╚══════════════════════════════════════════════╝
    """)

# ============================================
# SIMULATED PACKET DATA
# (Real version reads from .pcap file using scapy)
# ============================================
SIMULATED_PACKETS = [
    {"src": "192.168.1.9",  "dst": "8.8.8.8",         "proto": "DNS",  "data": "query: google.com"},
    {"src": "192.168.1.9",  "dst": "8.8.8.8",         "proto": "DNS",  "data": "query: tryhackme.com"},
    {"src": "192.168.1.9",  "dst": "142.251.221.163",  "proto": "HTTP", "data": "GET /index.html HTTP/1.1"},
    {"src": "192.168.1.9",  "dst": "127.0.0.1",        "proto": "HTTP", "data": "POST /login.php HTTP/1.1\nusername=admin&password=password123"},
    {"src": "192.168.1.9",  "dst": "192.168.1.1",      "proto": "TCP",  "data": "SYN port 80"},
    {"src": "10.0.0.5",     "dst": "192.168.1.9",      "proto": "TCP",  "data": "SYN port 22"},
    {"src": "10.0.0.5",     "dst": "192.168.1.9",      "proto": "TCP",  "data": "SYN port 23"},
    {"src": "10.0.0.5",     "dst": "192.168.1.9",      "proto": "TCP",  "data": "SYN port 3389"},
    {"src": "10.0.0.5",     "dst": "192.168.1.9",      "proto": "TCP",  "data": "SYN port 8080"},
    {"src": "172.16.0.100", "dst": "192.168.1.9",      "proto": "HTTP", "data": "POST /admin HTTP/1.1\nusername=root&password=toor"},
    {"src": "192.168.1.9",  "dst": "8.8.8.8",         "proto": "DNS",  "data": "query: malware-c2-server.ru"},
    {"src": "192.168.1.9",  "dst": "185.220.101.45",   "proto": "TCP",  "data": "Connection to Tor exit node"},
    {"src": "192.168.1.9",  "dst": "8.8.8.8",         "proto": "DNS",  "data": "query: github.com"},
    {"src": "192.168.1.9",  "dst": "8.8.8.8",         "proto": "DNS",  "data": "query: shodan.io"},
]

SUSPICIOUS_DOMAINS = ["malware", "c2", "botnet", "ransomware", ".ru", ".tk", ".pw", "tor"]
CRED_KEYWORDS = ["username", "password", "passwd", "login", "user", "pass"]

# ============================================
# ANALYSIS 1: IP Statistics
# ============================================
def analyze_ips(packets):
    print("=" * 55)
    print("📊 IP ADDRESS ANALYSIS")
    print("=" * 55)
    
    src_ips = [p["src"] for p in packets]
    ip_counts = Counter(src_ips).most_common(5)
    
    print("\n  Top Source IPs:")
    for ip, count in ip_counts:
        bar = "█" * count
        print(f"  {ip:18} → {count:2} packets  {bar}")

# ============================================
# ANALYSIS 2: DNS Queries
# ============================================
def analyze_dns(packets):
    print("\n" + "=" * 55)
    print("🌐 DNS QUERY ANALYSIS")
    print("=" * 55)
    
    dns_packets = [p for p in packets if p["proto"] == "DNS"]
    print(f"\n  Total DNS queries: {len(dns_packets)}\n")
    
    for pkt in dns_packets:
        domain = pkt["data"].replace("query: ", "")
        is_suspicious = any(s in domain.lower() for s in SUSPICIOUS_DOMAINS)
        
        if is_suspicious:
            print(f"  ⚠️  SUSPICIOUS: {domain}")
        else:
            print(f"  ✅ Normal:     {domain}")

# ============================================
# ANALYSIS 3: HTTP Credentials
# ============================================
def analyze_credentials(packets):
    print("\n" + "=" * 55)
    print("🔑 CREDENTIAL EXPOSURE ANALYSIS")
    print("=" * 55)
    
    found = False
    for pkt in packets:
        if pkt["proto"] == "HTTP" and "POST" in pkt["data"]:
            for keyword in CRED_KEYWORDS:
                if keyword.lower() in pkt["data"].lower():
                    print(f"\n  ⚠️  CREDENTIALS IN PLAIN TEXT!")
                    print(f"  Source IP : {pkt['src']}")
                    print(f"  Dest IP   : {pkt['dst']}")
                    
                    # Extract and show credentials
                    lines = pkt["data"].split("\n")
                    for line in lines:
                        if any(k in line.lower() for k in CRED_KEYWORDS):
                            print(f"  Data      : {line}")
                    print(f"  Risk      : HIGH — Password visible in plain text!")
                    found = True
                    break
    
    if not found:
        print("\n  ✅ No credentials found in plain text")

# ============================================
# ANALYSIS 4: Port Scan Detection
# ============================================
def detect_port_scan(packets):
    print("\n" + "=" * 55)
    print("🔍 PORT SCAN DETECTION")
    print("=" * 55)
    
    syn_by_src = {}
    for pkt in packets:
        if pkt["proto"] == "TCP" and "SYN" in pkt["data"]:
            src = pkt["src"]
            if src not in syn_by_src:
                syn_by_src[src] = []
            syn_by_src[src].append(pkt["data"])
    
    print()
    for src, syns in syn_by_src.items():
        if len(syns) >= 3:
            print(f"  ⚠️  POSSIBLE PORT SCAN from {src}")
            print(f"      {len(syns)} SYN packets sent")
            for s in syns:
                print(f"      → {s}")
        else:
            print(f"  ✅ Normal traffic from {src} ({len(syns)} connections)")

# ============================================
# SUMMARY
# ============================================
def print_summary(packets):
    print("\n" + "=" * 55)
    print("📋 ANALYSIS SUMMARY")
    print("=" * 55)
    
    dns_count = sum(1 for p in packets if p["proto"] == "DNS")
    http_count = sum(1 for p in packets if p["proto"] == "HTTP")
    tcp_count = sum(1 for p in packets if p["proto"] == "TCP")
    cred_count = sum(1 for p in packets if "POST" in p["data"] 
                     and any(k in p["data"].lower() for k in CRED_KEYWORDS))
    suspicious_dns = sum(1 for p in packets if p["proto"] == "DNS" 
                         and any(s in p["data"].lower() for s in SUSPICIOUS_DOMAINS))
    
    print(f"""
  Total packets analyzed  : {len(packets)}
  DNS queries             : {dns_count}
  HTTP requests           : {http_count}
  TCP connections         : {tcp_count}
  Credentials exposed     : {'⚠️  YES - ' + str(cred_count) + ' found!' if cred_count else '✅ None'}
  Suspicious DNS queries  : {'⚠️  YES - ' + str(suspicious_dns) + ' found!' if suspicious_dns else '✅ None'}
  Scan completed          : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)
    print("=" * 55)
    print("✅ Analysis Complete!")
    print("=" * 55)

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    print_banner()
    print("  📦 Loading packet data...")
    print(f"  📊 Analyzing {len(SIMULATED_PACKETS)} packets\n")
    
    analyze_ips(SIMULATED_PACKETS)
    analyze_dns(SIMULATED_PACKETS)
    analyze_credentials(SIMULATED_PACKETS)
    detect_port_scan(SIMULATED_PACKETS)
    print_summary(SIMULATED_PACKETS)
