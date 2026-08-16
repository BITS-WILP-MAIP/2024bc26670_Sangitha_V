# Wireframes & Screens — MVP 1

**Note on this document:** these are text-based screen descriptions of what was actually built and verified running (via browser automation — `read_page`/`get_page_text`), not designer mockups or captured screenshots. This session's environment has no screenshot-compositing support. To get real screenshots for a presentation: run `mvp1` locally (`streamlit run dashboards/app.py`) and capture each screen directly — every layout and copy string below matches the live code exactly, so screenshots will match this description one-to-one.

## Screen 1 — Patient Dashboard

**Sidebar (dark, Sandoz Prussian Blue):** "💊 MedGuardian AI" wordmark, caption "MVP 1 — rules-based medication safety, no AI/LLM dependency," a 3-item navigation radio (Patient Dashboard / Pharmacist Review Queue / KPI Dashboard), a live alert-count badge, and a version/phase footer read from `config.yaml`.

**Main content, top to bottom:**
1. `Welcome back, Asha` + condition summary line (from config: "Type 2 diabetes with cardiometabolic comorbidities")
2. Three stat cards in a row: **Adherence (14 days)**, **Active medications**, **Open interaction alerts** — each a white card with a Denim-blue number
3. **Your medications** — one card per drug, showing name, drug class chip, and common-use text
4. **Add a new medication** — two tabs:
   - *📷 Scan label or bottle* — a file uploader ("Take a photo of your prescription label or pill bottle"), which reveals a confirm-match dropdown over the real FDA ingredient list once a file is uploaded
   - *🔍 Search manually* — a searchable dropdown over the same real ~2,300-ingredient list, with its own "Check & add" button
   - Selecting and confirming a drug either shows a green success card ("no known interaction"), or a colored risk card (amber/red) with the plain-language explanation and a note that it was routed to the pharmacist
5. **Today's check-in** — three buttons (✅ Taken / ❌ Skipped / ⏰ Remind me later); once logged today, this collapses to a confirmation message
6. **14-day adherence** — a Plotly bar chart, Denim bars for taken days, light grey for missed, updating live as check-ins are logged

## Screen 2 — Pharmacist Review Queue

Title `🧑‍⚕️ Pharmacist Review Queue` with a one-line explanation that every moderate/high-risk flag — including unmatched medications — lands here.

Each pending item is a card with a colored severity badge (MODERATE = amber, HIGH = red), the two drugs involved (or the unmatched drug name), the plain-language explanation, a status line, and two buttons: **Approve alert to patient** / **Dismiss (false positive)**. Acting on an item updates its status in place and re-renders the queue.

Empty-state: a green "Queue is empty" message when nothing is pending.

## Screen 3 — KPI Dashboard

Title `📊 KPI Dashboard`. Four stat cards, one per Phase 1 KPI (Medication adherence rate, Interaction alerts acted on, False-positive interaction rate, Pharmacist review turnaround) — each shows a current illustrative value and a threshold string **generated from `config.yaml`**, not hardcoded (e.g. "Threshold: ≥ 85%").

Below the cards: a status-summary table (KPI / Status), and a closing caption stating the Phase 2 graduation gate in full: "≥ 95% pharmacist agreement with flagged risk level, sustained over a 60-day pilot" — also sourced from config, not a hardcoded string.

## Verified Interaction (from browser testing)

Searching "Warfarin Sodium" (a real FDA salt-form name) → normalizes to "Warfarin" → detects the existing high-risk interaction with the patient's ibuprofen → displays the red HIGH RISK card with the correct explanation → adds the item to the Pharmacist Review Queue with the sidebar alert count updating from 1 to 2 → the queue page shows both the pre-existing Lisinopril+Ibuprofen (moderate) and the new Warfarin+Ibuprofen (high) items correctly.
