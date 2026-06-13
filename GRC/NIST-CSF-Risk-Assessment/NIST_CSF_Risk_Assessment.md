# NIST Cybersecurity Framework (CSF) v2.0 — Risk Assessment Report

**Organization:** Meridian Diagnostics Pvt. Ltd. *(fictional organization, built for portfolio demonstration)*

**Prepared by:** Nivedhitha K.S. (Crystal) — GRC Analyst (Portfolio Project)

**Version:** 1.0 | **Classification:** Confidential — Internal Use Only

> A full formatted version of this report is also available as a [Word document](./NIST_CSF_Risk_Assessment.docx) and [PDF](./NIST_CSF_Risk_Assessment.pdf).

---

## 1. Executive Summary

This report presents a structured cybersecurity risk assessment for Meridian Diagnostics Pvt. Ltd., aligned to the NIST Cybersecurity Framework (CSF) v2.0. It identifies critical information assets, maps threat sources and events against those assets, scores resulting risks using a 5x5 likelihood-impact matrix, and proposes a prioritized treatment plan with controls mapped to specific NIST CSF subcategories.

**Highlights:**
- 15 critical assets across clinical applications, cloud infrastructure, identity systems, and third-party integrations
- 12 threat scenarios mapped to vulnerabilities and NIST CSF functions
- 12 risks scored and consolidated into a prioritized risk register
- 2 risks rated **Critical**, 5 rated **High** — all addressed in the treatment plan
- Treatment plan phased across 0-9 months, prioritizing Identify/Protect controls first

## 2. Methodology

Performed in line with NIST CSF v2.0 and NIST SP 800-30 (Guide for Conducting Risk Assessments):

1. **Asset Inventory** — identify and categorize assets, assign CIA criticality (High/Medium/Low)
2. **Threat Identification** — map threat sources/events to vulnerabilities and CSF functions
3. **Risk Rating** — Risk Score = Likelihood (1-5) × Impact (1-5), banded into Low/Medium/High/Critical
4. **Risk Register** — consolidated, sorted risk statements with CSF function mapping
5. **Treatment Plan** — controls mapped to NIST CSF subcategories, with owners and timelines

### NIST CSF v2.0 Functions

| Function | Purpose |
|---|---|
| Govern (GV) | Cybersecurity risk management strategy, expectations, and policy |
| Identify (ID) | Understand assets, business context, and risk to systems/people/data |
| Protect (PR) | Safeguards — access control, awareness, data security, protective tech |
| Detect (DE) | Timely identification of cybersecurity events |
| Respond (RS) | Actions to contain and mitigate detected incidents |
| Recover (RC) | Resilience plans and restoration of impaired capabilities |

## 3. Asset Inventory

