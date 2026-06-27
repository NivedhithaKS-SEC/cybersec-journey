# WAF Home Lab — ModSecurity v3 + Nginx + ELK Stack

**Built by:** Nivedhitha K.S. (Crystal) | [LinkedIn](https://linkedin.com/in/nivedhitha-k-s) | [GitHub](https://github.com/NivedhithaKS-SEC)

A fully functional Web Application Firewall home lab simulating real-world attack detection, log analysis, and SIEM-style alerting — built entirely from source on Ubuntu 20.04 in VirtualBox.

---

## Architecture

```
Attacker (curl / Nikto / ZAP)
        │
        ▼ HTTP request
┌─────────────────────────┐
│   Nginx 1.18 (port 80)  │  ← Reverse proxy
│   ModSecurity v3        │  ← WAF engine (OWASP CRS 3.3.5)
└────────────┬────────────┘
             │ clean requests only
             ▼
     DVWA (Docker, port 8080)
     Damn Vulnerable Web App

             │ audit + access logs
             ▼
┌─────────────────────────────────────────┐
│            ELK Stack (Docker)           │
│  Filebeat → Logstash → Elasticsearch   │
│              ↓                          │
│           Kibana (port 5601)            │
│        SIEM Dashboard + Alerts          │
└─────────────────────────────────────────┘
```

---

## Stack

| Component | Version | Role |
|---|---|---|
| ModSecurity | v3 (compiled from source) | WAF engine |
| Nginx | 1.18.0 | Reverse proxy + WAF host |
| OWASP Core Rule Set | 3.3.5 | Attack detection rules |
| DVWA | Latest (Docker) | Vulnerable target application |
| Elasticsearch | 8.11.0 | Log indexing and storage |
| Logstash | 8.11.0 | Log parsing and enrichment |
| Kibana | 8.11.0 | SIEM dashboard and visualization |
| Filebeat | 8.11.0 | Log shipping from host to Logstash |

---

## What I Built

### Phase 1 — Target Application (DVWA)
Deployed DVWA (Damn Vulnerable Web Application) in Docker as the backend target. DVWA provides realistic vulnerable endpoints for SQL injection, XSS, file inclusion, command injection, and more — all in a controlled environment.

### Phase 2 — ModSecurity v3 WAF (compiled from source)
Compiled ModSecurity v3 from source on Ubuntu 20.04, built the Nginx dynamic module connector, and deployed the OWASP Core Rule Set 3.3.5. Nginx acts as a reverse proxy — all traffic passes through ModSecurity before reaching DVWA.

Key configuration decisions:
- `SecRuleEngine On` — blocking mode (not detection-only)
- OWASP CRS 3.3.5 loaded via explicit rule file includes (excluded incompatible multipart rule)
- Audit logging to `/var/log/modsec_audit.log` with full request/response capture
- Custom rules written for scanner detection and sensitive file access

### Phase 3 — ELK Stack SIEM
Deployed Elasticsearch, Logstash, and Kibana using Docker Compose. Logstash parses both Nginx access logs and ModSecurity audit logs using Grok filters, enriches them with metadata, and indexes into Elasticsearch under `waf-logs-YYYY.MM.DD` indices.

### Phase 4 — Filebeat Log Shipping
Configured Filebeat on the host to watch both log sources and ship to Logstash on port 5044. Multiline pattern configured for ModSecurity audit log boundaries (`--[hex]-`).

### Phase 5 — Attack Simulation and Detection
Simulated five attack categories against DVWA and confirmed WAF detection and blocking for each:

| Attack Type | Payload | OWASP Rule | Result |
|---|---|---|---|
| SQL Injection | `1' OR '1'='1` | 942100 (libinjection) | 403 Blocked |
| XSS | `<script>alert(1)</script>` | 941100 | 403 Blocked |
| Path Traversal | `../../../../etc/passwd` | 930100 | 403 Blocked |
| UNION-based SQLi | `UNION SELECT 1,2,3--` | 942100 | 403 Blocked |
| Shadow file access | `../../../etc/shadow` | 930100 | 403 Blocked |

---

## Custom IDS Rules Written

```apache
# Block SQLmap automated scanner (rule id: 10001)
SecRule REQUEST_HEADERS:User-Agent "@contains sqlmap" \
    "id:10001,phase:1,deny,status:403,log,msg:'SQLMap scanner blocked'"

# Block .env file enumeration (rule id: 10002)
SecRule REQUEST_URI "@endsWith .env" \
    "id:10002,phase:1,deny,status:403,log,msg:'Sensitive file access attempt'"

# Log all WAF blocks for SIEM correlation (rule id: 10003)
SecRule RESPONSE_STATUS "@streq 403" \
    "id:10003,phase:5,pass,log,msg:'Request blocked by WAF'"
```

Custom rule test result:
```bash
$ curl -A "sqlmap/1.0" http://localhost -w "%{http_code}"
403
```

---

## ModSecurity Audit Log — SQL Injection Detection

```
ModSecurity: Warning. detected SQLi using libinjection.
[file "REQUEST-942-APPLICATION-ATTACK-SQLI.conf"] [line "46"] [id "942100"]
[msg "SQL Injection Attack Detected via libinjection"]
[data "Matched Data: s&sos found within ARGS:id: 1' OR '1'='1"]
[severity "2"] [ver "OWASP_CRS/3.3.5"]

ModSecurity: Access denied with code 403 (phase 2).
Matched Operator 'Ge' with parameter '5' against variable 'TX:ANOMALY_SCORE'
[id "949110"] [msg "Inbound Anomaly Score Exceeded (Total Score: 5)"]
```

This is real SOC-style log output — rule ID, detection method (libinjection), matched payload, anomaly score, and blocking decision all captured in structured audit format.

---

## SIEM — Kibana Dashboard

After attack simulation, logs flow through the full pipeline:

```
Attack → ModSecurity blocks → audit log written → Filebeat ships
→ Logstash parses → Elasticsearch indexes → Kibana visualizes
```

**Elasticsearch index confirmed:**
```
yellow open   waf-logs-2026.06.27   18 documents   110.9kb
```

Kibana Discover shows 18 attack events with full metadata including timestamps, request URIs, HTTP status codes, and ModSecurity rule matches — enabling the same analysis workflow used in enterprise SOC environments.

---

## Skills Demonstrated

- **WAF configuration and rule writing** — ModSecurity v3, OWASP CRS, custom SecRules
- **Linux system administration** — compiled C++ project from source, dynamic module loading, systemd service management
- **SIEM log pipeline** — Filebeat → Logstash (Grok parsing) → Elasticsearch → Kibana
- **Attack simulation and detection** — SQLi, XSS, LFI, path traversal, scanner detection
- **Docker and Docker Compose** — multi-service deployment and orchestration
- **IDS/IPS-adjacent rule writing** — phase-based rules, anomaly scoring, custom block logic
- **Alert tuning** — understanding anomaly score thresholds and CRS paranoia levels

---

## Repository Structure

```
waf-homelab/
├── README.md
├── configs/
│   ├── nginx/
│   │   └── dvwa-waf          # Nginx virtual host with ModSecurity enabled
│   ├── modsec/
│   │   ├── main.conf         # ModSecurity rule includes
│   │   └── custom_rules.conf # Hand-written IDS rules
│   └── filebeat/
│       └── filebeat.yml      # Log shipping config
├── elk/
│   ├── docker-compose.yml    # ELK Stack deployment
│   └── logstash.conf         # Grok parsing pipeline
└── screenshots/
    ├── 01-modsec-audit-sqli-detection.png
    ├── 02-nginx-waf-blocking-403.png
    ├── 03-nginx-config-test-ok.png
    ├── 04-modsecurity-nginx-compile.png
    ├── 05-dvwa-target-application.png
    ├── 06-elasticsearch-running.png
    ├── 07-kibana-dashboard.png
    ├── 08-kibana-discover-18-hits.png
    └── 09-custom-rule-sqlmap-blocked.png
```

---

## How to Reproduce

### Prerequisites
- Ubuntu 20.04 LTS (VM recommended)
- 6GB RAM, 40GB disk
- Internet access for package downloads

### Quick Start
```bash
# 1. Install dependencies
sudo apt install -y git curl wget build-essential nginx docker.io

# 2. Clone this repo
git clone https://github.com/NivedhithaKS-SEC/waf-homelab.git
cd waf-homelab

# 3. Start DVWA
docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa

# 4. Compile ModSecurity v3 (see Phase 2 notes in README)
# Full compile steps in configs/modsec/BUILD_NOTES.md

# 5. Start ELK Stack
cd elk && docker-compose up -d

# 6. Start Filebeat
sudo cp configs/filebeat/filebeat.yml /etc/filebeat/
sudo systemctl start filebeat
```

---

## Related Portfolio Projects

- [Email Security Watchdog](https://github.com/NivedhithaKS-SEC/cybersec-journey) — Python/Flask phishing detection tool (100% detection on test set)
- [ISO 27001 Gap Assessment](https://github.com/NivedhithaKS-SEC/cybersec-journey) — 93-control Annex A assessment for fictional GridFlex Technologies
- [NIST CSF v2.0 Risk Assessment](https://github.com/NivedhithaKS-SEC/cybersec-journey) — 12-risk assessment for fictional Meridian Diagnostics
- [Bugcrowd P3 Finding](https://github.com/NivedhithaKS-SEC/cybersec-journey) — WAF bypass on safeocs.gov (U.S. DOT VDP)

---

*Built June 2026 | Ubuntu 20.04 | VirtualBox home lab*
