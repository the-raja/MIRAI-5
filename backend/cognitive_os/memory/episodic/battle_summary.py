"""BattleSummary data structure.

Summarizes thousands of combat frames into compact, ML-ready feature matrices.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class PlayerProfile(BaseModel):
    player_id: str
    combat_style: str = "Balanced"  # e.g. "Aggressive", "Defensive", "Counter_Fighter"
    reload_count: int = 0
    preferred_dodge: str = "Unknown"  # e.g. "Left", "Right", "Back"
    most_used_weapon: str = "Unknown"
    hit_accuracy: float = 0.0
    panic_threshold_hp: float = 30.0


class BossProfile(BaseModel):
    boss_id: str = "boss_mirai"
    damage_dealt: float = 0.0
    damage_taken: float = 0.0
    counter_success_rate: float = 0.0
    primary_strategy_used: str = "Standard_Engage"


class BattleSummary(BaseModel):
    match_id: str
    duration_seconds: float = 0.0
    winner: str = "UNKNOWN"  # "Player" or "Boss"
    damage_dealt: float = 0.0
    damage_taken: float = 0.0
    reload_count: int = 0
    most_used_weapon: str = "Katana"
    average_distance: float = 0.0
    preferred_dodge: str = "Left"  # "Left", "Right", "Back"
    aggression_score: float = 0.5  # [0.0 - 1.0]
    defense_score: float = 0.5     # [0.0 - 1.0]
    accuracy: float = 0.0          # [0.0 - 1.0]
    critical_moments: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
