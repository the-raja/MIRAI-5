"""ReasoningTrace module.

Defines first-class ReasoningTrace schema encapsulating reasoning across all Cognitive OS subsystems:
Prediction, Threat, Experience, Skill, Planner, Utility AI, and Final Decision.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ReasoningTrace(BaseModel):
    frame_index: int = 1
    prediction: Dict[str, Any] = Field(default_factory=lambda: {"intent": "Reload", "confidence": 0.94})
    threat: Dict[str, float] = Field(default_factory=lambda: {"healing": 0.91})
    experience: Dict[str, Any] = Field(default_factory=lambda: {"episode": "Episode 102", "similarity": 0.94})
    skill: Dict[str, Any] = Field(default_factory=lambda: {"tier": "Expert", "score": 92})
    planner: Dict[str, Any] = Field(default_factory=lambda: {"goal": "Pressure Player", "plan": "Plan A"})
    utility: Dict[str, float] = Field(default_factory=lambda: {"Dash": 0.88, "Block": 0.63})
    final_decision: str = "Dash"
    reasoning_summary: str = "High player reload prediction (94%) and healing threat (0.91) triggered Plan A Dash."
