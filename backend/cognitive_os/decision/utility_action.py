"""UtilityAction data structure. Only data models, no logic."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class UtilityAction(BaseModel):
    id: str
    name: str  # e.g. "HeavyAttack", "Dash", "Heal", "Retreat", "Observe", "Block", "MoveToCover"
    base_score: float = 0.5  # Base utility score [0.0 - 1.0]
    risk: float = 0.2        # Risk deduction [0.0 - 1.0]
    cost: float = 10.0       # Stamina / mana cost
    cooldown: float = 0.0    # Cooldown duration in seconds
    last_used_timestamp: float = 0.0
    requirements: Dict[str, Any] = Field(default_factory=dict)
    target_entity_id: Optional[str] = None

    def is_on_cooldown(self, current_time: float) -> bool:
        """Returns True if the action is currently on cooldown."""
        if self.cooldown <= 0.0:
            return False
        return (current_time - self.last_used_timestamp) < self.cooldown


def create_standard_action_set() -> List[UtilityAction]:
    """Returns standard action candidates available to MIRAI."""
    return [
        UtilityAction(id="act_heavy", name="HeavyAttack", base_score=0.85, risk=0.4, cost=30.0, cooldown=3.0),
        UtilityAction(id="act_light", name="LightAttack", base_score=0.70, risk=0.15, cost=10.0, cooldown=0.5),
        UtilityAction(id="act_dash", name="Dash", base_score=0.60, risk=0.1, cost=15.0, cooldown=1.5),
        UtilityAction(id="act_heal", name="Heal", base_score=0.75, risk=0.5, cost=0.0, cooldown=10.0),
        UtilityAction(id="act_retreat", name="Retreat", base_score=0.65, risk=0.1, cost=5.0, cooldown=2.0),
        UtilityAction(id="act_observe", name="Observe", base_score=0.30, risk=0.0, cost=0.0, cooldown=0.0),
        UtilityAction(id="act_block", name="Block", base_score=0.65, risk=0.1, cost=20.0, cooldown=1.0),
        UtilityAction(id="act_cover", name="MoveToCover", base_score=0.80, risk=0.05, cost=10.0, cooldown=2.0)
    ]
