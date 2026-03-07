# ================================================
# DAY 1 PYTHON CONCEPTS - Nivedhitha KS
# Run this file by clicking the ▶ button in VS Code
# ================================================

# ── CONCEPT 1: VARIABLES ──────────────────────────
name = "Alice"           # string (text)
age = 25                 # integer (whole number)
score = 98.5             # float (decimal number)
is_hacker = True         # boolean (True or False)

print("---- VARIABLES ----")
print(name)
print(age)
print(score)
print(is_hacker)

# ── CONCEPT 2: PRINT FORMATTING ───────────────────
print("\n---- PRINT FORMATTING ----")
print(f"Hello, my name is {name} and I am {age} years old.")
print(f"My score is {score} and hacker status: {is_hacker}")

# ── CONCEPT 3: USER INPUT ─────────────────────────
print("\n---- USER INPUT ----")
target_ip = input("Enter a target IP to scan: ")
print(f"You entered: {target_ip}")
print(f"Now scanning {target_ip}... (pretend scan!)")

# ── CONCEPT 4: LISTS ──────────────────────────────
print("\n---- LISTS ----")
open_ports = [22, 80, 443, 8080]
print("All open ports:", open_ports)
print("First port:", open_ports[0])
print("Last port:", open_ports[-1])
print("Total ports found:", len(open_ports))

# ── CONCEPT 5: DICTIONARIES ───────────────────────
print("\n---- DICTIONARIES ----")
scan_result = {
    "ip": "192.168.1.1",
    "port": 80,
    "service": "http",
    "status": "open"
}
print("Full scan result:", scan_result)
print("IP address:", scan_result["ip"])
print("Service running:", scan_result["service"])

# ── CONCEPT 6: IF/ELSE ────────────────────────────
print("\n---- IF/ELSE ----")
port = 22
if port == 22:
    print(f"Port {port} is SSH - possible brute force target!")
elif port == 80:
    print(f"Port {port} is HTTP - check for web vulnerabilities")
else:
    print(f"Port {port} - unknown service, investigate further")

# ── DONE ──────────────────────────────────────────
print("\n✅ Day 1 Python concepts complete!")
print("Push this file to GitHub now.")
