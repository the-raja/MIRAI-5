"""MIRAI v2 — Advanced Decision Intelligence: Threat Ranking Demonstrator Runner.

Executes 17-feature XGBoost Threat Ranking:
Outputs the exact Threat Ranking console report card.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.threat.threat_ranker import ThreatRanker
from backend.cognitive_os.threat.threat_report import ThreatReportFormatter


def run_threat_demo() -> None:
    ranker = ThreatRanker()

    context = {
        "player_hp": 34.0,
        "boss_hp": 48.0,
        "distance": 4.5,
        "ultimate_charge": 0.95,
        "recent_aggression": 0.85
    }

    candidate_intents = ["Ultimate", "Healing", "Reload", "Retreat"]
    ranked_threats = ranker.rank_threats(candidate_actions=candidate_intents, context=context)

    print("\n")
    ThreatReportFormatter.print_threat_report(ranked_threats)
    print("\n")


if __name__ == "__main__":
    run_threat_demo()
