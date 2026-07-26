"""MIRAI v2 — Phase 18 Explainability (XAI) Demonstrator Runner.

Executes ExplanationEngine:
Outputs the exact multi-subsystem reasoning trace explanation card.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.explainability.explanation_engine import ExplanationEngine


def run_xai_demo() -> None:
    engine = ExplanationEngine()

    trace = engine.merge_subsystem_trace(
        frame_index=24,
        prediction={"intent": "Reload", "confidence": 0.94},
        threat={"healing": 0.91},
        experience={"episode": "Episode 102", "similarity": 0.94},
        skill={"tier": "Expert", "score": 92},
        planner={"goal": "Pressure Player", "plan": "Plan A"},
        utility={"Dash": 0.88, "Block": 0.63},
        final_decision="Dash"
    )

    print("\n")
    card = engine.format_explanation_card(trace)
    print(card)
    print("\n")


if __name__ == "__main__":
    run_xai_demo()
