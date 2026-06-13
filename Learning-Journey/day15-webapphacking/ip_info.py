#!/usr/bin/env python3
"""
IP Geolocation & Info Tool
===========================
Author  : Nivedhitha KS
Day     : 15 of 60-Day Cybersecurity Journey
GitHub  : github.com/NivedhithaKS-SEC/cybersec-journey
Purpose : Fetch geolocation, ASN, and network info for any IP using
          free ipapi.co API. Demonstrates JSON parsing and API calls.

Usage:
    python3 ip_info.py                    # Defaults to 8.8.8.8
    python3 ip_info.py 1.1.1.1           # Single IP
    python3 ip_info.py -f ips.txt        # Batch from file
    python3 ip_info.py -o results.json   # Save output to JSON

Requirements:
    pip install requests
"""

import requests
import json
import sys
import argparse
import os
from datetime import datetime


# ─────────────────────────────────────────────
# JSON LEARNING NOTES (read before the code)
# ─────────────────────────────────────────────
# JSON (JavaScript Object Notation) is the universal format for API data.
#
# JSON types → Python types:
#   JSON object  {}   →  Python dict   {}
#   JSON array   []   →  Python list   []
#   JSON string  ""   →  Python str    ""
#   JSON number       →  Python int / float
#   JSON true/false   →  Python True / False
#   JSON null         →  Python None
#
# Core operations:
#   json.loads(string)  → parse JSON string into Python object
#   json.dumps(obj)     → convert Python object to JSON string
#   json.load(file)     → read JSON from file object
#   json.dump(obj,file) → write JSON to file object
#
# Example:
#   raw = '{"ip": "8.8.8.8", "country": "US"}'
#   data = json.loads(raw)         # → dict: {"ip": "8.8.8.8", ...}
#   print(data["ip"])              # → 8.8.8.8
#   print(data.get("city", "N/A")) # → N/A (safe access with default)
# ─────────────────────────────────────────────


def get_ip_info(ip_address: str, verbose: bool = False) -> dict:
    """
    Fetch geolocation and network info for an IP address.
    
    Uses ipapi.co free API (no key needed, 1000 requests/day).
    Returns a dictionary with all available fields.
    
    Args:
        ip_address: IPv4 or IPv6 address string
        verbose:    Print raw JSON response if True
    
    Returns:
        Dictionary with IP info, or empty dict on error
    """
    url = f"https://ipapi.co/{ip_address}/json/"
    
    headers = {
        "User-Agent": "cybersec-learning-tool/1.0"
    }
    
    try:
        # Make the HTTP GET request
        response = requests.get(url, headers=headers, timeout=10)
        
        # Raise exception for HTTP errors (4xx, 5xx)
        response.raise_for_status()
        
        # Parse JSON response → Python dictionary
        # response.json() is equivalent to json.loads(response.text)
        data = response.json()
        
        if verbose:
            print("\n[RAW JSON RESPONSE]")
            print(json.dumps(data, indent=2))  # Pretty-print the raw data
        
        return data
    
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to API. Check internet connection.")
        return {}
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timed out for {ip_address}")
        return {}
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP error: {e}")
        return {}
    except json.JSONDecodeError:
        print(f"[ERROR] Could not parse API response as JSON")
        return {}


def print_ip_report(data: dict) -> None:
    """
    Print a formatted report from IP data dictionary.
    Uses dict.get(key, default) for safe access — 
    if a key doesn't exist, returns the default instead of crashing.
    """
    if not data:
        print("No data to display.")
        return
    
    # Check for API error (e.g., private IP, invalid IP)
    if data.get("error"):
        print(f"[API ERROR] {data.get('reason', 'Unknown error')}")
        return
    
    ip = data.get("ip", "Unknown")
    
    print(f"\n{'='*50}")
    print(f"  IP Information Report: {ip}")
    print(f"{'='*50}")
    
    # Geographic information
    print(f"\n[LOCATION]")
    print(f"  Country      : {data.get('country_name', 'N/A')} ({data.get('country', 'N/A')})")
    print(f"  Region       : {data.get('region', 'N/A')} ({data.get('region_code', 'N/A')})")
    print(f"  City         : {data.get('city', 'N/A')}")
    print(f"  Postal code  : {data.get('postal', 'N/A')}")
    print(f"  Latitude     : {data.get('latitude', 'N/A')}")
    print(f"  Longitude    : {data.get('longitude', 'N/A')}")
    print(f"  Timezone     : {data.get('timezone', 'N/A')} (UTC{data.get('utc_offset', '')})")
    
    # Network / ASN information
    print(f"\n[NETWORK]")
    print(f"  ISP / Org    : {data.get('org', 'N/A')}")
    print(f"  ASN          : {data.get('asn', 'N/A')}")
    print(f"  Currency     : {data.get('currency_name', 'N/A')} ({data.get('currency', 'N/A')})")
    print(f"  Languages    : {data.get('languages', 'N/A')}")
    
    print(f"\n{'='*50}\n")


def save_results(results: list, output_file: str) -> None:
    """
    Save a list of IP result dictionaries to a JSON file.
    Demonstrates json.dump() for writing JSON to a file.
    """
    output = {
        "generated_at": datetime.now().isoformat(),
        "tool": "ip_info.py - Day 15 Cybersecurity Journey",
        "count": len(results),
        "results": results
    }
    
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)    # indent=2 for pretty formatting
    
    print(f"[SAVED] Results written to: {output_file}")


def read_ips_from_file(filepath: str) -> list:
    """
    Read a list of IPs from a text file (one per line).
    Lines starting with # are treated as comments and skipped.
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return []
    
    ips = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                ips.append(line)
    
    return ips


def main():
    parser = argparse.ArgumentParser(
        description="IP Geolocation Tool — Day 15 Cybersecurity Journey",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ip_info.py                      Look up your own public IP
  python3 ip_info.py 8.8.8.8             Look up Google DNS
  python3 ip_info.py 1.1.1.1 -v         Verbose — shows raw JSON
  python3 ip_info.py -f ips.txt         Batch lookup from file
  python3 ip_info.py 8.8.8.8 -o out.json  Save to file
        """
    )
    
    parser.add_argument(
        "ip", 
        nargs="?", 
        default="8.8.8.8",
        help="IP address to look up (default: 8.8.8.8)"
    )
    parser.add_argument(
        "-f", "--file",
        help="Path to text file with one IP per line"
    )
    parser.add_argument(
        "-o", "--output",
        help="Save all results to this JSON file"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print raw JSON response"
    )
    
    args = parser.parse_args()
    
    # Build list of IPs to process
    if args.file:
        ip_list = read_ips_from_file(args.file)
        if not ip_list:
            print("No valid IPs found in file.")
            sys.exit(1)
        print(f"[INFO] Loaded {len(ip_list)} IPs from {args.file}")
    else:
        ip_list = [args.ip]
    
    all_results = []
    
    for ip in ip_list:
        print(f"\n[LOOKUP] Fetching info for: {ip}")
        data = get_ip_info(ip, verbose=args.verbose)
        
        if data:
            print_ip_report(data)
            all_results.append(data)
    
    # Save to file if requested
    if args.output and all_results:
        save_results(all_results, args.output)
    
    print(f"[DONE] Processed {len(all_results)} IP(s).")


if __name__ == "__main__":
    main()
