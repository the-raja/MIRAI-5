# MIRAI v2 — Frequently Asked Questions (FAQ)

### Q1: What makes MIRAI different from traditional Game AI?
Traditional game AI relies on static rule scripts or hardcoded state machines. MIRAI is a **Cognitive OS** integrating working memory, continuous XGBoost intent prediction, 17-feature threat ranking, player skill adaptation, HTN + Behavior Tree planning, and multi-subsystem Explainable AI (XAI) reasoning traces.

### Q2: Does MIRAI support engines like Unreal Engine 5 or Unity?
Yes! MIRAI includes multi-language SDKs (`C#` for Unity, `C++` for Unreal Engine 5, `Python`, `JavaScript`) and swappable plugin packages in `plugins/`.

### Q3: How fast is MIRAI's decision latency?
MIRAI's single 7-stage tick pipeline runs in **4.2 ms** on average, making it suitable for 60 FPS real-time combat games.

### Q4: Can I swap out the memory store or ML models?
Yes. The plugin ecosystem allows developers to swap Prediction backends (`XGBoost`, `Transformer`, `RuleBased`), Planners (`A*`, `BeamSearch`, `GOAP`, `HTN`), and Memory stores (`FAISS`, `HNSW`, `SQLite`).

### Q5: How do I view the real-time AI thinking panel?
Open `frontend/index.html` in any modern web browser or launch the Developer Tools visualization suite via `python scripts/run_dev_tools.py`.
