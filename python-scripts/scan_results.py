# ============================================================
# Day 6 Python — scan_results.py
# Topic: Lists and Dictionaries
# Author: Nivedhitha KS
# GitHub: github.com/NivedhithaKS-SEC/cybersec-journey
# ============================================================

# ============================================================
# PART 1: LISTS — Storing open ports
# ============================================================

open_ports = [21, 22, 23, 25, 80, 139, 445, 1524, 3306, 5432, 5900, 6667, 8180]

print("=" * 50)
print("         OPEN PORTS ON TARGET")
print("=" * 50)

for port in open_ports:
    print(f"  [+] Port {port} is OPEN")

print(f"\n  Total open ports found: {len(open_ports)}")

# List operations
open_ports.append(8080)           # Add a new port
open_ports.remove(8080)           # Remove it
print(f"  First port: {open_ports[0]}")
print(f"  Last port:  {open_ports[-1]}")
print(f"  Is port 21 in list? {21 in open_ports}")


# ============================================================
# PART 2: DICTIONARIES — Storing host information
# ============================================================

host_info = {
    "ip":           "192.168.1.8",
    "hostname":     "metasploitable",
    "os":           "Linux 2.6.24-16-server (Ubuntu 8.04)",
    "open_ports":   open_ports,
    "exploited":    True,
    "access_level": "root (uid=0)",
    "cve":          "CVE-2011-2523"
}

print("\n" + "=" * 50)
print("         HOST INFORMATION")
print("=" * 50)

for key, value in host_info.items():
    print(f"  {key:<15}: {value}")


# ============================================================
# PART 3: NESTED DICTIONARIES — Multiple hosts
# ============================================================

scan_results = {
    "192.168.1.7": {
        "hostname":        "kali",
        "os":              "Kali Linux 2025.1c",
        "open_ports":      [],
        "vulnerabilities": [],
        "exploited":       False,
        "access_level":    "N/A (attacker machine)"
    },
    "192.168.1.8": {
        "hostname":        "metasploitable",
        "os":              "Linux 2.6.24 (Ubuntu 8.04)",
        "open_ports":      [21, 22, 80, 139, 445, 1524, 3306],
        "vulnerabilities": ["CVE-2011-2523", "CVE-2007-2447"],
        "exploited":       True,
        "access_level":    "root (uid=0)"
    }
}


# ============================================================
# PART 4: FUNCTIONS — Print a clean report
# ============================================================

def print_scan_report(results):
    print("\n" + "=" * 50)
    print("         FULL SCAN REPORT")
    print("=" * 50)
    for ip, data in results.items():
        print(f"\n  Host     : {ip} ({data['hostname']})")
        print(f"  OS       : {data['os']}")
        print(f"  Ports    : {data['open_ports']}")
        print(f"  Vulns    : {len(data['vulnerabilities'])} found")
        if data['vulnerabilities']:
            for v in data['vulnerabilities']:
                print(f"             - {v}")
        status = "YES ⚠️  — " + data['access_level'] if data['exploited'] else "No"
        print(f"  Exploited: {status}")
        print("  " + "-" * 44)


def add_host(results, ip, hostname, os, ports):
    results[ip] = {
        "hostname":        hostname,
        "os":              os,
        "open_ports":      ports,
        "vulnerabilities": [],
        "exploited":       False,
        "access_level":    "none"
    }
    print(f"\n  [+] Host {ip} ({hostname}) added to scan results.")


def get_exploited_hosts(results):
    print("\n" + "=" * 50)
    print("  EXPLOITED HOSTS SUMMARY")
    print("=" * 50)
    found = False
    for ip, data in results.items():
        if data['exploited']:
            print(f"  [PWNED] {ip} ({data['hostname']}) — {data['access_level']}")
            found = True
    if not found:
        print("  No hosts exploited yet.")


# ============================================================
# PART 5: RUN EVERYTHING
# ============================================================

print_scan_report(scan_results)

add_host(scan_results, "10.0.0.5", "webserver", "Ubuntu 20.04", [80, 443])

print_scan_report(scan_results)

get_exploited_hosts(scan_results)

print("\n" + "=" * 50)
print("  Script complete! Push to GitHub.")
print("=" * 50)
