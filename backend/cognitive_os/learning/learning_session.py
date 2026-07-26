"""LearningSession data structure. Only data models, no logic."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class LearningSession(BaseModel):
    session_id: str = Field(default_factory=lambda: f"ls_{int(time.time()*1000)}")
    episode_id: str
    timestamp: float = Field(default_factory=time.time)
    changes: List[str] = Field(default_factory=list)
    knowledge_updates: List[Dict[str, Any]] = Field(default_factory=list)
    prediction_accuracy: float = 0.0
    decision_accuracy: float = 0.0
    statistics: Dict[str, Any] = Field(default_factory=dict)
    model_versions: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
