"""ActionNode module for Action Graph representation."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ActionNode(BaseModel):
    name: str
    energy_cost: float = 10.0
    cooldown_sec: float = 1.0
    risk: float = 0.1
    expected_damage: float = 25.0
    success_probability: float = 0.90
    prerequisites: List[str] = Field(default_factory=list)
    valid_transitions: List[str] = Field(default_factory=list)
