"""Statistics module for Continuous Learning Engine.

Tracks research-grade continuous learning benchmark metrics:
- Prediction Accuracy
- Decision Accuracy
- Goal Accuracy
- Average Fight Time
- Average Damage
- Counter Success Rate
- Memory Growth
- Knowledge Growth
- Learning Speed
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class LearningStatistics(BaseModel):
    total_episodes_analyzed: int = 0
    prediction_accuracy: float = 0.0
    decision_accuracy: float = 0.0
    goal_accuracy: float = 0.0
    average_fight_time: float = 0.0
    average_damage: float = 0.0
    counter_success_rate: float = 0.0
    memory_growth: int = 0
    knowledge_growth: int = 0
    learning_speed: float = 0.0  # Adaptations generated per battle

    def update_metrics(
        self,
        prediction_acc: float = 0.74,
        decision_acc: float = 0.88,
        goal_acc: float = 0.85,
        fight_time: float = 82.0,
        damage_dealt: float = 450.0,
        counter_success: float = 0.80,
        current_memory_count: int = 1,
        current_knowledge_count: int = 4,
        adaptations_count: int = 2
    ) -> None:
        """Updates research benchmark metrics from a completed learning session."""
        self.total_episodes_analyzed += 1
        n = self.total_episodes_analyzed

        # Cumulative running averages
        self.prediction_accuracy = round(((self.prediction_accuracy * (n - 1)) + prediction_acc) / n, 4)
        self.decision_accuracy = round(((self.decision_accuracy * (n - 1)) + decision_acc) / n, 4)
        self.goal_accuracy = round(((self.goal_accuracy * (n - 1)) + goal_acc) / n, 4)
        self.average_fight_time = round(((self.average_fight_time * (n - 1)) + fight_time) / n, 2)
        self.average_damage = round(((self.average_damage * (n - 1)) + damage_dealt) / n, 2)
        self.counter_success_rate = round(((self.counter_success_rate * (n - 1)) + counter_success) / n, 4)

        # Growth metrics
        self.memory_growth = current_memory_count
        self.knowledge_growth = current_knowledge_count
        self.learning_speed = round(((self.learning_speed * (n - 1)) + float(adaptations_count)) / n, 2)

    def get_research_summary(self) -> Dict[str, Any]:
        """Returns research metrics dictionary for academic benchmark logging."""
        return {
            "Total Battles Analyzed": self.total_episodes_analyzed,
            "Prediction Accuracy": f"{self.prediction_accuracy * 100:.1f}%",
            "Decision Accuracy":   f"{self.decision_accuracy * 100:.1f}%",
            "Goal Accuracy":       f"{self.goal_accuracy * 100:.1f}%",
            "Average Fight Time":  f"{self.average_fight_time:.1f}s",
            "Average Damage":      f"{self.average_damage:.1f}",
            "Counter Success":     f"{self.counter_success_rate * 100:.1f}%",
            "Memory Growth":       f"{self.memory_growth} items",
            "Knowledge Growth":    f"{self.knowledge_growth} rules",
            "Learning Speed":      f"{self.learning_speed} adaptations/match"
        }
