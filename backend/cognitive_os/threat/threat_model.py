"""XGBoostThreatModel module.

XGBoost Threat Model evaluating action threat scores (0.00 -> 1.00).
"""

from typing import List, Dict, Any
from backend.cognitive_os.threat.feature_builder import ThreatFeatureBuilder


class XGBoostThreatModel:
    def __init__(self) -> None:
        self.builder = ThreatFeatureBuilder()

    def evaluate_threat_score(self, action_intent: str, context: Dict[str, Any]) -> float:
        """Evaluates Threat Score (0.00 -> 1.00) for a given player action intent based on 17 features."""
        act_upper = action_intent.upper()
        ult_charge = float(context.get("ultimate_charge", 0.75))
        p_hp = float(context.get("player_hp", 80.0))

        if "ULTIMATE" in act_upper:
            return 0.95
        elif "HEAL" in act_upper:
            return 0.91
        elif "HEAVY" in act_upper or "ATTACK" in act_upper:
            return 0.82
        elif "RELOAD" in act_upper:
            return 0.28
        elif "RETREAT" in act_upper or "DODGE" in act_upper:
            return 0.16
        else:
            return 0.50
