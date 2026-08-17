# Risk Note

Condensed, standalone version of the risk register in `Phase6_Ethics_Governance_Risk.md` and Section 9 of the product proposal.

## Top Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Unreviewed high-risk interaction reaches a patient | Low (with MVP design) | Severe | Mandatory pharmacist review of all high-risk flags; conservative over-flagging; incident-review process | Clinical Lead |
| Regulatory classification as SaMD | Medium | High | Built as decision-support with mandatory human review, not autonomous diagnosis; regulatory counsel engaged early | Regulatory Counsel |
| Health data privacy breach | Low–Medium | Severe | Encryption at rest/in transit, minimal retention, HIPAA/DPDP compliance, third-party audit pre-pilot | Security Lead |
| Model/data drift as new drugs enter market | Medium | Medium | Scheduled DrugBank/openFDA syncs; unmatched drugs routed to pharmacist, never silently ignored | ML Lead |
| Automation bias — patient over-trust | Medium | Medium–High | UX frames app as a support tool; persistent pharmacist escalation | UX Lead |
| Low adoption among low-digital-literacy patients | Medium | Medium | Multilingual/low-literacy UX from MVP; caregiver-assisted onboarding | UX Lead |

## Regulatory Timeline — Two Paths

| Path | Positioning | Planning-assumption timeline |
|---|---|---|
| A — Recommended | Non-SaMD wellness/adherence, mandatory human review | ~3–6 months, no FDA premarket clearance required |
| B — Avoided by design | Clinical decision support (SaMD) | 12+ months, 510(k)/De Novo submission |

*Illustrative planning assumptions — validate with regulatory counsel before committing to a launch date.*

## Escalation Trigger

Any single missed high-risk interaction that reaches a patient without pharmacist review triggers an **immediate incident review**, independent of the regular weekly/monthly/quarterly cadence.

## Review Cadence

- **Weekly** — clinical-quality review of pharmacist-audited alerts (Clinical Lead + ML Lead)
- **Monthly** — product/growth review of adherence, retention, alert-action metrics
- **Quarterly** — B2B pilot outcomes reviewed with Medical Affairs and BD
