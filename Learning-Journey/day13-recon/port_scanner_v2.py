#!/usr/bin/env python3
"""
Port Scanner v2.0 — Portfolio Project
Author: Nivedhitha K.S
GitHub: github.com/NivedhithaKS-SEC

Upgrades from v1.0:
- Command line arguments (argparse)
- Configurable port ranges
- Timeout control
- Output to file
- Service detection
- Scan summary report
"""

import socket
import argparse
import sys
import os
from datetime import datetime

# ============================================
# SERVICE NAMES
# ============================================
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet",
    25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    27017: "MongoDB"
}

RISK_LEVELS = {
    21: "HIGH — FTP sends credentials in plaintext",
    22: "LOW — SSH is encrypted",
    23: "CRITICAL — Telnet sends everything in plaintext",
    80: "MEDIUM — HTTP is unencrypted",
    443: "LOW — HTTPS is encrypted",
    3389: "HIGH — RDP is common attack target",
    445: "HIGH — SMB EternalBlue vulnerability",
    3306: "HIGH — Database should not be public",
    6379: "CRITICAL — Redis often has no auth by default",
    27017: "CRITICAL — MongoDB often has no auth"
}

# ============================================
# BANNER
# ============================================
def print_banner():
    print("""
╔══════════════════════════════════════════════╗
║         PORT SCANNER v2.0                    ║
║         Portfolio Project #1 (upgraded)      ║
║         Author: Nivedhitha K.S               ║
╚══════════════════════════════════════════════╝
    """)

# ============================================
# SCAN SINGLE PORT
# ============================================
def scan_port(host, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False

# ============================================
# GET SERVICE INFO
# ============================================
def get_service(port):
    if port in COMMON_SERVICES:
        return COMMON_SERVICES[port]
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

def get_risk(port):
    return RISK_LEVELS.get(port, "MEDIUM — Review if this should be public")

# ============================================
# MAIN SCANNER
# ============================================
def run_scan(args):
    print_banner()

    # Resolve hostname to IP
    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"  ❌ Cannot resolve host: {args.target}")
        sys.exit(1)

    print(f"  🎯 Target   : {args.target} ({ip})")
    print(f"  📋 Ports    : {args.start_port} — {args.end_port}")
    print(f"  ⏱️  Timeout  : {args.timeout}s per port")
    print(f"  🕐 Started  : {datetime.now().strftime('%H:%M:%S')}")

    if args.output:
        print(f"  💾 Output   : {args.output}")

    print("\n" + "=" * 55)
    print("  Scanning...")
    print("=" * 55 + "\n")

    open_ports = []
    total_ports = args.end_port - args.start_port + 1

    for port in range(args.start_port, args.end_port + 1):
        # Progress indicator
        print(f"  Scanning port {port}/{args.end_port}...", end="\r")

        if scan_port(args.target, port, args.timeout):
            service = get_service(port)
            risk = get_risk(port)
            open_ports.append((port, service, risk))
            print(f"  ✅ OPEN  Port {port:5} | {service:12} | {risk}")

    # ============================================
    # RESULTS
    # ============================================
    print("\n" + "=" * 55)
    print(f"  ✅ Scan Complete!")
    print(f"  🔍 Ports scanned : {total_ports}")
    print(f"  🎯 Open ports    : {len(open_ports)}")
    print(f"  🕐 Finished      : {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 55)

    if open_ports:
        print("\n  📌 OPEN PORTS SUMMARY:")
        print(f"  {'Port':<8} {'Service':<15} {'Risk'}")
        print("  " + "-" * 50)
        for port, service, risk in open_ports:
            print(f"  {port:<8} {service:<15} {risk[:40]}")

    # ============================================
    # SAVE TO FILE
    # ============================================
    if args.output and open_ports:
        with open(args.output, "w") as f:
            f.write(f"Port Scan Report\n")
            f.write(f"Target: {args.target} ({ip})\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Ports Scanned: {args.start_port}-{args.end_port}\n")
            f.write("=" * 40 + "\n")
            for port, service, risk in open_ports:
                f.write(f"Port {port} | {service} | {risk}\n")
        print(f"\n  💾 Results saved to: {args.output}")

    return open_ports

# ============================================
# ARGUMENT PARSER
# ============================================
def main():
    parser = argparse.ArgumentParser(
        description="Port Scanner v2.0 — by Nivedhitha K.S",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python port_scanner_v2.py scanme.nmap.org
  python port_scanner_v2.py 192.168.1.1 -p 1 1024
  python port_scanner_v2.py scanme.nmap.org -p 1 100 -t 2
  python port_scanner_v2.py scanme.nmap.org -o results.txt
        """
    )

    parser.add_argument(
        "target",
        help="Target hostname or IP address"
    )
    parser.add_argument(
        "-p", "--ports",
        nargs=2,
        type=int,
        metavar=("START", "END"),
        default=[1, 1024],
        dest="port_range",
        help="Port range to scan (default: 1-1024)"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=1.0,
        help="Timeout per port in seconds (default: 1.0)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Save results to file"
    )

    args = parser.parse_args()
    args.start_port = args.port_range[0]
    args.end_port = args.port_range[1]

    run_scan(args)

if __name__ == "__main__":
    main()