| ID | Asset Name | Category | Owner | Criticality (C-I-A) | Description / Notes |
|---|---|---|---|---|---|
| A-01 | Patient Records Database (PostgreSQL) | Data / Information | Database Admin Team | H-H-H | Stores PHI for ~120,000 patients; subject to HIPAA-equivalent data protection requirements. |
| A-02 | Hospital Information System (HIS) Application Servers | Application / Server | IT Operations | H-H-H | Core clinical workflow application; 24x7 availability requirement. |
| A-03 | Active Directory Domain Controllers | Identity Infrastructure | IAM Team | H-H-H | Authentication and authorization for ~800 employees and service accounts. |
| A-04 | Email & Collaboration Platform (M365 tenant) | Cloud Service | IT Operations | M-H-H | Hosts corporate email, OneDrive, Teams; primary phishing attack surface. |
| A-05 | Endpoint Devices (laptops/desktops) | Hardware / Endpoint | End User Computing | M-M-M | ~750 corporate-managed Windows endpoints; EDR agent deployed. |
| A-06 | Diagnostic Imaging Devices (PACS-connected) | Medical / OT Device | Biomedical Engineering | H-M-H | Legacy imaging modalities with limited patching capability; network-segmented. |
| A-07 | Cloud Infrastructure (AWS production VPC) | Cloud Infrastructure | Cloud Engineering | H-H-H | Hosts patient portal, billing API, and analytics workloads. |
| A-08 | Billing & Payment Processing System | Application | Finance IT | H-H-M | Processes card and insurance payment data; PCI-DSS scope. |
| A-09 | VPN / Remote Access Gateway | Network Infrastructure | Network Security | H-M-H | Remote access for ~150 remote/clinical staff; MFA-enforced. |
| A-10 | SIEM Platform (ELK Stack) | Security Tooling | SOC Team | H-H-H | Centralized log aggregation and detection; single point of monitoring. |
| A-11 | Backup & Disaster Recovery Storage | Data / Infrastructure | IT Operations | H-M-H | Offsite + cloud backups for critical systems; tested quarterly. |
| A-12 | Third-Party Lab Results Integration (HL7 interface) | Third-Party Integration | Integration Team | M-H-H | Inbound HL7 feeds from external diagnostic labs; trust boundary risk. |
| A-13 | Wi-Fi Network (Guest & Clinical SSIDs) | Network Infrastructure | Network Security | M-M-M | Segmented guest and clinical wireless networks across 6 facility sites. |
| A-14 | HR & Payroll System (SaaS) | Cloud Service | HR / IT | M-H-M | Stores employee PII and bank details; vendor-hosted SaaS. |
| A-15 | Source Code Repositories (GitHub Enterprise) | Application / Dev | Engineering | M-H-M | Houses proprietary application code and CI/CD pipeline secrets. |

## 4. Threat Identification

| ID | Threat Source | Threat Event | Vulnerability Exploited | NIST CSF Function(s) |
|---|---|---|---|---|
| T-01 | External — Cybercriminal (financially motivated) | Phishing email leads to credential theft and BEC/ransomware deployment. | Insufficient email filtering, low user awareness, lack of phishing-resistant MFA. | Identify, Protect, Detect, Respond |
| T-02 | External — Ransomware Group | Ransomware encrypts HIS application servers and patient database, disrupting clinical operations. | Unpatched server vulnerabilities, flat network segmentation, weak endpoint detection coverage. | Protect, Detect, Respond, Recover |
| T-03 | External — Opportunistic Attacker | Exploitation of internet-facing AWS workload (e.g., misconfigured S3 bucket or exposed API). | Cloud misconfiguration, missing CSPM controls, weak IAM role scoping. | Identify, Protect, Detect |
| T-04 | Insider — Negligent Employee | Accidental exposure of patient data via misdirected email or unsecured file share. | Lack of DLP controls, inadequate data handling training, excessive sharing permissions. | Protect, Detect |
| T-05 | Insider — Malicious/Disgruntled Employee | Unauthorized access to and exfiltration of patient records prior to departure. | Excessive standing privileges, lack of UEBA/anomaly detection, weak offboarding process. | Identify, Protect, Detect, Respond |
| T-06 | External — Nation-State / Advanced Actor | Supply-chain compromise via third-party HL7 lab integration leading to lateral movement. | Insufficient third-party risk assessment, lack of network segmentation for integration points. | Identify, Protect, Detect, Respond |
| T-07 | External — Attacker (Network-based) | Exploitation of legacy diagnostic imaging device (unpatched OS) to gain network foothold. | End-of-life OT/medical device software, inadequate network segmentation/monitoring. | Identify, Protect, Detect |
| T-08 | Environmental — Natural/Utility | Power outage or data center failure causes extended downtime of production systems. | Insufficient redundancy, untested DR/BCP procedures, single-region dependency. | Recover, Respond |
| T-09 | External — Credential Stuffing | Automated credential-stuffing attacks against VPN/remote access portal using leaked credentials. | Password reuse, absence of breach-credential monitoring, account lockout gaps. | Protect, Detect |
| T-10 | External — Attacker (Web Application) | SQL injection or broken access control on patient portal exposes patient database. | Insecure coding practices, lack of WAF/SAST-DAST in CI/CD pipeline. | Identify, Protect, Detect, Respond |
| T-11 | Insider — Third-Party Vendor/Contractor | Vendor with excessive remote access privileges introduces malware during maintenance. | Lack of vendor access governance, no just-in-time access, insufficient monitoring of vendor sessions. | Identify, Protect, Detect |
| T-12 | External — Wireless Attacker | Rogue access point or Wi-Fi eavesdropping on clinical wireless network. | Weak Wi-Fi segmentation, outdated WPA configuration, lack of wireless intrusion detection. | Protect, Detect |

