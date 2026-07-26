"""Plan schema model for Strategic Planning System.

Plans are first-class objects representing multi-step strategic action sequences rather than single reactive moves:
Situation -> Goal -> Plan -> Execute -> Monitor -> Re-plan
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class Plan(BaseModel):
    plan_id: str
    goal: str = "Pressure Player"
    actions: List[str] = Field(default_factory=list)
    expected_reward: float = 85.0
    risk: float = 0.15
    estimated_duration: float = 4.5
    success_probability: float = 0.88
    current_step_index: int = 0
    status: str = "PLANNED"
    timestamp: float = Field(default_factory=time.time)

    def get_current_action(self) -> Optional[str]:
        if 0 <= self.current_step_index < len(self.actions):
            return self.actions[self.current_step_index]
        return None

    def advance(self) -> bool:
        if self.current_step_index < len(self.actions) - 1:
            self.current_step_index += 1
            return True
        self.current_step_index = len(self.actions)
        self.status = "COMPLETED"
        return False

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
