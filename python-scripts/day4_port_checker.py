# ============================================
# DAY 4 PYTHON — Functions + Port Checker
# Nivedhitha KS | 60-Day Cybersecurity Journey
# ============================================

import socket

# ==========================================
# PART 1: What is a Function?
# ==========================================
def greet_hacker(name):
    print(f"Welcome to the security lab, {name}!")

greet_hacker("Nivedhitha")


# ==========================================
# PART 2: Function with Return Value
# ==========================================
def calculate_risk(open_ports):
    if open_ports >= 10:
        return "CRITICAL"
    elif open_ports >= 5:
        return "HIGH"
    elif open_ports >= 2:
        return "MEDIUM"
    else:
        return "LOW"

print("\n--- Risk Calculator ---")
print(f"2 open ports → Risk: {calculate_risk(2)}")
print(f"5 open ports → Risk: {calculate_risk(5)}")
print(f"12 open ports → Risk: {calculate_risk(12)}")


# ==========================================
# PART 3: Port Checker Function
# ==========================================
def check_port(host, port, timeout=1):
    """
    Tries to connect to host:port
    Returns True if open, False if closed
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False


# ==========================================
# PART 4: Scan Multiple Ports Using Function
# ==========================================
def scan_target(host, ports):
    print(f"\n{'='*45}")
    print(f"  PORT SCAN REPORT")
    print(f"  Target: {host}")
    print(f"{'='*45}")

    open_count = 0
    for port in ports:
        is_open = check_port(host, port)
        status = "OPEN  ✅" if is_open else "CLOSED ❌"
        print(f"  Port {port:5} → {status}")
        if is_open:
            open_count += 1

    print(f"{'='*45}")
    print(f"  Open ports found: {open_count}/{len(ports)}")
    print(f"  Risk Level: {calculate_risk(open_count)}")
    print(f"{'='*45}")


# Scan localhost
common_ports = [21, 22, 23, 80, 443, 3306, 8080, 8443]
scan_target("127.0.0.1", common_ports)

# Scan official Nmap test server (safe and legal)
print("\nScanning public test target (scanme.nmap.org)...")
scan_target("scanme.nmap.org", [22, 80, 443])

print("\n✅ Day 4 Python Complete!")
