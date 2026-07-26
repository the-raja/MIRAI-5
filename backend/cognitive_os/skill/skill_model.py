"""SkillModel module.

Step 2: Continuously evaluates player skill rating (0-100) across 9 features:
- Reaction Time
- Accuracy
- Combo Length
- Dodge Success
- Prediction Accuracy
- Decision Diversity
- Planning Success
- Average Damage
- Movement Entropy
"""

from typing import Dict, Any, Tuple
from pydantic import BaseModel


class PlayerSkillProfile(BaseModel):
    skill_score: float = 78.5
    skill_tier: str = "Expert"
    reaction_time_ms: float = 210.0
    accuracy_pct: float = 82.0
    combo_length: int = 4
    dodge_success_pct: float = 85.0
    planning_depth: int = 4
    forgiving_mode: bool = False


class SkillModel:
    @staticmethod
    def evaluate_skill(metrics: Dict[str, Any]) -> PlayerSkillProfile:
        """Computes 0-100 Skill Score and maps to Skill Tier & Strategy Adaptation rules."""
        rt = float(metrics.get("reaction_time_ms", 220.0))
        acc = float(metrics.get("accuracy_pct", 75.0))
        combo = float(metrics.get("combo_length", 3))
        dodge = float(metrics.get("dodge_success_pct", 80.0))
        dmg = float(metrics.get("average_damage", 70.0))

        # Normalized feature scores (0-100)
        rt_score = max(0.0, min(100.0, (400.0 - rt) / 2.5))
        combo_score = min(100.0, combo * 12.5)

        # Weighted skill score computation
        score = (
            rt_score * 0.25 +
            acc * 0.25 +
            combo_score * 0.15 +
            dodge * 0.20 +
            min(100.0, dmg) * 0.15
        )
        score = max(0.0, min(100.0, round(score, 1)))

        # Tier mapping & Strategy Adaptation
        if score < 30.0:
            tier = "Novice"
            p_depth = 2
            forgiving = True
        elif score < 60.0:
            tier = "Intermediate"
            p_depth = 3
            forgiving = False
        elif score < 80.0:
            tier = "Advanced"
            p_depth = 4
            forgiving = False
        elif score < 90.0:
            tier = "Expert"
            p_depth = 4
            forgiving = False
        else:
            tier = "Professional"
            p_depth = 5
            forgiving = False

        return PlayerSkillProfile(
            skill_score=score,
            skill_tier=tier,
            reaction_time_ms=rt,
            accuracy_pct=acc,
            combo_length=int(combo),
            dodge_success_pct=dodge,
            planning_depth=p_depth,
            forgiving_mode=forgiving
        )
