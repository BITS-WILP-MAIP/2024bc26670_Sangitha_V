"""
ai_engine.py
The AI layer for MedGuardian AI.

Design note (for the product proposal's "staged automation" MVP strategy):
- If an ANTHROPIC_API_KEY environment variable is present, this module calls
  the real Claude API so the copilot gives genuinely generated explanations.
- If no key is set, it falls back to a deterministic, rule-based "simulated AI"
  so the MVP is fully demoable offline / without any credentials.
Both paths go through the SAME interaction-safety logic (mock_data.check_interactions),
so a human-reviewable, high-risk flag is never skipped just because the
generation layer changed \u2014 mirroring the human-in-the-loop design in the
product proposal.
"""

import os
from mock_data import MEDICATIONS_DB, check_interactions

MODEL_NAME = os.environ.get("MEDGUARDIAN_MODEL", "claude-sonnet-4-5")
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

_client = None
if API_KEY:
    try:
        import anthropic
        _client = anthropic.Anthropic(api_key=API_KEY)
    except Exception:
        _client = None


def _call_llm(system_prompt, user_prompt, max_tokens=400):
    """Call the real Claude API. Returns None on any failure so callers can fall back."""
    if not _client:
        return None
    try:
        resp = _client.messages.create(
            model=MODEL_NAME,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return "".join(block.text for block in resp.content if block.type == "text").strip()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Patient-facing AI copilot
# ---------------------------------------------------------------------------
COPILOT_SYSTEM_PROMPT = (
    "You are MedGuardian, a calm, plain-language medication safety assistant. "
    "You explain drug interactions and adherence in simple terms, you are never "
    "alarmist, you always suggest talking to a pharmacist for anything moderate "
    "or high risk, and you never give a dosing instruction. Keep answers under "
    "120 words."
)


def _rule_based_reply(user_message, patient_meds):
    msg = user_message.lower()

    # 1) Direct question about interactions among the patient's own medications
    if any(k in msg for k in ["interact", "safe to take", "together", "combination"]):
        hits = check_interactions(patient_meds)
        if not hits:
            return (
                "Based on your current medication list, I don't see any known "
                "interactions in my reference data. This isn't a substitute for "
                "your pharmacist's review \u2014 tap 'Talk to a pharmacist' if you'd like a human check."
            )
        lines = []
        for h in hits:
            a, b = h["pair"]
            lines.append(f"\u2022 **{a.title()} + {b.title()}** ({h['severity']} risk): {h['explanation']}")
        tail = "\n\nI'd recommend tapping 'Talk to a pharmacist' for anything above low risk."
        return "Here's what I found:\n\n" + "\n".join(lines) + tail

    # 2) Question naming a new/candidate drug not yet in the list
    for drug in MEDICATIONS_DB:
        if drug in msg and drug not in patient_meds:
            hits = check_interactions(patient_meds + [drug])
            relevant = [h for h in hits if drug in h["pair"]]
            if relevant:
                lines = [f"\u2022 {h['explanation']}" for h in relevant]
                return (
                    f"Adding **{drug.title()}** to your current list, here's what stands out:\n\n"
                    + "\n".join(lines)
                    + "\n\nPlease confirm with a pharmacist before starting it."
                )
            return (
                f"I don't see a known interaction between {drug.title()} and your current "
                f"medications in my reference data, but a pharmacist should still confirm "
                f"before you start anything new."
            )

    # 3) Adherence-related question
    if any(k in msg for k in ["forget", "missed", "remind", "adherence", "skip"]):
        return (
            "Missing an occasional dose happens \u2014 what matters is the pattern. "
            "I can send you a daily reminder at a time that fits your routine. "
            "If you've missed a dose today, check your medication's label for what "
            "to do, or tap 'Talk to a pharmacist' if you're unsure."
        )

    # 4) Fallback
    return (
        "I can help with two things: checking whether your medications interact "
        "safely, or helping you stay on track with reminders. Try asking me "
        "something like \u201cIs it safe to take ibuprofen with my medications?\u201d"
    )


def get_copilot_reply(user_message, patient_meds):
    """Patient-facing chat reply. Tries the real LLM first, falls back to rules."""
    context = (
        f"Patient's current medications: {', '.join(patient_meds)}.\n"
        f"Known interaction reference hits for this list: {check_interactions(patient_meds)}.\n"
        f"Patient message: {user_message}"
    )
    llm_reply = _call_llm(COPILOT_SYSTEM_PROMPT, context)
    if llm_reply:
        return llm_reply, "live-llm"
    return _rule_based_reply(user_message, patient_meds), "simulated"


# ---------------------------------------------------------------------------
# AI for Project Management Artifacts
# (the product's own roadmap / risk register / backlog, AI-summarized for
#  stand-ups and stakeholder updates)
# ---------------------------------------------------------------------------
PM_SYSTEM_PROMPT = (
    "You are an AI project-management assistant for a product team. Given "
    "structured roadmap, risk, or backlog data, write a concise, decision-useful "
    "status narrative a product manager could paste into a stakeholder update. "
    "Be specific about what changed and what needs a decision. Under 150 words."
)


def _rule_based_pm_summary(kind, data):
    if kind == "roadmap":
        lines = ["**Roadmap status summary (auto-generated):**"]
        for r in data:
            lines.append(
                f"- {r['phase']} ({r['window']}): {r['status']}, {r['pct_complete']}% complete \u2014 {r['focus']}"
            )
        active = [r for r in data if r["status"] == "In progress"]
        if active:
            lines.append(
                f"\n**Focus:** {active[0]['phase']} is the only active phase at {active[0]['pct_complete']}% "
                f"complete. No blockers currently logged against it."
            )
        return "\n".join(lines)

    if kind == "risk":
        lines = ["**Risk register summary (auto-generated):**"]
        high = [r for r in data if r["impact"] == "Severe"]
        lines.append(f"{len(data)} tracked risks, {len(high)} rated Severe impact.")
        for r in high:
            lines.append(f"- **{r['risk']}** (owner: {r['owner']}): {r['status']}")
        others = [r for r in data if r["impact"] != "Severe"]
        if others:
            lines.append("\nOther tracked risks: " + "; ".join(f"{r['risk']} ({r['status']})" for r in others))
        return "\n".join(lines)

    if kind == "backlog":
        lines = ["**Backlog summary (auto-generated):**"]
        done = [b for b in data if b["status"] == "Done"]
        in_prog = [b for b in data if b["status"] == "In progress"]
        not_started = [b for b in data if b["status"] == "Not started"]
        lines.append(f"{len(done)} done, {len(in_prog)} in progress, {len(not_started)} not started.")
        if in_prog:
            lines.append("**In progress:** " + ", ".join(b["item"] for b in in_prog))
        p0_remaining = [b for b in data if b["priority"] == "P0" and b["status"] != "Done"]
        if p0_remaining:
            lines.append("**P0 items still open:** " + ", ".join(b["item"] for b in p0_remaining))
        else:
            lines.append("All P0 (MVP-critical) items are complete.")
        return "\n".join(lines)

    return "No summary available for this artifact type."


def generate_pm_summary(kind, data):
    """kind: 'roadmap' | 'risk' | 'backlog'. Returns (summary_text, source)."""
    prompt = f"Artifact type: {kind}\nData: {data}"
    llm_reply = _call_llm(PM_SYSTEM_PROMPT, prompt)
    if llm_reply:
        return llm_reply, "live-llm"
    return _rule_based_pm_summary(kind, data), "simulated"


# ---------------------------------------------------------------------------
# AI for Pharma Program Insights
# (de-identified, aggregate Specialty Care Support Program data, summarized
#  for a pharma account/medical-affairs stakeholder — Section 13's closed loop)
# ---------------------------------------------------------------------------
PHARMA_SYSTEM_PROMPT = (
    "You are an AI assistant for a pharma manufacturer's patient support program (PSP) team. "
    "Given de-identified, aggregate adherence and safety-escalation data for a specialty drug "
    "program, write a concise, decision-useful narrative a medical-affairs or market-access "
    "stakeholder could use to assess program health and inform payer conversations. Never "
    "reference any individual patient. Under 150 words."
)


def _rule_based_pharma_summary(insights, trend):
    lines = ["**Specialty program summary (auto-generated, de-identified):**"]
    lines.append(
        f"{insights['enrolled_patients']} enrolled patients, {insights['avg_adherence_rate']} average adherence — "
        f"{insights['discontinuation_risk_high']} flagged high risk of discontinuation this period."
    )
    lines.append(
        f"Pharmacist review resolved {insights['interaction_flags_resolved_90d']} interaction flags and "
        f"{insights['pharmacist_escalations_90d']} escalations over the last 90 days, an estimated "
        f"{insights['est_doses_saved_90d']} doses preserved versus an unmanaged cohort."
    )
    start, end = trend[0], trend[-1]
    direction = "up" if end["adherence_pct"] >= start["adherence_pct"] else "down"
    lines.append(
        f"Adherence trended {direction} from {start['adherence_pct']}% in {start['month']} to "
        f"{end['adherence_pct']}% in {end['month']} — useful context for the next payer/PBM renewal conversation."
    )
    return "\n".join(lines)


def generate_pharma_insights_summary(insights, trend):
    """Returns (summary_text, source) for the de-identified pharma program dashboard."""
    prompt = f"Aggregate program data: {insights}\nAdherence trend: {trend}"
    llm_reply = _call_llm(PHARMA_SYSTEM_PROMPT, prompt)
    if llm_reply:
        return llm_reply, "live-llm"
    return _rule_based_pharma_summary(insights, trend), "simulated"
