"""TournamentRunner module.

Step 3: Executes multi-match tournaments automatically:
- MIRAI vs Scripted AI (1000 Matches)
- MIRAI vs Random AI (1000 Matches)
- MIRAI vs Previous Version (1000 Matches)
"""

from typing import List, Dict, Any
from backend.cognitive_os.simulation.match_runner import MatchRunner
from backend.cognitive_os.simulation.scenario import BattleScenario


class TournamentRunner:
    def __init__(self) -> None:
        self.match_runner = MatchRunner()

    def run_tournament(
        self,
        mirai_version: str = "MIRAI v2 (Strategic Planner)",
        opponent_type: str = "Scripted AI",
        num_matches: int = 1000
    ) -> Dict[str, Any]:
        """Runs a tournament series of N matches against specified opponent AI across standard scenarios."""
        scenarios = BattleScenario.get_standard_scenarios()
        mirai_wins = 0
        total_duration = 0.0
        total_damage = 0.0

        for i in range(num_matches):
            scen = scenarios[i % len(scenarios)]
            res = self.match_runner.run_match(
                mirai_version=mirai_version,
                opponent_type=opponent_type,
                scenario=scen
            )

            if res["winner"] == "MIRAI":
                mirai_wins += 1
            total_duration += res["duration_sec"]
            total_damage += res["mirai_damage_dealt"]

        win_rate = round((mirai_wins / num_matches) * 100.0, 1)
        avg_dur = round(total_duration / num_matches, 2)
        avg_dmg = round(total_damage / num_matches, 1)

        return {
            "mirai_version": mirai_version,
            "opponent_type": opponent_type,
            "total_matches": num_matches,
            "mirai_wins": mirai_wins,
            "mirai_losses": num_matches - mirai_wins,
            "win_rate_pct": win_rate,
            "average_duration_sec": avg_dur,
            "average_damage_dealt": avg_dmg
        }
