"""EpisodeBuilder module (The Historian).

Listens to real-time events and Working Memory updates during a battle match, aggregates combat statistics, filters key timeline events, and constructs a complete, ML-ready Episode object when the match terminates.
"""

from typing import Optional, List, Dict, Any
import time
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.timeline_event import TimelineEvent
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary, PlayerProfile, BossProfile
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class EpisodeBuilder:
    def __init__(self, match_id: str, event_bus: Optional[EventBus] = None) -> None:
        self.match_id = match_id
        self.event_bus = event_bus

        self.start_time: float = time.time()
        self.end_time: Optional[float] = None
        self.is_active: bool = True

        self.timeline: List[TimelineEvent] = []
        self._recorded_event_ids: set = set()

        # Accumulated Statistics
        self.reload_count: int = 0
        self.dodge_counts: Dict[str, int] = {"Left": 0, "Right": 0, "Back": 0}
        self.weapon_usage: Dict[str, int] = {}
        self.distance_sum: float = 0.0
        self.distance_samples: int = 0
        self.damage_dealt_by_boss: float = 0.0
        self.damage_taken_by_boss: float = 0.0
        self.critical_moments: List[str] = []

        if self.event_bus:
            self.event_bus.subscribe("WORKING_MEMORY_UPDATED", self._on_working_memory_updated)

    def _on_working_memory_updated(self, event: Event) -> None:
        if not self.is_active:
            return
        if isinstance(event.payload, list):
            self.ingest_working_memories(event.payload, current_time=event.timestamp)

    def ingest_working_memories(self, memories: List[MemoryItem], current_time: float) -> None:
        """Ingest active working memories, filter key timeline events, and accumulate battle stats."""
        if not self.is_active:
            return

        for mem in memories:
            if mem.id in self._recorded_event_ids:
                continue

            # Only record high importance events into timeline (>60 importance)
            if mem.importance >= 60.0:
                self._recorded_event_ids.add(mem.id)
                tl_event = TimelineEvent(
                    event_id=mem.id,
                    timestamp=mem.timestamp,
                    event_type=mem.event_type,
                    importance=mem.importance,
                    position=mem.position,
                    related_entity=mem.related_entity,
                    metadata=mem.metadata
                )
                self.timeline.append(tl_event)

            # Accumulate statistics
            if mem.event_type in ("PlayerReloading", "Player Reloaded"):
                self.reload_count += 1

            if "Dodge" in mem.event_type:
                direction = mem.metadata.get("direction", "Left")
                self.dodge_counts[direction] = self.dodge_counts.get(direction, 0) + 1

            dist = mem.metadata.get("distance")
            if dist is not None:
                self.distance_sum += dist
                self.distance_samples += 1

            if mem.event_type == "BossHit":
                self.damage_taken_by_boss += mem.metadata.get("damage", 10.0)

            if mem.importance >= 85.0 and mem.event_type not in self.critical_moments:
                self.critical_moments.append(f"Key Event: {mem.event_type} at t={mem.timestamp:.1f}s")

    def finish_episode(self, winner: str = "Player", end_time: Optional[float] = None) -> Episode:
        """Finalizes the match building process and returns a completed Episode object."""
        self.is_active = False
        self.end_time = end_time if end_time is not None else time.time()
        duration = round(self.end_time - self.start_time, 2)

        preferred_dodge = max(self.dodge_counts, key=self.dodge_counts.get) if self.dodge_counts else "Left"
        avg_distance = round(self.distance_sum / self.distance_samples, 2) if self.distance_samples > 0 else 5.0
        most_used_weapon = max(self.weapon_usage, key=self.weapon_usage.get) if self.weapon_usage else "Katana"

        aggression = min(1.0, round(self.reload_count * 0.05 + (10.0 / max(1.0, avg_distance)) * 0.5, 2))
        defense = min(1.0, round(sum(self.dodge_counts.values()) * 0.1, 2))

        player_prof = PlayerProfile(
            player_id="player_raja_01",
            combat_style="Aggressive" if aggression > 0.6 else "Defensive",
            reload_count=self.reload_count,
            preferred_dodge=preferred_dodge,
            most_used_weapon=most_used_weapon,
            hit_accuracy=0.75
        )

        boss_prof = BossProfile(
            boss_id="boss_mirai",
            damage_dealt=self.damage_dealt_by_boss,
            damage_taken=self.damage_taken_by_boss,
            counter_success_rate=0.80
        )

        summary = BattleSummary(
            match_id=self.match_id,
            duration_seconds=duration,
            winner=winner,
            damage_dealt=self.damage_dealt_by_boss,
            damage_taken=self.damage_taken_by_boss,
            reload_count=self.reload_count,
            most_used_weapon=most_used_weapon,
            average_distance=avg_distance,
            preferred_dodge=preferred_dodge,
            aggression_score=aggression,
            defense_score=defense,
            accuracy=0.75,
            critical_moments=self.critical_moments
        )

        episode = Episode(
            episode_id=self.match_id,
            timestamp=self.start_time,
            duration=duration,
            winner=winner,
            player_profile=player_prof,
            boss_profile=boss_prof,
            timeline=self.timeline,
            battle_summary=summary
        )

        if self.event_bus:
            event = Event(
                event_type="EPISODE_COMPLETED",
                timestamp=self.end_time,
                source="EpisodeBuilder",
                payload=episode
            )
            self.event_bus.publish(event)

        return episode
