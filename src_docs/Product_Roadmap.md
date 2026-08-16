# Product Roadmap

| Phase | Timeframe | Focus | Key Milestone |
|---|---|---|---|
| **Phase 1 — MVP** | Months 1–4 | Rules-based interaction engine + adherence reminders for a single condition (diabetes/cardiac), pharmacist-reviewed alerts, one language | 60-day pilot with a single clinic or small patient cohort; ≥95% pharmacist agreement with AI risk flags |
| **Phase 2 — GenAI layer & expansion** | Months 5–8 | Plain-language explanation generation for low-risk alerts; multi-condition support; multilingual UX | False-positive rate < 5% on low-risk auto-sent alerts, validated by pharmacist audit |
| **Phase 3 — B2B distribution** | Months 9–14 | PBM/health-plan pilot program; caregiver dashboard; formal regulatory review for target market | ≥1 signed PBM/insurer pilot with measurable readmission-proxy improvement |
| **Phase 4 — Scale & integration** | Months 15+ | EHR/pharmacy-system API integration; personalized adherence-risk prediction model | Embedded as a feature inside ≥1 partner pharmacy or insurer platform |

## Feature-to-Phase Mapping

| Feature | Ships in |
|---|---|
| Barcode/photo medication capture | Phase 1 |
| Rules-based interaction engine | Phase 1 |
| Daily adherence check-in | Phase 1 |
| Pharmacist review queue | Phase 1 |
| GenAI plain-language explanations | Phase 2 |
| Caregiver dashboard | Phase 2 |
| Multilingual / low-literacy UX | Phase 2 |
| Specialty Pharma Extension (Physician View, Pharma Program Insights) | Phase 3+ |
| Personalized adherence-risk prediction | Phase 4 |
| EHR / pharmacy system integration | Phase 4 |

## Sequencing Logic

Distribution deliberately front-loads pharmacy chains and PBMs/health plans (Phase 1–3) ahead of hospital EHR integration (Phase 4) — the EHR channel carries its own 6–12 month procurement and security-review cycle independent of product readiness, so it's sequenced *after* the product has already been validated through a lighter-weight channel, not before.
