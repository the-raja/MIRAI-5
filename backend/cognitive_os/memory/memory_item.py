"""MemoryItem data structure with cognitive time-decay scoring."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from backend.cognitive_os.telemetry.telemetry_frame import Vector3Data


class MemoryItem(BaseModel):
    id: str
    timestamp: float
    event_type: str
    confidence: float = 1.0
    importance: float = 50.0  # Initial importance score [0.0 - 100.0]
    position: Optional[Vector3Data] = None
    related_entity: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def get_decayed_score(self, current_time: float) -> float:
        """Calculates current decayed importance score based on elapsed time.
        
        High importance memories (e.g. 100) decay very slowly.
        Lower importance memories decay rapidly.
        """
        elapsed = max(0.0, current_time - self.timestamp)
        decay_rate = 0.02 + 0.5 * ((100.0 - self.importance) / 100.0) ** 1.2
        score = self.importance - (decay_rate * 10.0 * elapsed)
        return max(0.0, round(score, 2))
