"""MIRAI v2 — Phase 12 Vector Memory & Experience Retrieval Demonstrator Runner.

Executes experience vector retrieval over past battle memories:
Outputs the exact Experience Retrieval console report.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.vector_memory.retrieval_engine import ExperienceRetrievalEngine
from backend.cognitive_os.vector_memory.retrieval_report import ExperienceRetrievalReportFormatter


def run_vector_memory_demo() -> None:
    retrieval_engine = ExperienceRetrievalEngine()

    current_situation = {
        "player_hp": 34.0,
        "boss_hp": 48.0,
        "distance": 4.5,
        "aggression_score": 0.82
    }

    retrieval_data = retrieval_engine.query_experiences(current_situation, top_k=3)

    print("\n")
    ExperienceRetrievalReportFormatter.print_retrieval_report(retrieval_data)
    print("\n")


if __name__ == "__main__":
    run_vector_memory_demo()
