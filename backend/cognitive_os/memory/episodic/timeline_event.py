"""TimelineEvent data structure.

Stores meaningful tactical events occurring during a battle episode (Never saves raw 60 Hz frames—only key events).
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.cognitive_os.telemetry.telemetry_frame import Vector3Data


class TimelineEvent(BaseModel):
    event_id: str
    timestamp: float
    event_type: str  # e.g. "Player Reloaded", "Boss Heavy Attack", "Player Dodged Left", "Boss Healed", "Player Used Medkit", "Boss Defeated", "Player Defeated"
    importance: float = 50.0
    position: Optional[Vector3Data] = None
    related_entity: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
