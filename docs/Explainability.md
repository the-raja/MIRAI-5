# MIRAI v2 — Explainability (XAI) Engine Specification

## 1. Purpose
The **Explainability (XAI) Engine** merges multi-subsystem evidence into a unified `ReasoningTrace` and generates human-readable explanation cards.

---

## 2. Reasoning Trace Architecture

```mermaid
graph LR
    DECISION[Decision Cortex] --> REASON[Reasoning Engine]
    REASON --> EXPLANATION[Explanation Generator]
    EXPLANATION --> DEVTOOLS[Developer Tools]
    DEVTOOLS --> REPLAY[Replay Viewer]
```

---

## 3. Explanation Card Output

```text
====================================
Decision: Dash
====================================

Reasoning

Prediction
-------------
Reload (94%)

Threat
-------------
Healing = 0.91

Experience
-------------
Episode 102
Similarity 0.94

Skill Rating
-------------
Expert (92)

Planner
-------------
Plan A

Goal
-------------
Pressure Player

Utility
-------------
Dash: 0.88
Block: 0.63

Final Decision
-------------
Dash
====================================
```

---

## 4. Code Example

```python
from backend.cognitive_os.explainability.explanation_engine import ExplanationEngine

engine = ExplanationEngine()
trace = engine.merge_subsystem_trace(frame_index=24, final_decision="Dash")
print(engine.format_explanation_card(trace))
```
