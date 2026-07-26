"""Knowledge data structure. Only data models, no logic."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class Knowledge(BaseModel):
    id: str
    type: str  # e.g. "PlayerReloadHabit", "PreferredWeapon", "PreferredDodge", "PanicThreshold", "EngagementRange"
    confidence: float = 0.5  # Confidence score [0.0 - 1.0]
    evidence_count: int = 1  # Number of supporting battles/episodes
    last_updated: float = Field(default_factory=time.time)
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