## 5. Risk Rating Matrix

Risk Score = Likelihood × Impact (both rated 1-5).

| Score Range | Rating | Treatment Priority |
|---|---|---|
| 1-4 | Low | Accept / monitor during routine reviews |
| 5-9 | Medium | Treat within 6-12 months |
| 10-15 | High | Treat within 3-6 months; report to management |
| 16-25 | Critical | Immediate action (0-3 months); escalate to leadership |

## 6. Risk Register

Sorted by descending risk score (highest priority first).

| Risk ID | Description | Likelihood | Impact | Score | Rating | Primary CSF Function(s) |
|---|---|---|---|---|---|---|
| R-02 | Phishing-driven credential compromise (T-01) leading to unauthorized access to Patient Records DB (A-01). | 5 | 5 | 25 | **Critical** | Identify, Protect, Detect, Respond |
| R-01 | Ransomware deployment on HIS servers (A-02) via T-02, disrupting clinical operations and patient safety. | 4 | 5 | 20 | **Critical** | Protect, Detect, Respond, Recover |
| R-05 | Cloud misconfiguration in AWS production VPC (A-07) exposes billing data (A-08) (T-03). | 4 | 4 | 16 | **Critical** | Identify, Protect, Detect |
| R-03 | SQL injection / access control flaw in patient portal (T-10) exposes Patient Records DB (A-01) via AWS prod (A-07). | 3 | 5 | 15 | **High** | Identify, Protect, Detect |
| R-06 | Supply-chain compromise via HL7 lab integration (A-12) enabling lateral movement (T-06). | 3 | 4 | 12 | **High** | Identify, Protect, Detect, Respond |
| R-07 | Compromise of legacy diagnostic imaging device (A-06) used as network pivot point (T-07). | 3 | 4 | 12 | **High** | Identify, Protect, Detect |
| R-08 | Credential-stuffing attack against VPN gateway (A-09) results in unauthorized remote access (T-09). | 4 | 3 | 12 | **High** | Protect, Detect |
| R-10 | Accidental data exposure via misdirected email or open file share containing PHI (A-01, A-04) (T-04). | 4 | 3 | 12 | **High** | Protect, Detect |
| R-04 | Malicious insider exfiltrates patient records (A-01) prior to offboarding (T-05). | 2 | 5 | 10 | **High** | Identify, Protect, Detect, Respond |
| R-09 | Extended outage of production data center / cloud region affecting A-02, A-07, A-11 (T-08). | 2 | 5 | 10 | **High** | Respond, Recover |
| R-12 | Wireless eavesdropping or rogue AP on clinical Wi-Fi (A-13) intercepts unencrypted traffic (T-12). | 3 | 3 | 9 | **Medium** | Protect, Detect |
| R-11 | Vendor/contractor with excessive privileged access introduces malware during maintenance (A-02, A-03) (T-11). | 2 | 4 | 8 | **Medium** | Identify, Protect, Detect |

## 7. Risk Treatment Plan

All risks assigned a **Mitigate** strategy. Sorted by descending risk score.

