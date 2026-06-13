# Python JSON Notes — Day 15

**Author:** Nivedhitha KS | **Day:** 15 of 60  
**GitHub:** github.com/NivedhithaKS-SEC/cybersec-journey

---

## What is JSON?

JSON (JavaScript Object Notation) is the universal format for exchanging data between systems. Every API you will ever work with in security — Shodan, VirusTotal, HaveIBeenPwned, Censys, ipapi, HackerOne — returns data as JSON.

### JSON Syntax Rules
- Data is in key/value pairs: `"key": "value"`
- Objects are wrapped in `{}` curly braces
- Arrays are wrapped in `[]` square brackets
- Strings must use double quotes `"` (not single `'`)
- No trailing commas
- No comments

### JSON Example
```json
{
  "ip": "8.8.8.8",
  "country": "United States",
  "country_code": "US",
  "city": "Mountain View",
  "org": "AS15169 Google LLC",
  "latitude": 37.4056,
  "longitude": -122.0775,
  "timezone": "America/Los_Angeles",
  "is_vpn": false,
  "tags": ["dns", "google", "public"],
  "ports": [53, 443]
}
```

---

## JSON ↔ Python Type Mapping

| JSON type | Python type | Example |
|-----------|------------|---------|
| `{}` object | `dict` | `{"key": "value"}` |
| `[]` array | `list` | `["a", "b", "c"]` |
| `"string"` | `str` | `"hello"` |
| `123` number | `int` | `123` |
| `1.23` number | `float` | `1.23` |
| `true` / `false` | `True` / `False` | boolean |
| `null` | `None` | None |

---

## Core JSON Operations

### 1. Parse JSON string → Python object
```python
import json

json_string = '{"ip": "8.8.8.8", "country": "US", "port": 53}'

# json.loads() = "load string"
data = json.loads(json_string)

print(type(data))         # <class 'dict'>
print(data["ip"])         # 8.8.8.8
print(data["country"])    # US
print(data["port"])       # 53
```

### 2. Convert Python object → JSON string
```python
import json

my_dict = {
    "target": "192.168.1.1",
    "ports_open": [22, 80, 443],
    "has_ssl": True,
    "version": None
}

# json.dumps() = "dump string"
json_string = json.dumps(my_dict)
print(json_string)
# {"target": "192.168.1.1", "ports_open": [22, 80, 443], "has_ssl": true, "version": null}

# Pretty print with indentation
pretty = json.dumps(my_dict, indent=2)
print(pretty)
```

### 3. Read JSON from file
```python
import json

with open("scan_results.json", "r") as f:
    data = json.load(f)    # json.load() = "load from file"

print(data["target"])
```

### 4. Write JSON to file
```python
import json

results = {
    "scan_date": "2026-03-27",
    "target": "192.168.1.1",
    "findings": ["port 22 open", "port 80 open"]
}

with open("output.json", "w") as f:
    json.dump(results, f, indent=2)    # json.dump() = "dump to file"
```

---

## Safe Dictionary Access

When parsing API responses, keys may be missing. Always use `.get()` to avoid KeyError crashes:

```python
# UNSAFE — crashes if "city" key doesn't exist
print(data["city"])

# SAFE — returns "Unknown" if "city" key doesn't exist
print(data.get("city", "Unknown"))

# Nested access — safe way
country = data.get("location", {}).get("country", "N/A")
```

---

## Making API Calls with requests

### Basic GET request
```python
import requests
import json

# Make request
response = requests.get("https://ipapi.co/8.8.8.8/json/")

# Check status
print(response.status_code)    # 200 = OK

# Parse JSON — two equivalent ways:
data = response.json()              # Built-in method
data = json.loads(response.text)    # Manual parse

# Access fields
print(data.get("country_name"))
print(data.get("org"))
```

### HTTP Status Codes to know
| Code | Meaning |
|------|---------|
| 200 | OK — success |
| 201 | Created |
| 301/302 | Redirect |
| 400 | Bad Request — your fault |
| 401 | Unauthorised — need auth |
| 403 | Forbidden — no permission |
| 404 | Not Found |
| 429 | Too Many Requests — rate limited |
| 500 | Server Error — their fault |

