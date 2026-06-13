# ============================================
# DAY 2 PYTHON PROGRAMS — Security Concepts
# Nivedhitha KS | 60-Day Cybersecurity Journey
# ============================================

# ==========================================
# PROGRAM 1: Data Types Explorer
# ==========================================
print("=" * 50)
print("PROGRAM 1: Data Types in Python")
print("=" * 50)

# String
target_name = "Metasploitable2"
print(f"Target Name (string): {target_name}")

# Integer
open_ports = 5
print(f"Open Ports Found (int): {open_ports}")

# Float
risk_score = 8.7
print(f"Risk Score (float): {risk_score}")

# Boolean
is_vulnerable = True
print(f"Is Vulnerable (boolean): {is_vulnerable}")

# List
vulnerabilities = ["SQL Injection", "XSS", "RCE", "Buffer Overflow"]
print(f"Vulnerabilities Found (list): {vulnerabilities}")
print(f"First Vulnerability: {vulnerabilities[0]}")

# Dictionary
target_info = {
    "ip": "192.168.1.1",
    "os": "Linux",
    "open_ports": [22, 80, 443],
    "risk": "HIGH"
}
print(f"\nTarget Info (dictionary):")
for key, value in target_info.items():
    print(f"  {key}: {value}")

input("\nPress Enter to continue to Program 2...")


# ==========================================
# PROGRAM 2: Port Risk Checker
# ==========================================
print("\n" + "=" * 50)
print("PROGRAM 2: Port Risk Checker")
print("=" * 50)

ports = [21, 22, 80, 443, 3389, 8080]

port_info = {
    21:   ("FTP",   "HIGH RISK — Plaintext, no encryption"),
    22:   ("SSH",   "SECURE — Encrypted remote access"),
    80:   ("HTTP",  "MEDIUM RISK — Unencrypted web traffic"),
    443:  ("HTTPS", "SECURE — Encrypted web traffic"),
    3389: ("RDP",   "CRITICAL RISK — Common attack target"),
    8080: ("HTTP Alt", "MEDIUM RISK — Often used for testing")
}

print(f"\nScanning {len(ports)} ports...\n")
for port in ports:
    service, risk = port_info[port]
    print(f"Port {port:5} | {service:8} | {risk}")

input("\nPress Enter to continue to Program 3...")


# ==========================================
# PROGRAM 3: Password Strength Checker
# ==========================================
print("\n" + "=" * 50)
print("PROGRAM 3: Password Strength Checker")
print("=" * 50)

import string

def check_password(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short — use at least 8 characters")

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters (A-Z)")

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters (a-z)")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers (0-9)")

    special = "!@#$%^&*"
    if any(c in special for c in password):
        score += 1
    else:
        feedback.append("Add special characters (!@#$%^&*)")

    if score <= 2:
        strength = "WEAK ❌"
    elif score <= 4:
        strength = "MEDIUM ⚠️"
    else:
        strength = "STRONG ✅"

    return score, strength, feedback

passwords = ["abc", "password123", "P@ssw0rd!", "X#9kL$mN2@qR"]

for pwd in passwords:
    score, strength, feedback = check_password(pwd)
    print(f"\nPassword : {pwd}")
    print(f"Score    : {score}/5")
    print(f"Strength : {strength}")
    if feedback:
        print(f"Improve  : {', '.join(feedback)}")

input("\nPress Enter to continue to Program 4...")


# ==========================================
# PROGRAM 4: IP Address Validator
# ==========================================
print("\n" + "=" * 50)
print("PROGRAM 4: IP Address Validator")
print("=" * 50)

def validate_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        if not (0 <= int(part) <= 255):
            return False
    return True

ip_list = ["192.168.1.1", "10.0.0.256", "172.16.0.1", "999.1.1.1", "8.8.8.8"]

print()
for ip in ip_list:
    result = validate_ip(ip)
    status = "VALID ✅" if result else "INVALID ❌"
    print(f"IP: {ip:16} → {status}")

input("\nPress Enter to continue to Program 5...")


# ==========================================
# PROGRAM 5: Simple Recon Report Generator
# ==========================================
print("\n" + "=" * 50)
print("PROGRAM 5: Recon Report Generator")
print("=" * 50)

target = {
    "name": "TestServer-01",
    "ip": "192.168.1.105",
    "open_ports": [22, 80, 443, 8080],
    "os": "Ubuntu 20.04",
    "vulnerabilities": ["Outdated SSH version", "HTTP not redirecting to HTTPS"],
    "risk_level": "MEDIUM"
}

print(f"""
╔══════════════════════════════════════╗
║         RECON REPORT SUMMARY        ║
╚══════════════════════════════════════╝
Target Name  : {target['name']}
IP Address   : {target['ip']}
OS Detected  : {target['os']}
Open Ports   : {target['open_ports']}
Risk Level   : {target['risk_level']}

Vulnerabilities Found ({len(target['vulnerabilities'])}):""")

for i, vuln in enumerate(target['vulnerabilities'], 1):
    print(f"  {i}. {vuln}")

print("\n[Report Generated Successfully]")
print("=" * 50)
print("\n✅ All 5 Programs Complete! Great work Nivedhitha!")