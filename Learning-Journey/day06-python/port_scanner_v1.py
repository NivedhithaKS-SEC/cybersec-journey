#!/usr/bin/env python3
"""
Port Scanner v1.0
Author: Nivedhitha KS
GitHub: github.com/NivedhithaKS-SEC/cybersec-journey
Day 5 of 60-Day Cybersecurity Journey

Scans a target host for open TCP ports in range 1-1024.
Displays service names where known.
"""

import socket
import sys
from datetime import datetime


def get_service(port):
    """Return the common service name for a given port number."""
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"


def scan_port(target_ip, port, timeout=0.5):
    """
    Attempt a TCP connection to target_ip:port.
    Returns True if port is open, False otherwise.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target_ip, port))
        sock.close()
        return result == 0
    except socket.error:
        return False


def resolve_target(target):
    """Resolve hostname to IP address."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[ERROR] Cannot resolve hostname: {target}")
        sys.exit(1)


def scan_range(target, start_port=1, end_port=1024):
    """
    Scan all ports from start_port to end_port on the target.
    Prints open ports with service names.
    """
    target_ip = resolve_target(target)

    print("=" * 55)
    print(f"  Port Scanner v1.0 — by Nivedhitha KS")
    print("=" * 55)
    print(f"  Target   : {target} ({target_ip})")
    print(f"  Range    : {start_port} – {end_port}")
    print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    open_ports = []

    for port in range(start_port, end_port + 1):
        # Simple progress indicator every 100 ports
        if port % 100 == 0:
            print(f"  [~] Scanning port {port}...", end="\r")

        if scan_port(target_ip, port):
            service = get_service(port)
            open_ports.append((port, service))
            print(f"  [OPEN] Port {port:<6} —  {service}")

    print()
    print("=" * 55)
    print(f"  Scan complete. {len(open_ports)} open port(s) found.")
    print(f"  Finished : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    return open_ports


def main():
    # Default safe target for testing (legal to scan)
    if len(sys.argv) == 1:
        target = "scanme.nmap.org"
        print(f"[INFO] No target given. Using default: {target}")
    elif len(sys.argv) == 2:
        target = sys.argv[1]
    elif len(sys.argv) == 4:
        target = sys.argv[1]
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        scan_range(target, start, end)
        return
    else:
        print("Usage: python3 port_scanner_v1.py <target> [start_port] [end_port]")
        print("Example: python3 port_scanner_v1.py scanme.nmap.org 1 1024")
        sys.exit(1)

    scan_range(target)


if __name__ == "__main__":
    main()
