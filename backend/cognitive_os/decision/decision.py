"""Decision data structure. Only data models, no logic."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time
from backend.cognitive_os.decision.goal import Goal
from backend.cognitive_os.decision.utility_action import UtilityAction
from backend.cognitive_os.decision.reasoning_trace import ReasoningTraceModel


class Decision(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"dec_{int(time.time()*1000)}")
    timestamp: float = Field(default_factory=time.time)
    goal: Goal
    chosen_action: UtilityAction
    utility_score: float = 0.0
    confidence: float = 0.85
    reasoning_trace: ReasoningTraceModel
    metadata: Dict[str, Any] = Field(default_factory=dict)
