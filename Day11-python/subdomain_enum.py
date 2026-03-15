#!/usr/bin/env python3
"""
Subdomain Enumerator — Portfolio Project #1
Author: Nivedhitha K.S
GitHub: github.com/NivedhithaKS-SEC
Description: Discovers active subdomains of a target domain
             by testing common subdomain names from a wordlist.
"""

import requests
import sys
import os
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================
TIMEOUT = 5        # seconds to wait for response
FOUND = []         # store discovered subdomains

# ============================================
# BANNER
# ============================================
def print_banner():
    print("""
╔══════════════════════════════════════════════╗
║        SUBDOMAIN ENUMERATOR v1.0             ║
║        Portfolio Project #1                  ║
║        Author: Nivedhitha K.S                ║
╚══════════════════════════════════════════════╝
    """)

# ============================================
# CHECK A SINGLE SUBDOMAIN
# ============================================
def check_subdomain(subdomain, domain):
    url = f"http://{subdomain}.{domain}"
    url_https = f"https://{subdomain}.{domain}"
    
    for target_url in [url, url_https]:
        try:
            response = requests.get(target_url, timeout=TIMEOUT)
            if response.status_code < 400:
                print(f"  ✅ FOUND: {target_url} "
                      f"[Status: {response.status_code}]")
                FOUND.append(target_url)
                return True
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.RequestException:
            pass
    return False

# ============================================
# LOAD WORDLIST
# ============================================
def load_wordlist(filepath):
    if not os.path.exists(filepath):
        print(f"  ❌ Wordlist not found: {filepath}")
        sys.exit(1)
    with open(filepath, "r") as f:
        words = [line.strip() for line in f if line.strip()]
    print(f"  📋 Loaded {len(words)} subdomains from wordlist")
    return words

# ============================================
# SAVE RESULTS
# ============================================
def save_results(domain):
    if not FOUND:
        return
    filename = f"results_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(f"Subdomain Enumeration Results\n")
        f.write(f"Target: {domain}\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Found: {len(FOUND)} subdomains\n")
        f.write("=" * 40 + "\n")
        for url in FOUND:
            f.write(f"{url}\n")
    print(f"\n  💾 Results saved to: {filename}")

# ============================================
# MAIN SCANNER
# ============================================
def run_scan(domain, wordlist_path):
    print_banner()
    print(f"  🎯 Target Domain : {domain}")
    print(f"  📋 Wordlist      : {wordlist_path}")
    print(f"  ⏱️  Timeout       : {TIMEOUT}s per request")
    print(f"  🕐 Started       : {datetime.now().strftime('%H:%M:%S')}")
    print("\n" + "=" * 50)
    print("  Scanning subdomains...")
    print("=" * 50)

    subdomains = load_wordlist(wordlist_path)
    total = len(subdomains)

    for i, sub in enumerate(subdomains, 1):
        print(f"  [{i:3}/{total}] Testing: {sub}.{domain}",
              end="\r")
        check_subdomain(sub, domain)

    print("\n" + "=" * 50)
    print(f"  ✅ Scan Complete!")
    print(f"  🔍 Tested  : {total} subdomains")
    print(f"  🎯 Found   : {len(FOUND)} active subdomains")
    print("=" * 50)

    if FOUND:
        print("\n  📌 Active Subdomains Discovered:")
        for url in FOUND:
            print(f"     → {url}")
    else:
        print("\n  ℹ️  No active subdomains found.")

    save_results(domain)

# ============================================
# ENTRY POINT
# ============================================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  SUBDOMAIN ENUMERATOR — Portfolio Project #1")
    print("=" * 50)

    # Get target domain
    domain = input("\n  Enter target domain (e.g. example.com): ").strip()
    if not domain:
        print("  ❌ No domain entered. Exiting.")
        sys.exit(1)

    # Remove http/https if user typed it
    domain = domain.replace("https://", "").replace("http://", "").strip("/")

    wordlist = "wordlist.txt"
    run_scan(domain, wordlist)