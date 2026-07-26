"""Cognitive state data structures. Only data models, no logic."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from backend.cognitive_os.attention.salience import AttentionState


class CognitiveState(BaseModel):
    timestamp: float = 0.0
    attention: AttentionState = Field(default_factory=AttentionState)
    current_goal: Optional[str] = None
    current_target: Optional[str] = None
    emotion: str = "NEUTRAL"
    risk: float = 0.0
    confidence: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
