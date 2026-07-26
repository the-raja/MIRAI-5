"""Base event model and standard event definitions for the Cognitive OS Event Bus."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import time


class Event(BaseModel):
    event_type: str
    timestamp: float = Field(default_factory=time.time)
    source: str = "UNKNOWN"
    payload: Any = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
