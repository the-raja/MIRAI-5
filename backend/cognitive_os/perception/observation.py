"""Perception observation data structures. Only data models, no logic."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class Observation(BaseModel):
    type: str
    source: str
    confidence: float = 1.0
    timestamp: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ObservationSet(BaseModel):
    timestamp: float
    frame_id: int
    observations: List[Observation] = Field(default_factory=list)
    feature_vector: List[float] = Field(default_factory=list)
    flags: Dict[str, bool] = Field(default_factory=dict)
