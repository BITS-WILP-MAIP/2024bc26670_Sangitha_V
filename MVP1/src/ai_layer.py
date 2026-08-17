"""Phase 2 preview — optional, live Claude integration.

MVP 1's safety-critical core (interaction_engine.py, drug_normalizer.py,
adherence.py) makes zero AI/LLM calls, by design — Section 11 / RICE P0.
This module is the one deliberate exception, added at the user's explicit
request to preview a Phase 2 capability (Section 2.1, GenAI explanation
layer) inside the MVP 1 build:

1. Turning dense, real FDA label interaction text into a plain-language
   table (used inline on the Patient Dashboard).
2. A general medication Q&A chatbot (used on the separate, clearly-labeled
   "Phase 2 Preview" page only — never on the core Phase 1 pages).

Neither path ever makes or overrides a safety decision — check_interactions()
in interaction_engine.py remains the sole source of truth for interaction
risk. Both paths fall back to a deterministic, non-LLM response when no
ANTHROPIC_API_KEY is configured, so the app stays fully demoable without
credentials — mirroring the live/fallback pattern already used in the
full-vision app's ai_engine.py.
"""

import os
import re

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODEL_NAME = os.environ.get("MEDGUARDIAN_MODEL", "claude-sonnet-5")
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

_client = None
if API_KEY:
    try:
        import anthropic
        _client = anthropic.Anthropic(api_key=API_KEY)
    except Exception:
        _client = None


def is_live():
    return _client is not None


def _call_llm(system_prompt, user_prompt, max_tokens=600):
    """Call the real Claude API. Returns None on any failure so callers fall back."""
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
# Layman-language summary table for real FDA label interaction text
# ---------------------------------------------------------------------------
SUMMARY_SYSTEM_PROMPT = (
    "You turn dense FDA drug-label 'Drug Interactions' text into a short, "
    "plain-language Markdown table for a patient, not a clinician. Columns: "
    "'Interacts with' | 'What can happen' | 'What to do'. One row per "
    "distinct interacting factor/drug/drug class named in the text. Keep "
    "each cell under 20 words, use everyday language, no dosing "
    "instructions. Output ONLY the Markdown table (header row, separator "
    "row, data rows) — no preamble, no closing remarks."
)


def _trim_words(text, max_words=8, max_chars=70):
    """Word-boundary-safe trim of the tail of `text` — never cuts mid-word."""
    words = text.strip().split()[-max_words:]
    kept, total = [], 0
    for w in reversed(words):
        total += len(w) + 1
        if total > max_chars:
            break
        kept.insert(0, w)
    return " ".join(kept)


def _rule_based_structured_rows(raw_text):
    """Reformat label text that follows the PLR 'Clinical Impact: ...
    Intervention: ... [Examples: ...]' structure into (factor, impact,
    action) rows. Returns None if that structure isn't present, so the
    caller can fall back to plain sentence bullets instead."""
    if "Clinical Impact:" not in raw_text:
        return None
    segments = raw_text.split("Clinical Impact:")
    rows = []
    for i in range(1, len(segments)):
        heading_source = segments[i - 1]
        last_period = heading_source.rfind(". ")
        heading_tail = heading_source[last_period + 2:] if last_period != -1 else heading_source
        heading = _trim_words(heading_tail) or f"Interacting factor {i}"
        body = segments[i]
        intervention_split = re.split(r"\bIntervention:\s*", body, maxsplit=1)
        impact_text = intervention_split[0].strip()
        rest = intervention_split[1] if len(intervention_split) > 1 else ""
        action_text = re.split(r"\bExamples?:\s*", rest, maxsplit=1)[0].strip()
        rows.append((heading, impact_text[:220], action_text[:220] or "Ask your pharmacist"))
    return rows


def _rule_based_sentence_bullets(raw_text, max_sentences=6):
    """Fallback of last resort for label text with no recognizable
    structure: just split into short, independently-readable sentences
    instead of one unbroken paragraph."""
    text = re.sub(r"^(Drug Interactions:?|DRUG INTERACTIONS)\s*", "", raw_text.strip())
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 15][:max_sentences]


def _parse_markdown_table(markdown_text):
    rows = []
    for line in markdown_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 3:
            continue
        if set("".join(cells)) <= {"-", " ", ":"}:
            continue  # the "| --- | --- | --- |" separator row
        if cells[0].lower() in ("interacts with",):
            continue  # the header row
        rows.append(tuple(cells))
    return rows


def summarize_interaction_text(raw_text):
    """Returns (rows, source). `rows` is a list of 3-tuples (factor, what
    can happen, what to do) when source is 'live-llm' or 'simulated-table',
    or a flat list of sentence strings when source is 'simulated-bullets'
    (label text with no structure to key off of)."""
    llm_reply = _call_llm(SUMMARY_SYSTEM_PROMPT, raw_text[:4000])
    if llm_reply:
        rows = _parse_markdown_table(llm_reply)
        if rows:
            return rows, "live-llm"
    structured = _rule_based_structured_rows(raw_text)
    if structured:
        return structured, "simulated-table"
    return _rule_based_sentence_bullets(raw_text), "simulated-bullets"


# ---------------------------------------------------------------------------
# Phase 2 preview chatbot — general medication Q&A (e.g. food interactions)
# ---------------------------------------------------------------------------
CHATBOT_SYSTEM_PROMPT = (
    "You are MedGuardian, a calm, plain-language medication safety assistant "
    "answering general questions (including food/drink/medication questions "
    "like grapefruit juice or alcohol) for a patient. Rules: never give a "
    "specific dosing instruction; never contradict or override a flagged "
    "interaction risk; always recommend confirming with a pharmacist for "
    "anything above low risk or when you are not confident; keep answers "
    "under 120 words; make clear you are not a substitute for professional "
    "medical advice."
)


def _rule_based_chat_reply(user_message):
    return (
        "This Phase 2 preview isn't connected to a live AI model right now "
        "(no ANTHROPIC_API_KEY configured for this session), so I can't "
        "generate a live answer to that question. In a real Phase 2 pilot "
        "this would be answered by Claude, using your medication list as "
        "context, always with a 'confirm with your pharmacist' safety net. "
        "Please ask your pharmacist directly for now."
    )


def get_chatbot_reply(user_message, patient_meds):
    """Returns (reply_text, source)."""
    context = (
        f"Patient's current medications: {', '.join(patient_meds) if patient_meds else '(none logged)'}.\n"
        f"Patient question: {user_message}"
    )
    llm_reply = _call_llm(CHATBOT_SYSTEM_PROMPT, context, max_tokens=300)
    if llm_reply:
        return llm_reply, "live-llm"
    return _rule_based_chat_reply(user_message), "simulated"
