"""ThreatRanker module.

Ranks player actions/intents by Threat Score (0.00 -> 1.00).

Example output:
Ultimate: 0.95
Healing:  0.91
Reload:   0.28
Retreat:  0.16
"""

from typing import List, Dict, Any, Tuple, Optional
from backend.cognitive_os.threat.threat_model import XGBoostThreatModel


class ThreatRanker:
    def __init__(self, threat_model: Optional[XGBoostThreatModel] = None) -> None:
        self.threat_model = threat_model or XGBoostThreatModel()

    def rank_threats(
        self,
        candidate_actions: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[str, float]]:
        """Ranks candidate player intents by Threat Score (0.00 -> 1.00) in descending order."""
        actions = candidate_actions or ["Ultimate", "Healing", "Reload", "Retreat"]
        ctx = context or {"ultimate_charge": 0.95, "player_hp": 34.0}

        ranked: List[Tuple[str, float]] = []
        for act in actions:
            score = self.threat_model.evaluate_threat_score(act, ctx)
            ranked.append((act, round(score, 2)))

        ranked.sort(key=lambda x: -x[1])
        return ranked
