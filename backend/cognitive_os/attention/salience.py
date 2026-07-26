"""Attention and salience event data structures. Only data models, no logic."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SalienceEvent(BaseModel):
    event_id: str
    target_id: Optional[str] = None
    saliency_score: float = 0.0
    reason: str = ""
    timestamp: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AttentionState(BaseModel):
    timestamp: float = 0.0
    primary_target_id: Optional[str] = None
    priority_targets: List[str] = Field(default_factory=list)
    salient_events: List[SalienceEvent] = Field(default_factory=list)
    focus_score: float = 1.0
