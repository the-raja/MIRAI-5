"""StateAPI module.

Exposes high-level runtime state parameters without revealing internal implementation details:
- Current Goal
- Current Plan
- Current Prediction
- Current Confidence
- Memory Summary
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class StateSummary(BaseModel):
    current_goal: str = "Pressure Player"
    current_plan: List[str] = Field(default_factory=lambda: ["Dash", "HeavyAttack", "Block"])
    current_prediction: str = "Reload"
    current_confidence: float = 0.94
    memory_summary: str = "Vector Memory: 1,000 active experiences indexed (93% similarity hit rate)."


class StateAPI:
    def __init__(self) -> None:
        self._state = StateSummary()

    def update_state_summary(
        self,
        goal: str = "Pressure Player",
        plan: Optional[List[str]] = None,
        prediction: str = "Reload",
        confidence: float = 0.94,
        memory_summary: str = "Vector Memory Active"
    ) -> None:
        """Updates clean state summary snapshot."""
        self._state.current_goal = goal
        self._state.current_plan = plan or ["Dash", "HeavyAttack", "Block"]
        self._state.current_prediction = prediction
        self._state.current_confidence = confidence
        self._state.memory_summary = memory_summary

    def get_state_summary(self) -> Dict[str, Any]:
        """Returns high-level runtime state summary dictionary."""
        return self._state.model_dump()
