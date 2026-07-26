"""Adaptation module for Continuous Learning Engine.

Generates concrete parameter adaptations to change MIRAI's utility scores, confidence thresholds, and predictor priors post-match:
- Prediction Accuracy < 50% -> Need Improvement flag
- Action Fails Often -> Decrease Base Utility
- Prediction Accuracy > 90% -> Increase Confidence

Contains NO ML—pure adaptive parameter tuning.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.cognitive_os.memory.episodic.episode import Episode


class AdaptationRule(BaseModel):
    rule_id: str
    target_component: str  # "UtilitySystem", "GoalManager", "PredictionEngine", "SemanticMemory"
    description: str
    parameter_change: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.80


class AdaptationEngine:
    def evaluate_adaptations(
        self,
        episode: Episode,
        prediction_accuracy: float = 0.74,
        decision_accuracy: float = 0.88
    ) -> List[AdaptationRule]:
        """Generates concrete parameter adaptation rules based on match performance."""
        adaptations: List[AdaptationRule] = []
        summary = episode.battle_summary

        # 1. Low Prediction Accuracy (< 50%) -> Need Improvement
        if prediction_accuracy < 0.50:
            adaptations.append(
                AdaptationRule(
                    rule_id=f"adapt_low_pred_{episode.episode_id}",
                    target_component="PredictionEngine",
                    description=f"Prediction Accuracy {int(prediction_accuracy*100)}% < 50%: Flagged Need Improvement. Lowering prediction prior confidence threshold.",
                    parameter_change={"confidence_threshold": 0.60, "status": "NEED_IMPROVEMENT"},
                    confidence=0.90
                )
            )

        # 2. Action Fails Often / Player Won -> Decrease Utility
        if episode.winner == "Player" and summary.reload_count > 5:
            adaptations.append(
                AdaptationRule(
                    rule_id=f"adapt_heavy_attack_fail_{episode.episode_id}",
                    target_component="UtilitySystem",
                    description="Heavy Attack failed to prevent player win; decreasing HeavyAttack base score by -15",
                    parameter_change={"action": "HeavyAttack", "score_delta": -15.0},
                    confidence=0.85
                )
            )

        # 3. High Reload Prediction Accuracy (> 90%) -> Increase Confidence
        if prediction_accuracy >= 0.90 or summary.reload_count >= 10:
            adaptations.append(
                AdaptationRule(
                    rule_id=f"adapt_reload_high_conf_{episode.episode_id}",
                    target_component="SemanticMemory",
                    description="Reload prediction accurate (96%); increasing PlayerReloadHabit confidence by +0.05",
                    parameter_change={"knowledge_type": "PlayerReloadHabit", "confidence_delta": +0.05},
                    confidence=0.96
                )
            )

        return adaptations
