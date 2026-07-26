"""GoalDecomposer module.

Step 4: Hierarchical Goal Decomposition.
Decomposes high-level battle objectives into structured sub-goals:
WIN FIGHT -> Pressure Player -> Reduce HP -> Interrupt Reload -> Finish
"""

from typing import List, Dict, Any


class GoalDecomposer:
    @staticmethod
    def decompose_goal(high_level_goal: str) -> List[str]:
        """Decomposes a top-level objective into an ordered hierarchy of sub-goals."""
        hierarchy_map = {
            "WIN_FIGHT": [
                "Pressure Player",
                "Reduce HP",
                "Interrupt Reload",
                "Finish"
            ],
            "PRESSURE": [
                "Interrupt Reload",
                "Reduce HP",
                "Maintain Engagement"
            ],
            "DEFEND": [
                "Block Heavy Attacks",
                "Create Distance",
                "Recover Stamina"
            ]
        }

        normalized = high_level_goal.upper().replace(" ", "_")
        return hierarchy_map.get(normalized, ["Pressure Player", "Reduce HP", "Finish"])
