# NIST CSF v2.0 Risk Assessment — Healthcare Sector (Portfolio Project)

End-to-end Governance, Risk & Compliance (GRC) deliverable demonstrating a complete risk assessment workflow aligned to the **NIST Cybersecurity Framework v2.0**, for a fictional healthcare organization (Meridian Diagnostics Pvt. Ltd.).

## What's Included

| File | Description |
|---|---|
| [`NIST_CSF_Risk_Assessment.md`](./NIST_CSF_Risk_Assessment.md) | Full report — asset inventory, threat ID, risk matrix, risk register, treatment plan |
| [`NIST_CSF_Risk_Assessment.docx`](./NIST_CSF_Risk_Assessment.docx) | Formal Word version with title page, headers/footers, formatted tables |
| [`NIST_CSF_Risk_Assessment.pdf`](./NIST_CSF_Risk_Assessment.pdf) | PDF export of the Word report |
| [`risk-register.csv`](./risk-register.csv) | Structured risk register data (sortable/filterable) |

## Methodology

Aligned to **NIST CSF v2.0** and **NIST SP 800-30**:

1. Asset Inventory (CIA criticality ratings)
2. Threat Identification (threat source → event → vulnerability → CSF function)
3. Risk Rating (5x5 Likelihood × Impact matrix)
4. Risk Register (consolidated, scored, prioritized)
5. Risk Treatment Plan (controls mapped to NIST CSF subcategories, owners, timelines)

## Key Findings

- **15** critical assets inventoried across clinical, cloud, identity, and third-party systems
- **12** threat scenarios identified and mapped to NIST CSF functions
- **2 Critical** and **5 High** risks identified — fully addressed in the treatment plan
- Treatment plan phased 0-9 months, prioritizing Protect/Identify controls (MFA, segmentation, CSPM) followed by Detect (EDR, UEBA, WIDS) and Recover (backup/DR testing)

## Disclaimer

The organization name, assets, and figures used in this assessment are fictional and created for portfolio demonstration purposes. The methodology, structure, and NIST CSF v2.0 subcategory mappings reflect real-world risk assessment practice and are directly transferable to actual GRC engagements.

## Related Projects

- [ISO 27001 Annex A Gap Assessment](../ISO27001-Gap-Assessment) *(update path as applicable)*
- [WAF & SIEM Home Lab](../../SOC/WAF-SIEM-Home-Lab) *(update path as applicable)*
