# CEH Module — Social Engineering & Phishing

## What is Social Engineering?
Manipulating people into revealing confidential information
or performing actions that compromise security.
Exploits human psychology, not technical vulnerabilities.

## Types of Social Engineering Attacks

### Phishing
- Mass email campaign impersonating trusted brands
- Goal: steal credentials or install malware
- Example: Fake "Your account is suspended" email from "PayPal"

### Spear Phishing
- Targeted phishing at specific individual or organization
- Uses personal details to appear legitimate
- More dangerous than regular phishing

### Whaling
- Spear phishing targeting senior executives (CEO, CFO)
- High value targets with access to finances/data

### Vishing (Voice Phishing)
- Phone call pretending to be IT support or bank
- "Hi, I'm from Microsoft, your computer has a virus"

### Smishing (SMS Phishing)
- Text message with malicious link
- "Your parcel is held, click here to release"

### Pretexting
- Creating a fabricated scenario to extract info
- Example: Pretending to be an auditor to get access

### Baiting
- Leaving infected USB drives in parking lots
- Curious employees plug them in

### Tailgating / Piggybacking
- Following an authorized person through a secure door

## Phishing Methodology (CEH)
1. Reconnaissance — find target emails, names, roles
2. Create phishing email — mimic trusted brand
3. Set up fake website — clone of real login page
4. Send campaign — bulk or targeted emails
5. Harvest credentials — capture what victims enter
6. Use credentials — access real systems

## Tools Used (for awareness)
- GoPhish — open source phishing simulation
- SET (Social Engineering Toolkit) — in Kali Linux
- Evilginx — advanced credential capture

## Defense Against Social Engineering
- Security awareness training
- Email filtering and SPF/DKIM/DMARC
- Multi-Factor Authentication (MFA)
- Verify caller identity before sharing info
- Never plug in unknown USB devices