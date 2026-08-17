# Prototype — README / Link

The runnable prototype lives in two places in this repository, scoped differently on purpose:

## MVP 1 — `../mvp1/`

The strictly-scoped Phase 1 build. Zero AI/LLM dependency. Config-driven, modular, tested.

```bash
cd mvp1
pip install -r requirements.txt
streamlit run dashboards/app.py
```

```bash
cd mvp1
pytest tests/ -v      # 25 tests, all passing
```

Full README: `../mvp1/README.md`. Full spec: `../MVP1_Specification.docx`.

## Full-Vision Demo — project root

The complete product vision, including the GenAI copilot, the Physician View, and Pharma Program Insights (Section 13, Specialty Pharma Extension). This is **not** what ships first — see `Product_Roadmap.md` for what belongs to which phase.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Optional: set `ANTHROPIC_API_KEY` to enable live Claude API calls for the GenAI copilot and PM-artifact summaries. Without it, the app falls back to a deterministic rule-based "simulated AI" automatically — both paths run through the same interaction-safety check, so the fallback never bypasses pharmacist review.

Full README: `../README.md`.

## Which One Should You Run?

| If you want to see... | Run |
|---|---|
| Exactly what would ship first, and why it's scoped that way | `mvp1/` |
| The full product ambition — GenAI, specialty pharma loop, AI-generated PM reporting | project root `app.py` |
