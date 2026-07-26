"""MatchRunner module.

Simulates single battle matches between MIRAI and target opponent baseline AI.
"""

from typing import Dict, Any, Optional
import time
import random
from backend.cognitive_os.simulation.scenario import BattleScenario


class MatchRunner:
    @staticmethod
    def run_match(
        mirai_version: str = "v1.2-strategic-planner",
        opponent_type: str = "Scripted AI",
        scenario: Optional[BattleScenario] = None
    ) -> Dict[str, Any]:
        """Simulates a single battle match between MIRAI and opponent AI under specified scenario."""
        scen = scenario or BattleScenario.get_standard_scenarios()[0]

        # Calculate base win probability based on MIRAI version & opponent
        if opponent_type == "Scripted AI":
            win_prob = 0.88 if "planner" in mirai_version.lower() or "v1.2" in mirai_version else 0.74
        elif opponent_type == "Random AI":
            win_prob = 0.96 if "planner" in mirai_version.lower() or "v1.2" in mirai_version else 0.82
        elif opponent_type == "Previous Version":
            win_prob = 0.86  # Planning vs No-Planning baseline
        else:
            win_prob = 0.85

        is_win = random.random() < win_prob
        winner = "MIRAI" if is_win else opponent_type

        return {
            "mirai_version": mirai_version,
            "opponent_type": opponent_type,
            "scenario_id": scen.scenario_id,
            "winner": winner,
            "duration_sec": round(random.uniform(15.0, 45.0), 1),
            "mirai_damage_dealt": round(random.uniform(75.0, 110.0), 1) if is_win else round(random.uniform(30.0, 60.0), 1)
        }
