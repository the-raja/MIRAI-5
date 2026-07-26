"""Goal data structure. Only data models, no logic."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import time


class Goal(BaseModel):
    id: str
    type: str  # e.g. "PRESSURE_PLAYER", "ATTACK", "RETREAT", "HEAL", "OBSERVE", "TAKE_COVER", "FLANK", "WAIT", "FINISH_ENEMY"
    priority: float = 0.5  # Priority score [0.0 - 100.0] or [0.0 - 1.0]
    reason: str = ""
    created_at: float = Field(default_factory=time.time)
    expires_at: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
