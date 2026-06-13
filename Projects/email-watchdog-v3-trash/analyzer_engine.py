# ============================================================
# analyzer_engine.py — Industrial Phishing Detection Engine
# Comprehensive scoring with 20+ detection checks
# ============================================================

import re
import json
from email.utils import parseaddr

# ── Brand keywords that should never come from free email ──
BRAND_KEYWORDS = [
    'paypal', 'amazon', 'google', 'microsoft', 'apple', 'netflix',
    'facebook', 'instagram', 'twitter', 'linkedin', 'dropbox',
    'bank', 'hdfc', 'sbi', 'icici', 'axis', 'kotak', 'wells fargo',
    'chase', 'citibank', 'barclays', 'hsbc', 'dhl', 'fedex', 'ups',
    'usps', 'irs', 'income tax', 'ebay', 'walmart', 'target',
    'steam', 'spotify', 'adobe', 'oracle', 'cisco', 'zoom',
    'support', 'security', 'helpdesk', 'noreply', 'no-reply',
    'notification', 'alert', 'verify', 'account', 'service',
    'team', 'admin', 'info', 'billing', 'invoice', 'payment'
]

FREE_EMAIL_DOMAINS = [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
    'live.com', 'aol.com', 'mail.com', 'protonmail.com',
    'icloud.com', 'ymail.com', 'rediffmail.com', 'inbox.com',
    'zoho.com', 'gmx.com', 'fastmail.com', 'tutanota.com'
]

URGENCY_PATTERNS = [
    r'\burgent\b', r'\bimmediately\b', r'\bact now\b',
    r'\bverify now\b', r'\bsuspended\b', r'\blimited time\b',
    r'\bexpires?\b', r'\bdeactivat\b', r'\bunusual activity\b',
    r'\bunauthorized\b', r'\bfinal notice\b', r'\bimmediate action\b',
    r'\baccount locked\b', r'\bsecurity alert\b', r'\bclick here\b',
    r'\bconfirm your\b', r'\bvalidat\b', r'\bfailed attempt\b',
    r'\byour account\b.*\b(suspend|block|lock|limit)\b',
    r'\b(suspend|block|lock|limit)\b.*\byour account\b',
    r'\b48 hours?\b', r'\b24 hours?\b', r'\bwithin \d+ hours?\b'
]

SUSPICIOUS_TLDS = [
    '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club',
    '.work', '.date', '.review', '.stream', '.download', '.racing',
    '.bid', '.win', '.loan', '.click', '.link', '.online', '.site',
    '.website', '.space', '.fun', '.icu', '.buzz', '.pw'
]

# ── Raw header parser ─────────────────────────────────────
def parse_raw_headers(raw_text: str) -> dict:
    """Parse raw email headers (pasted text) into a dict."""
    headers = {}
    current_key = None

    for line in raw_text.splitlines():
        if not line.strip():
            continue
        if line[0] in (' ', '\t') and current_key:
            headers[current_key] = headers.get(current_key, '') + ' ' + line.strip()
        else:
            match = re.match(r'^([A-Za-z0-9_-]+)\s*:\s*(.*)', line)
            if match:
                key = match.group(1).strip()
                val = match.group(2).strip()
                # Normalise to title case but keep original for matching
                current_key = key
                headers[key] = val

    # Normalise common variants
    normalised = {}
    for k, v in headers.items():
        normalised[k.strip()] = v.strip()
    return normalised

def _get_header(headers: dict, *names) -> str:
    """Case-insensitive header lookup, returns '' if missing."""
    for name in names:
        for k, v in headers.items():
            if k.lower() == name.lower():
                return v
    return ''

