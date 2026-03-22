# CEH Modules 9, 10, 11 — Social Engineering, DoS, Session Hijacking

---

## Module 9 — Social Engineering

### What is Social Engineering?
Manipulating humans rather than hacking technology.
The weakest link in security is always the human.

### Attack Types
- **Phishing** — mass fake emails
- **Spear Phishing** — targeted at specific person
- **Vishing** — voice/phone attack
- **Smishing** — SMS attack
- **Tailgating** — physically following someone through a door
- **Pretexting** — fabricating a scenario

### Phishing Red Flags
- Urgency ("Act now or your account is closed!")
- Suspicious sender domain (paypa1.com not paypal.com)
- Generic greetings ("Dear Customer")
- Requests for credentials or payment
- Hover over links before clicking

---

## Module 10 — Denial of Service (DoS)

### Types of DoS Attacks
| Attack | How It Works |
|--------|-------------|
| SYN Flood | Sends thousands of SYN packets, never completes handshake |
| UDP Flood | Overwhelms with UDP packets |
| HTTP Flood | Overwhelms web server with GET/POST requests |
| Ping of Death | Sends oversized ping packets |
| Smurf Attack | Spoofed ICMP broadcast flood |

### DDoS (Distributed DoS)
- Uses botnet — thousands of infected computers
- Much harder to block than single-source DoS
- Attackers rent botnets on dark web

### Amplification Attacks
- DNS Amplification — small query, massive response
- NTP Amplification — monlist command returns huge data
- Attacker spoofs victim's IP as source

### Countermeasures
- Rate limiting
- Ingress/egress filtering
- CDN and DDoS protection (Cloudflare)
- Blackhole routing for attack traffic

---

## Module 11 — Session Hijacking

### What is a Session?
After you log in, the server gives you a session token.
This token identifies you for future requests.
You don't need to re-enter your password every click.

### Session Hijacking
Stealing someone's session token to impersonate them.

### Attack Methods
| Method | Description |
|--------|-------------|
| Packet Sniffing | Capture token from unencrypted HTTP |
| XSS | Steal cookie via JavaScript injection |
| CSRF | Trick user's browser into making requests |
| Session Fixation | Force victim to use attacker's session ID |
| Brute Force | Try thousands of session IDs |

### CSRF (Cross-Site Request Forgery)
- Victim is logged into bank.com
- Attacker tricks victim into visiting evil.com
- evil.com silently sends request to bank.com
- Bank processes it because victim's cookie is attached

### Countermeasures
- HTTPS everywhere (prevents sniffing)
- HttpOnly cookie flag (prevents XSS theft)
- Secure cookie flag (HTTPS only)
- CSRF tokens on all forms
- Session timeout after inactivity
- Re-authenticate for sensitive actions