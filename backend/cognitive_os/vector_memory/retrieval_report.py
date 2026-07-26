"""ExperienceRetrievalReportFormatter module.

Step 6: Formats and renders Experience Retrieval Console Reports:

==================================
Experience Retrieval
==================================
Current Situation
Player HP: 34%
Boss HP: 48%

Top Matches
Episode 102
Similarity 0.94
Winner: Boss

Episode 58
Similarity 0.91
Winner: Player

Episode 17
Similarity 0.89
Winner: Boss

Recommended Strategy
Pressure Player

Confidence
93%
==================================
"""

from typing import Dict, Any, List


class ExperienceRetrievalReportFormatter:
    @staticmethod
    def format_retrieval_report(retrieval_data: Dict[str, Any]) -> str:
        """Formats Experience Retrieval result into exact Step 6 console string."""
        sit = retrieval_data.get("current_situation", {})
        p_hp = int(sit.get("player_hp", 34.0))
        b_hp = int(sit.get("boss_hp", 48.0))
        matches = retrieval_data.get("top_matches", [])
        rec_strat = retrieval_data.get("recommended_strategy", "Pressure Player")
        conf = int(retrieval_data.get("confidence", 0.93) * 100)

        lines: List[str] = []
        lines.append("==================================")
        lines.append("Experience Retrieval")
        lines.append("==================================")
        lines.append("Current Situation")
        lines.append(f"Player HP: {p_hp}%")
        lines.append(f"Boss HP: {b_hp}%\n")

        lines.append("Top Matches")
        for m in matches:
            ep_ref = m.get("episode_reference", "Episode 102")
            sim = m.get("similarity_score", 0.94)
            winner = m.get("outcome", "Boss")
            lines.append(ep_ref)
            lines.append(f"Similarity {sim:.2f}")
            lines.append(f"Winner: {winner}\n")

        lines.append("Recommended Strategy")
        lines.append(rec_strat + "\n")

        lines.append("Confidence")
        lines.append(f"{conf}%")
        lines.append("==================================")

        return "\n".join(lines)

    @classmethod
    def print_retrieval_report(cls, retrieval_data: Dict[str, Any]) -> None:
        """Prints Experience Retrieval Console Report."""
        print(cls.format_retrieval_report(retrieval_data))
