# Day 10 — Python Exception Handling
# Security scripts need to handle errors gracefully

import requests

# ============================================
# PROGRAM 1: Basic try/except
# ============================================
print("=" * 50)
print("PROGRAM 1: Basic Exception Handling")
print("=" * 50)

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Error caught: Cannot divide by zero!")

try:
    number = int("not_a_number")
except ValueError as e:
    print(f"Error caught: {e}")

print("Script continues after errors — no crash!")

# ============================================
# PROGRAM 2: Robust URL Fetcher with errors
# ============================================
print("\n" + "=" * 50)
print("PROGRAM 2: Robust Site Checker")
print("=" * 50)

sites = [
    "https://google.com",
    "https://tryhackme.com",
    "https://thissitedoesnotexist12345.com",
    "https://github.com"
]

for site in sites:
    try:
        response = requests.get(site, timeout=5)
        print(f"✅ {site:40} Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ {site:40} OFFLINE or unreachable")
    except requests.exceptions.Timeout:
        print(f"⚠️  {site:40} TIMEOUT after 5 seconds")
    except requests.exceptions.RequestException as e:
        print(f"❌ {site:40} Error: {e}")

# ============================================
# PROGRAM 3: Safe Security Header Checker
# ============================================
print("\n" + "=" * 50)
print("PROGRAM 3: Safe Security Header Checker")
print("=" * 50)

def check_security_headers(url):
    security_headers = [
        "X-Frame-Options",
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-XSS-Protection"
    ]
    try:
        response = requests.get(url, timeout=5)
        print(f"\nTarget: {url}")
        print(f"Status: {response.status_code}")
        print("-" * 40)
        for header in security_headers:
            if header in response.headers:
                print(f"✅ {header}: Present")
            else:
                print(f"❌ {header}: MISSING — vulnerability!")
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {url}")
    except requests.exceptions.Timeout:
        print(f"⚠️  {url} timed out")
    except Exception as e:
        print(f"Unexpected error: {e}")

check_security_headers("https://github.com")
check_security_headers("https://httpbin.org")

print("\n✅ Day 10 Python Complete!")