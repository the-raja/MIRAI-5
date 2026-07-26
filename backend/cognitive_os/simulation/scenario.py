"""BattleScenario module for Simulation Engine.

Defines repeatable battle scenarios for scientific benchmark evaluation:
- Scenario A: Aggressive Player, Sword, High HP
- Scenario B: Defensive Archer, Low HP
- Scenario C: Random Player
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class BattleScenario(BaseModel):
    scenario_id: str
    name: str
    player_style: str = "Aggressive"
    weapon: str = "Sword"
    player_hp: float = 100.0
    boss_hp: float = 100.0
    initial_distance: float = 5.0
    tags: List[str] = Field(default_factory=list)

    @classmethod
    def get_standard_scenarios(cls) -> List["BattleScenario"]:
        """Returns standard repeatable benchmark scenario suite."""
        return [
            cls(
                scenario_id="scenario_a",
                name="Scenario A — Aggressive Sword Player",
                player_style="Aggressive",
                weapon="Sword",
                player_hp=100.0,
                boss_hp=100.0,
                initial_distance=4.0,
                tags=["aggressive", "sword", "high_hp"]
            ),
            cls(
                scenario_id="scenario_b",
                name="Scenario B — Defensive Archer Player",
                player_style="Defensive",
                weapon="Bow",
                player_hp=30.0,
                boss_hp=100.0,
                initial_distance=15.0,
                tags=["defensive", "archer", "low_hp"]
            ),
            cls(
                scenario_id="scenario_c",
                name="Scenario C — Random Unpredictable Player",
                player_style="Random",
                weapon="Mixed",
                player_hp=80.0,
                boss_hp=100.0,
                initial_distance=8.0,
                tags=["random", "mixed"]
            )
        ]