| Risk ID | Strategy | Recommended Controls | CSF Subcategories | Owner | Timeline |
|---|---|---|---|---|---|
| R-02 | Mitigate | Deploy phishing-resistant MFA (FIDO2) for all privileged and remote-access accounts; conduct quarterly phishing simulations; enable conditional access policies and impossible-travel alerting in M365. | PR.AC-7, PR.AT-1, DE.CM-3 | IAM Team / SOC | 0-3 months |
| R-01 | Mitigate | Implement network segmentation (Zero Trust zones) isolating HIS servers; deploy EDR with ransomware behavior detection across all endpoints; validate offline/immutable backups via quarterly restore tests. | PR.AC-5, PR.DS-1, DE.CM-1, RC.RP-1 | IT Operations / SOC | 0-6 months |
| R-05 | Mitigate | Deploy Cloud Security Posture Management (CSPM) tooling for AWS production VPC; enforce least-privilege IAM roles via automated policy review; enable S3 bucket-level encryption and public-access blocks. | ID.RA-1, PR.AC-4, PR.DS-1 | Cloud Engineering | 0-3 months |
| R-03 | Mitigate | Integrate SAST/DAST scanning into CI/CD pipeline; deploy WAF in front of patient portal; perform annual penetration test and remediate critical findings within 30 days. | ID.RA-1, PR.IP-2, DE.CM-8 | Engineering / Security | 0-3 months |
| R-06 | Mitigate | Conduct third-party risk assessments for all HL7 integration partners; place integration points in a dedicated DMZ segment with monitored traffic; require contractual security SLAs from lab partners. | ID.SC-2, PR.AC-5, DE.CM-1 | Integration Team / GRC | 3-6 months |
| R-07 | Mitigate | Establish dedicated VLAN for medical/OT devices with strict firewall rules; deploy passive network monitoring for anomalous device behavior; create compensating controls inventory for unpatchable legacy devices. | PR.AC-5, DE.CM-1, PR.IP-12 | Biomedical Eng. / Network Security | 3-6 months |
| R-08 | Mitigate | Enforce MFA on VPN gateway (already partially in place — extend to 100% coverage); integrate breach-credential monitoring feed to trigger forced password resets; tune lockout thresholds. | PR.AC-7, DE.CM-7 | Network Security | 0-3 months |
| R-10 | Mitigate | Deploy Data Loss Prevention (DLP) policies across email and file-sharing platforms; provide role-based data-handling training; restrict default sharing permissions to internal-only. | PR.DS-5, PR.AT-1 | IT Operations / GRC | 3-6 months |
| R-04 | Mitigate | Implement least-privilege access reviews quarterly; deploy UEBA/anomaly detection for data access patterns; formalize and automate offboarding checklist with same-day access revocation. | PR.AC-1, PR.AC-4, DE.CM-3 | IAM Team / HR | 0-6 months |
| R-09 | Mitigate | Update and test Business Continuity / Disaster Recovery plan with annual tabletop exercises; implement multi-AZ redundancy for critical workloads; document RTO/RPO targets per system. | RC.RP-1, RC.IM-1, ID.BE-5 | IT Operations / GRC | 3-9 months |
| R-12 | Mitigate | Migrate clinical Wi-Fi to WPA3-Enterprise with certificate-based authentication; deploy wireless intrusion detection (WIDS); conduct periodic rogue-AP sweeps across all sites. | PR.AC-5, PR.PT-4, DE.CM-1 | Network Security | 3-9 months |
| R-11 | Mitigate | Implement Privileged Access Management (PAM) with just-in-time vendor access and session recording; require vendor access requests to be approved and time-bound. | PR.AC-1, PR.AC-4, DE.CM-3 | IAM Team / Vendor Mgmt | 3-6 months |

## 8. Governance & Review

- Reviewed **annually**, or triggered by major incidents, architecture changes, new regulations, or new CVEs affecting in-scope assets
- Risk register updated on a rolling basis as treatments are completed; residual risk re-scored after implementation
- Accepted risks require formal sign-off from the Asset Owner with documented justification and review date
- **Follow-on recommendation:** develop a dedicated Incident Response Plan and run a tabletop exercise for the R-01 (ransomware) and R-02 (credential compromise) scenarios

---

*Note: Organization name, assets, and figures are fictional, created for portfolio/demonstration purposes. Methodology and control mappings reflect real-world NIST CSF v2.0 risk assessment practice.*