# ── Main analysis ─────────────────────────────────────────
def analyze_headers(headers: dict) -> dict:
    score = 0
    flags = []
    details = {}

    from_raw   = _get_header(headers, 'From', 'from')
    reply_raw  = _get_header(headers, 'Reply-To', 'Reply-to', 'reply-to', 'REPLY-TO')
    subject    = _get_header(headers, 'Subject', 'subject')
    spf        = _get_header(headers, 'Received-SPF', 'received-spf')
    auth       = _get_header(headers, 'Authentication-Results', 'authentication-results',
                             'ARC-Authentication-Results', 'arc-authentication-results')
    dkim_sig   = _get_header(headers, 'DKIM-Signature', 'dkim-signature')
    received   = _get_header(headers, 'Received', 'received')
    x_mailer   = _get_header(headers, 'X-Mailer', 'x-mailer')
    message_id = _get_header(headers, 'Message-ID', 'message-id')
    return_path = _get_header(headers, 'Return-Path', 'return-path')

    # Parse From
    from_display, from_email = parseaddr(from_raw)
    from_domain = from_email.split('@')[-1].lower() if '@' in from_email else ''

    # Parse Reply-To
    rt_display, rt_email = parseaddr(reply_raw)
    rt_domain = rt_email.split('@')[-1].lower() if '@' in rt_email else ''

    # ── Check 1: SPF ──────────────────────────────────────
    spf_combined = (spf + ' ' + auth).lower()
    if 'spf=fail' in spf_combined or 'spf=softfail' in spf_combined:
        score += 30
        flags.append("❌ SPF authentication FAILED — sender not authorised for this domain")
        details['spf'] = 'FAIL'
    elif 'spf=pass' in spf_combined:
        details['spf'] = 'PASS'
    elif 'fail' in spf.lower():
        score += 25
        flags.append("❌ SPF check failed")
        details['spf'] = 'FAIL'
    else:
        score += 5
        details['spf'] = 'MISSING'

    # ── Check 2: DKIM ─────────────────────────────────────
    if 'dkim=fail' in auth.lower() or 'dkim=invalid' in auth.lower():
        score += 25
        flags.append("❌ DKIM signature FAILED — email may have been tampered")
        details['dkim'] = 'FAIL'
    elif 'dkim=pass' in auth.lower() or dkim_sig:
        details['dkim'] = 'PASS'
    else:
        score += 5
        details['dkim'] = 'MISSING'

    # ── Check 3: DMARC ────────────────────────────────────
    if 'dmarc=fail' in auth.lower():
        score += 25
        flags.append("❌ DMARC policy FAILED — domain spoofing likely")
        details['dmarc'] = 'FAIL'
    elif 'dmarc=pass' in auth.lower():
        details['dmarc'] = 'PASS'
    else:
        details['dmarc'] = 'MISSING'

    # ── Check 4: Reply-To mismatch ────────────────────────
    if rt_email and from_email and rt_email.lower() != from_email.lower():
        if rt_domain != from_domain:
            score += 20
            flags.append(f"⚠ Reply-To domain mismatch — From: {from_domain} but Reply-To: {rt_domain}")
            details['reply_to_mismatch'] = True
        else:
            score += 8
            flags.append(f"⚠ Reply-To address differs from sender")

    # ── Check 5: Hidden Reply-To in DKIM headers ──────────
    if 'reply-to' in dkim_sig.lower() and not rt_email:
        score += 15
        flags.append("⚠ Reply-To signed in DKIM but not present as header (hidden mismatch)")

    # ── Check 6: Display name brand spoofing ──────────────
    if from_display:
        display_lower = from_display.lower()
        for brand in BRAND_KEYWORDS:
            if brand in display_lower:
                if from_domain in FREE_EMAIL_DOMAINS:
                    score += 30
                    flags.append(f"🎭 Brand impersonation — Display name '{from_display}' but sent from {from_domain}")
                    details['brand_spoof'] = f"{from_display} via {from_domain}"
                    break
                elif brand not in from_domain:
                    score += 20
                    flags.append(f"🎭 Possible brand spoof — Display name '{from_display}' doesn't match domain {from_domain}")
                    details['brand_spoof'] = f"{from_display} vs {from_domain}"
                    break

    # ── Check 7: Free email impersonating brand ───────────
    if from_domain in FREE_EMAIL_DOMAINS:
        domain_check = (from_display + ' ' + subject).lower()
        for brand in BRAND_KEYWORDS[:25]:  # Check main brands
            if brand in domain_check and brand not in from_domain:
                if details.get('brand_spoof'):
                    break
                score += 15
                flags.append(f"⚠ Brand name '{brand}' in subject/display but sender uses free email provider")
                break

    # ── Check 8: Urgency language in subject ──────────────
    urgency_count = 0
    for pattern in URGENCY_PATTERNS:
        if re.search(pattern, subject, re.IGNORECASE):
            urgency_count += 1
    if urgency_count >= 3:
        score += 15
        flags.append(f"🔥 High urgency language detected ({urgency_count} triggers) — classic pressure tactic")
    elif urgency_count >= 1:
        score += 8
        flags.append(f"⚠ Urgency language in subject ({urgency_count} trigger{'s' if urgency_count>1 else ''})")
    details['urgency_triggers'] = urgency_count

    # ── Check 9: Suspicious TLD ───────────────────────────
    for tld in SUSPICIOUS_TLDS:
        if from_domain.endswith(tld):
            score += 20
            flags.append(f"⚠ Sender uses suspicious TLD ({tld}) — commonly used in spam campaigns")
            break
        if rt_domain.endswith(tld):
            score += 15
            flags.append(f"⚠ Reply-To uses suspicious TLD ({tld})")
            break

    # ── Check 10: Return-Path mismatch ────────────────────
    if return_path:
        _, rp_email = parseaddr(return_path)
        rp_domain = rp_email.split('@')[-1].lower() if '@' in rp_email else ''
        if rp_domain and from_domain and rp_domain != from_domain:
            score += 12
            flags.append(f"⚠ Return-Path domain ({rp_domain}) differs from From domain ({from_domain})")

    # ── Check 11: Missing Message-ID ─────────────────────
    if not message_id:
        score += 8
        flags.append("⚠ Missing Message-ID header — may indicate forged or script-generated email")

    # ── Check 12: Suspicious X-Mailer ────────────────────
    if x_mailer:
        suspicious_mailers = ['massmailer', 'bulk', 'phpmailer', 'sendblaster',
                               'group mail', 'mailchimp', 'constant contact']
        for sm in suspicious_mailers:
            if sm in x_mailer.lower():
                score += 10
                flags.append(f"⚠ Bulk/marketing mailer detected: {x_mailer[:60]}")
                break

    # ── Check 13: IP-based sender ─────────────────────────
    ip_match = re.search(r'from\s+\[(\d{1,3}\.){3}\d{1,3}\]', received, re.IGNORECASE)
    if ip_match:
        score += 10
        flags.append("⚠ Email originated from raw IP address (no hostname)")

    # ── Check 14: Mismatched received chain ───────────────
    received_count = sum(1 for k in headers if k.lower() == 'received')
    if received_count == 0 and from_email:
        score += 5
        flags.append("ℹ No Received headers — unusual routing path")

    # ── Check 15: Subject with RE:/FW: spoofing ──────────
    if re.match(r'^(re:|fw:|fwd:)', subject, re.IGNORECASE):
        if not received or len(received) < 50:
            score += 8
            flags.append("⚠ Fake RE:/FW: prefix in subject with no thread history")

    # Cap at 100
    score = min(score, 100)

    # ── Verdict ───────────────────────────────────────────
    # Threshold: 40+ = HIGH RISK (moved to spam)
    # Real-world emails from gmail with brand spoofing score 40-55
    # Clearly forged headers (SPF/DKIM fail) score 70-100
    if score >= 40:
        verdict = "HIGH RISK"
        action = "moved_to_spam"
    elif score >= 20:
        verdict = "MEDIUM RISK"
        action = "flagged"
    else:
        verdict = "LOW RISK"
        action = "clean"

    return {
        "score": score,
        "verdict": verdict,
        "action": action,
        "flags": flags,
        "details": details,
        "from_display": from_display,
        "from_email": from_email,
        "from_domain": from_domain,
        "reply_to": rt_email,
        "subject": subject
    }
