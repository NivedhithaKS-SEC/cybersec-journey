# Bonus: Simple port checker using loops
# Cybersecurity context — understand what nmap does internally

import socket

print("\n=== Simple Port Scanner ===")
target = "127.0.0.1"
common_ports = [21, 22, 23, 25, 53, 80, 443, 3306, 3389, 8080]

for port in common_ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))
    if result == 0:
        print(f"Port {port} — OPEN")
    else:
        print(f"Port {port} — closed")
    sock.close()