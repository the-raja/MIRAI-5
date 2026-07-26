"""MIRAI v2 — Phase 19 Demo Game & AI Debugger Vertical Slice Demonstrator Runner.

Executes 2D Combat Arena vertical slice demonstrator.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.developer_tools.replay_viewer import ReplayViewer
from backend.cognitive_os.explainability.explanation_engine import ExplanationEngine


def run_demo_game_summary() -> None:
    engine = ExplanationEngine()
    viewer = ReplayViewer()

    print("\n")
    print("====================================")
    print("MIRAI v2 Demo Game & AI Debugger Vertical Slice")
    print("====================================")

    print("\n1. 2D Combat Arena Layout:")
    print("   Player [HP: 100]  |  Boss AI [HP: 100]  |  Pillar Obstacle  |  Health Pack")

    print("\n2. Frame 130 AI Debugger Snapshot:")
    frame_snapshot = viewer.get_frame_state(frame_index=130)
    print(f"   Frame:               {frame_snapshot['frame_index']}")
    print(f"   Prediction:          {frame_snapshot['predictions']['fused_prediction']}")
    print(f"   Goal:                {frame_snapshot['plan']['goal']}")
    print(f"   Plan:                Plan A ({', '.join(frame_snapshot['plan']['actions'])})")
    print(f"   Threat:              Healing = 0.91")
    print(f"   Retrieved Memory:    {frame_snapshot['memories']['vector']}")
    print(f"   Chosen Boss Action:  {frame_snapshot['plan']['active_step']}")
    print("====================================\n")


if __name__ == "__main__":
    run_demo_game_summary()
