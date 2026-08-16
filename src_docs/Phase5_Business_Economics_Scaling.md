# Phase 5 — Business, Economics & Scaling

## Monetization Model

| Model | Description |
|---|---|
| B2B2C — PMPM licensing (primary) | Health plans and PBMs pay a per-member-per-month fee to offer MedGuardian as part of a chronic-care management program — justified by measurable readmission-cost avoidance |
| Direct-to-consumer freemium | Core adherence reminders and low-risk interaction checks free; premium tier (caregiver dashboard, unlimited pharmacist chat) as a paid consumer subscription |
| API licensing | Pharmacy chains and EHR vendors license the interaction/adherence engine as an embedded feature via API, priced on usage volume |
| Specialty Pharma PSP program (Section 13 extension) | A flat annual platform fee or per-enrolled-patient fee, sold to a pharma manufacturer's Patient Support Program team for a specific specialty/biologic drug |

## Illustrative Revenue Model

Bottom-up, mapped to the roadmap's own phase milestones — **planning assumptions to be validated by real pilot conversations, not a forecast.**

| Stream | Pricing assumption |
|---|---|
| B2B2C PMPM | $1.50–$3.00 PMPM — typical range for chronic-care digital health point solutions |
| DTC freemium | ~$7/month premium, ~2–3% free-to-paid conversion |
| API licensing | ~$0.10/interaction-check call, volume-dependent |
| Specialty pharma PSP | $150K–$400K/year flat program fee, or ~$15–$30 PMPM |

| Year | Roadmap phase | Illustrative revenue |
|---|---|---|
| Year 1 | Phase 1–2: single-condition pilot, proving the 95% agreement bar | ~$0–$50K (validation stage, not revenue stage) |
| Year 2 | Phase 3: "≥1 signed PBM/insurer pilot" (the roadmap's own milestone) | ~$250K–$650K ARR |
| Year 3 | Phase 4: scale — multiple PBM contracts + first specialty pharma pilot | ~$1.5M–$1.8M ARR |

**The honest read:** this is a B2B sales-cycle business, not a viral consumer app. Year 1 revenue is realistically near zero because the point of Phase 1 is generating the clinical-agreement evidence a PBM will actually pay for — the freemium/DTC line is structurally the smallest stream unless user count reaches the hundreds of thousands.

## Why Specialty Pharma Changes the Calculus

A missed dose of a low-cost generic is a clinical risk. A missed dose or early discontinuation of a specialty biologic — often several thousand dollars per month — is both a clinical *and* a revenue event for the manufacturer. This is exactly why manufacturers already fund Patient Support Programs (PSPs) for their specialty products; MedGuardian's adherence/interaction core is directly reusable infrastructure for that existing spend. Value to a pharma company specifically:

- **Revenue retention** — early discontinuation-risk signals let a hub program intervene before a patient drops a specialty drug entirely
- **Payer negotiation leverage** — real-world adherence data strengthens value-based contracts
- **REMS support** — an auditable safety-monitoring layer helps satisfy FDA-mandated Risk Evaluation and Mitigation Strategies
- **Differentiated patient support** — a genuinely helpful, AI-assisted PSP is a retention lever independent of the drug's own efficacy

## Competitive Positioning

MedGuardian sits in **Specialized Triage and Patient Care**, but fills a gap none of the named comparable products cover:

- **Conversational/Contact-Center AI** (Hyro, Artera, Syllable, Cognigy) — channel/infrastructure plays, no domain-specific medication-safety logic.
- **Patient Access & Workflow** (Luma Health, Innovaccer, Azure Health Bot) — logistics (scheduling, intake), transactional, not a continuous safety relationship.
- **Specialized Triage** (Ada Health — symptom triage, Wysa — mental health, Cedar — billing) — each is a single-purpose specialist; **none of them do medication adherence or drug-interaction safety.**

MedGuardian's specific differentiators: a *quantified* graduation gate for automation (not just a review-step UI pattern), and a data path back to the drug manufacturer via the Specialty Pharma Extension — a business model none of the above products have.

## Scaling Path

Distribution deliberately targets pharmacy chains and PBMs/health plans (Phase 1–3), not hospital EHR integration — that channel carries its own separate 6–12 month procurement and security-review cycle on top of any regulatory timeline, and is deliberately deferred to Phase 4 after the product has already been validated through a lighter-weight channel.