### Error Handling
```python
import requests

try:
    response = requests.get("https://api.example.com/data", timeout=10)
    response.raise_for_status()   # Raises exception for 4xx/5xx
    data = response.json()
    
except requests.exceptions.ConnectionError:
    print("Cannot connect — check internet or URL")
    
except requests.exceptions.Timeout:
    print("Request timed out")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    # e.g., "404 Client Error: Not Found"
    
except requests.exceptions.RequestException as e:
    print(f"General request error: {e}")
    
except ValueError:    # json.JSONDecodeError
    print("Response is not valid JSON")
```

---

## Real-World Security API Examples

### Shodan API (requires free key)
```python
import requests

API_KEY = "your_shodan_api_key"
ip = "8.8.8.8"

url = f"https://api.shodan.io/shodan/host/{ip}?key={API_KEY}"
response = requests.get(url)
data = response.json()

print(f"Hostnames: {data.get('hostnames', [])}")
print(f"Open ports: {data.get('ports', [])}")
print(f"OS: {data.get('os', 'Unknown')}")
print(f"Vulns: {data.get('vulns', {})}")
```

### HaveIBeenPwned API (free, no key for basic)
```python
import requests
import hashlib

def check_password_pwned(password):
    """Check if a password appears in known data breaches."""
    # HIBP uses k-anonymity: only first 5 chars of SHA1 are sent
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    # Response is "SUFFIX:COUNT" per line
    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)    # Found — times seen in breaches
    
    return 0    # Not found

count = check_password_pwned("password123")
print(f"Found in {count} breaches" if count else "Not found in known breaches")
```

### VirusTotal API (free key, 4 req/min)
```python
import requests

API_KEY = "your_vt_api_key"
ip = "8.8.8.8"

url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
headers = {"x-apikey": API_KEY}

response = requests.get(url, headers=headers)
data = response.json()

stats = data["data"]["attributes"]["last_analysis_stats"]
print(f"Malicious: {stats.get('malicious', 0)}")
print(f"Suspicious: {stats.get('suspicious', 0)}")
print(f"Clean: {stats.get('harmless', 0)}")
```

---

## Running the ip_info.py Tool

```bash
# Install dependency
pip install requests

# Basic usage — look up Google DNS
python3 ip_info.py 8.8.8.8

# Cloudflare DNS
python3 ip_info.py 1.1.1.1

# Your own public IP
python3 ip_info.py

# Verbose — see raw JSON
python3 ip_info.py 8.8.8.8 -v

# Batch lookup from file
echo "8.8.8.8" > ips.txt
echo "1.1.1.1" >> ips.txt
echo "9.9.9.9" >> ips.txt
python3 ip_info.py -f ips.txt

# Save results to JSON
python3 ip_info.py 8.8.8.8 -o results.json

# View saved results
cat results.json
```

### Expected output
```
==================================================
  IP Information Report: 8.8.8.8
==================================================

[LOCATION]
  Country      : United States (US)
  Region       : California (CA)
  City         : Mountain View
  Postal code  : 94043
  Latitude     : 37.4056
  Longitude    : -122.0775
  Timezone     : America/Los_Angeles (UTC-0800)

[NETWORK]
  ISP / Org    : AS15169 Google LLC
  ASN          : AS15169
  Currency     : US Dollar (USD)
  Languages    : en-US,es-US,haw,fr
==================================================
```

---

## Extension Ideas

```python
# 1. Add CSV export
import csv
with open("results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["ip", "country", "city", "org", "asn"])
    writer.writeheader()
    for result in all_results:
        writer.writerow({
            "ip": result.get("ip"),
            "country": result.get("country_name"),
            "city": result.get("city"),
            "org": result.get("org"),
            "asn": result.get("asn")
        })

# 2. Add rate limiting (free API = 1000 req/day)
import time
for ip in ip_list:
    data = get_ip_info(ip)
    print_ip_report(data)
    time.sleep(1.2)    # Stay under rate limit

# 3. Filter results (e.g., only show non-US IPs)
foreign_ips = [r for r in results if r.get("country") != "US"]
```

---

*Day 15 — 60-Day Cybersecurity Journey | github.com/NivedhithaKS-SEC/cybersec-journey*
