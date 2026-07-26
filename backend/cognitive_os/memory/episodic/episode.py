"""Episode data structure. Only data models, no logic."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.cognitive_os.memory.episodic.timeline_event import TimelineEvent
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary, PlayerProfile, BossProfile


class Episode(BaseModel):
    episode_id: str
    timestamp: float
    duration: float = 0.0
    winner: str = "UNKNOWN"
    player_profile: PlayerProfile = Field(default_factory=lambda: PlayerProfile(player_id="unknown"))
    boss_profile: BossProfile = Field(default_factory=BossProfile)
    timeline: List[TimelineEvent] = Field(default_factory=list)
    battle_summary: BattleSummary = Field(default_factory=lambda: BattleSummary(match_id="unknown"))
    metadata: Dict[str, Any] = Field(default_factory=dict)
