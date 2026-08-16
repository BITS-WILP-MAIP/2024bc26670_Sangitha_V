# Phase 2 — PM Artifact Pack

## Customer Segmentation

**Segmentation objective:** decide which user group to design the MVP around, and which channel to prioritize for go-to-market.

| Segment | Defining Traits | Needs | Economics | Behavior |
|---|---|---|---|---|
| Polypharmacy patients (primary) | Age 45–75, 3+ chronic-condition prescriptions | Simple, low-effort dose reminders; plain-language interaction warnings; reassurance, not alarm | Low direct willingness-to-pay; pays indirectly via insurer/PBM program | Moderate smartphone comfort; high trust in pharmacist/doctor over app alone |
| Family caregivers | Adult children managing meds for an elderly parent, often remotely | Visibility into parent's adherence; alerts they can act on | Will pay a modest subscription directly | Highly engaged, checks app daily |
| Health plans / PBMs (B2B channel) | Bear the cost of avoidable readmissions | Measurable reduction in adverse events; auditable safety logs | PMPM contracts; strong willingness to pay for proven outcomes | Procurement-driven; needs pilot data before scaling |
| Newly diagnosed chronic patients | Just started a new chronic prescription | Education-heavy onboarding; highest attention window | Acquisition moment for the B2C funnel | High initial engagement, adherence risk drops over first 90 days |

**Priority:** Polypharmacy patients (1 — core end user) and Health plans/PBMs (1 — go-to-market channel) are co-primary. Design the core experience around the patient; build MVP 1's clinical-safety and reporting features to satisfy the buyer who funds it.

## Jobs-to-Be-Done

1. *"When I get a new prescription, help me understand quickly and calmly whether it's safe to take with what I already take, so I don't have to call three different doctors to find out."*
2. *"When I'm juggling multiple daily medications, remind me in a way that fits my routine, so I don't forget a dose or double up."*
3. *"When something looks risky, tell me clearly what to do next and who to talk to, so I feel supported, not just alarmed."*

## Product Vision

Become the trusted layer between "what my doctor prescribed" and "what I actually take," reducing preventable harm from polypharmacy — delivered first as a consumer companion app, then embedded as an API/feature inside pharmacy, insurer, and EHR platforms.

## MVP Strategy — Staged Automation

| Stage | Automated | Human-Reviewed | Trigger to Progress |
|---|---|---|---|
| MVP 1 | Interaction lookup + adherence reminders (rules-based, deterministic) | All high-risk interaction alerts | ≥ 95% pharmacist agreement over a 60-day pilot |
| MVP 2 | Low-risk explanations generated and sent automatically | High-risk alerts + low-confidence GenAI output | False-positive rate < 5% on low-risk alerts |
| Scale | Personalized adherence-risk prediction | Random audit + all model-flagged edge cases | Sustained accuracy + completed clinical/regulatory review |

## RICE Feature Prioritization

| Feature | Reach | Impact | Confidence | Effort | Priority |
|---|---|---|---|---|---|
| Barcode/photo medication capture | High | High | High | Medium | **P0 — MVP** |
| Interaction alert (rules-based + pharmacist review) | High | High | High | Medium | **P0 — MVP** |
| Daily adherence check-in & reminders | High | Medium | High | Low | **P0 — MVP** |
| GenAI plain-language explanations | High | Medium | Medium | Medium | P1 — Fast follow |
| Caregiver dashboard | Medium | Medium | Medium | Medium | P1 |
| Personalized adherence-risk prediction | Medium | High | Low (needs data) | High | P2 — Scale phase |
| EHR/pharmacy system integration (API) | Low→High long-term | High | Low | High | P2 — Scale phase |

See `Product_Roadmap.md` for the phase-by-phase timeline these priorities map to.
