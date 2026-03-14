# Day 9 — Python requests library
# Fetching web pages like a security tool

import requests

# ============================================
# PROGRAM 1: Basic URL Fetch
# ============================================
print("=" * 50)
print("PROGRAM 1: Fetch a URL")
print("=" * 50)

url = "http://httpbin.org/get"
response = requests.get(url)

print(f"URL: {url}")
print(f"Status Code: {response.status_code}")
print(f"Response Time: {response.elapsed.total_seconds()} seconds")

if response.status_code == 200:
    print("✅ Site is UP")
else:
    print("❌ Site returned an error")

# ============================================
# PROGRAM 2: Check Multiple Sites
# ============================================
print("\n" + "=" * 50)
print("PROGRAM 2: Site Status Checker")
print("=" * 50)

sites = [
    "https://google.com",
    "https://github.com",
    "https://tryhackme.com",
    "https://portswigger.net"
]

for site in sites:
    try:
        r = requests.get(site, timeout=5)
        print(f"{site:35} → Status: {r.status_code} ✅")
    except requests.exceptions.ConnectionError:
        print(f"{site:35} → OFFLINE ❌")
    except requests.exceptions.Timeout:
        print(f"{site:35} → TIMEOUT ⚠️")

# ============================================
# PROGRAM 3: Read Response Headers (Recon)
# ============================================
print("\n" + "=" * 50)
print("PROGRAM 3: Header Recon (like a hacker)")
print("=" * 50)

target = "https://httpbin.org"
r = requests.get(target)

print(f"\nHeaders from {target}:")
for header, value in r.headers.items():
    print(f"  {header}: {value}")

print("\n🔍 Security-relevant headers to look for:")
security_headers = ["Server", "X-Powered-By", "X-Frame-Options", 
                    "Content-Security-Policy", "Strict-Transport-Security"]

for h in security_headers:
    if h in r.headers:
        print(f"  ✅ {h}: {r.headers[h]}")
    else:
        print(f"  ❌ {h}: MISSING (potential vulnerability)")

print("\n✅ Day 9 Python Complete!")