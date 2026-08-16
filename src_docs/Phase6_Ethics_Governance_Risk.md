# Phase 6 — Ethics, Governance & Risk

## Regulatory Positioning

**Target classification:** MVP 1 is deliberately positioned as a **non-SaMD** (Software as a Medical Device) wellness and adherence tool with clinician-facing decision support — never an autonomous diagnostic. Under FDA/IMDRF guidance, software only qualifies as SaMD when it independently produces a medical conclusion. Every moderate- or high-risk output stays behind a mandatory pharmacist review, and the product never issues an autonomous treatment recommendation — the design choice that keeps it on the lighter side of that line.

| Path | Positioning | Planning-assumption timeline |
|---|---|---|
| **A — Recommended for MVP 1** | Non-SaMD wellness/adherence tool, mandatory human review | No FDA premarket clearance required; ~3–6 months, dominated by internal safety/privacy review |
| **B — Avoided by design** | AI alerts framed as autonomous clinical judgment | 510(k)/De Novo submission; commonly 12+ months end-to-end before any sales cycle even starts |

*These are illustrative planning assumptions, not confirmed FDA timelines — validate with regulatory counsel before committing to a launch date.*

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Missed/incorrect high-risk interaction reaches a patient unreviewed | Low (with MVP design) | Severe | Mandatory pharmacist review of all high-risk flags; conservative over-flagging; incident-review process |
| Regulatory classification as a medical device (SaMD) | Medium | High | Early regulatory counsel; MVP 1 built as decision-support with mandatory human review, not autonomous diagnosis |
| Health data privacy breach | Low–Medium | Severe | Encryption at rest/in transit, minimal retention, HIPAA/DPDP compliance, third-party security audit pre-pilot |
| Model/data drift as new drugs or generics enter the market | Medium | Medium | Scheduled DrugBank/openFDA syncs; unmatched medications routed to a pharmacist, never silently ignored |
| Automation bias — patients over-trust the app | Medium | Medium–High | UX frames the app as a support tool with persistent pharmacist escalation and periodic prescriber-review reminders |
| Low adoption among lower digital-literacy or non-English-speaking patients | Medium | Medium | Multilingual & low-literacy UX from MVP; caregiver-assisted onboarding; usability testing with the target demographic |

## Ethical Impact Note

**Possible unintended consequences:**
- **Bias** — interaction and adherence models trained/validated primarily on younger, English-speaking, higher-digital-literacy data may underperform for elderly, non-English-speaking, or low-literacy patients — exactly the group most affected by polypharmacy.
- **Privacy** — medication data is highly sensitive; aggregation with adherence and pharmacy-pickup location data raises re-identification risk if not tightly scoped.
- **Job displacement / role shift** — pharmacists could be perceived as being replaced, when the design intends to augment their capacity by pre-triaging low-risk cases.
- **Over-reliance** — patients may substitute the app's guidance for professional medical advice, especially for ambiguous or borderline-risk cases.

**Steps for fairness, inclusivity, and responsible data use:**
- Validate interaction and adherence models across age, language, and literacy subgroups before launch, and report subgroup performance — not just an aggregate number.
- Offer multilingual, low-literacy, and caregiver-assisted UX modes from MVP, not as a later add-on.
- Position the pharmacist as the explicit escalation authority; involve practicing pharmacists in design and MVP-1 review.
- Collect only the data needed for the use case, with explicit opt-in consent, clear retention limits, and a user-facing deletion option.
- Never let the automated path show a high-risk or low-confidence alert without human review — per the staged-automation design.

## Specialty Pharma Extension — Additional Risk Considerations

Extending data visibility to a physician and, in aggregate, to a pharma manufacturer introduces risk beyond the register above: physician-facing data must be scoped to a clinician's own patients under existing care-relationship consent, and any pharma-facing feed must be irreversibly de-identified and aggregated — never event-level or re-identifiable — with a data-governance and legal review before any pharma pilot launches. This is a direct extension of the fairness commitments above, not a departure from them.

See `Risk_Note.md` for a condensed, standalone version of this register.
