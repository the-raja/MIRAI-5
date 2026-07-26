"""BaselinePredictor module.

Predicts target player actions (Reload, Dodge, Heal, Attack, Retreat, Block) using:
- Frequencies
- Recent action history
- Semantic memory habits

Contains NO ML—pure statistical and rule-based baseline prediction.
"""

from typing import List, Optional, Dict
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.prediction.predictor_interface import IPredictor
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager


class BaselinePredictor(IPredictor):
    SUPPORTED_PREDICTIONS = ["Reload", "Dodge", "Heal", "Attack", "Retreat", "Block"]

    def __init__(self) -> None:
        self.frequency_table: Dict[str, Dict[str, float]] = {
            "Attack": {"Attack": 0.50, "Reload": 0.35, "Dodge": 0.15},
            "Reload": {"Attack": 0.70, "Dodge": 0.20, "Retreat": 0.10},
            "Dodge": {"Attack": 0.60, "Retreat": 0.25, "Block": 0.15},
            "Block": {"Attack": 0.50, "Retreat": 0.30, "Heal": 0.20}
        }

    def predict(
        self,
        recent_actions: List[str],
        memory_manager: Optional[MemoryManager] = None,
        semantic_manager: Optional[SemanticManager] = None,
        current_time: float = 0.0
    ) -> Prediction:
        """Predicts the next probable event among (Reload, Dodge, Heal, Attack, Retreat, Block)."""
        if not recent_actions:
            return Prediction(
                prediction_id=f"pred_{int(current_time*1000)}",
                timestamp=current_time,
                action="Attack",
                confidence=0.50,
                time_horizon=2.0,
                reason="Default baseline prior frequency probability",
                source="Baseline Frequency Table"
            )

        last_action = recent_actions[-1]
        recent_attack_streak = 0
        for act in reversed(recent_actions):
            if "Attack" in act:
                recent_attack_streak += 1
            else:
                break

        # 1. Rule: Reload (3+ consecutive attacks)
        if recent_attack_streak >= 3:
            return Prediction(
                prediction_id=f"pred_{int(current_time*1000)}",
                timestamp=current_time,
                action="Reload",
                confidence=0.74,
                time_horizon=2.0,
                reason=f"Player reloads after {recent_attack_streak} attacks.",
                source="Semantic Memory"
            )

        # 2. Rule: Dodge (Semantic Memory habit match)
        if semantic_manager:
            k_dodge = semantic_manager.memory.get_knowledge_by_type("PreferredDodge")
            if k_dodge and k_dodge.confidence >= 0.80 and last_action == "Attack":
                return Prediction(
                    prediction_id=f"pred_{int(current_time*1000)}",
                    timestamp=current_time,
                    action="Dodge",
                    confidence=k_dodge.confidence,
                    time_horizon=1.5,
                    reason=f"Player exhibits known dodge habit after attacking.",
                    source="Semantic Memory"
                )

        # 3. Rule: Heal (Working Memory low HP trigger)
        if memory_manager:
            time_since_damage = memory_manager.time_since_event("PlayerTookDamage", current_time=current_time)
            if time_since_damage is not None and time_since_damage < 2.0 and last_action in ("Dodge", "Retreat"):
                return Prediction(
                    prediction_id=f"pred_{int(current_time*1000)}",
                    timestamp=current_time,
                    action="Heal",
                    confidence=0.75,
                    time_horizon=3.0,
                    reason="Player took damage recently and disengaged to heal.",
                    source="Working Memory"
                )

        # 4. Rule: Retreat (Disengage after Dodge)
        if last_action == "Dodge":
            return Prediction(
                prediction_id=f"pred_{int(current_time*1000)}",
                timestamp=current_time,
                action="Retreat",
                confidence=0.65,
                time_horizon=2.0,
                reason="Player dodged and is retreating to safe distance.",
                source="Baseline Frequency Table"
            )

        # 5. Rule: Block (If last action was Block)
        if last_action == "Block":
            return Prediction(
                prediction_id=f"pred_{int(current_time*1000)}",
                timestamp=current_time,
                action="Attack",
                confidence=0.60,
                time_horizon=1.0,
                reason="Player blocked and counter-attack is expected.",
                source="Baseline Frequency Table"
            )

        # 6. Fallback: Frequency matrix for Attack
        frequencies = self.frequency_table.get(last_action, {"Attack": 0.60})
        next_event, prob = max(frequencies.items(), key=lambda x: x[1])

        return Prediction(
            prediction_id=f"pred_{int(current_time*1000)}",
            timestamp=current_time,
            action=next_event,
            confidence=prob,
            time_horizon=2.0,
            reason=f"Frequency matrix prior P({next_event} | {last_action}) = {prob:.2f}",
            source="Baseline Frequency Table"
        )
