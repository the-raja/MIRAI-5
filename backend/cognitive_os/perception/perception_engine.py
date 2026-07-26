"""Perception Engine module.

Intakes TelemetryFrame data and extracts normalized spatial/combat observations and flags.
Contains ZERO ML and ZERO decision logic — it only observes state changes.
"""

from typing import Optional, Dict, List, Any
import math
from backend.cognitive_os.telemetry.telemetry_frame import TelemetryFrame, Vector3Data
from backend.cognitive_os.perception.observation import Observation, ObservationSet
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class PerceptionEngine:
    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.event_bus = event_bus
        if self.event_bus:
            self.event_bus.subscribe("TELEMETRY_FRAME", self._on_telemetry_frame)

    def _on_telemetry_frame(self, event: Event) -> None:
        if isinstance(event.payload, TelemetryFrame):
            self.process_frame(event.payload)

    def process_frame(self, frame: TelemetryFrame) -> ObservationSet:
        """Processes a TelemetryFrame and returns a normalized ObservationSet."""
        observations: List[Observation] = []
        flags: Dict[str, bool] = {}
        distances: Dict[str, float] = {}
        feature_vector: List[float] = []

        boss_pos = frame.boss.position if frame.boss else Vector3Data(x=0, y=0, z=0)

        # 1. Observe Players
        for player_id, player in frame.players.items():
            # Calculate Euclidian distance to boss
            dx = player.position.x - boss_pos.x
            dy = player.position.y - boss_pos.y
            dz = player.position.z - boss_pos.z
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            distances[player_id] = round(dist, 3)

            # Observe speed / running
            vx = player.velocity.x
            vy = player.velocity.y
            vz = player.velocity.z
            speed = math.sqrt(vx * vx + vy * vy + vz * vz)
            is_running = speed > 2.0 or "Shift" in frame.keyboard or "Sprint" in player.animation

            # Observe reload & cover
            is_reloading = "Reload" in player.animation or player.current_action == "RELOAD"
            is_in_cover = "Cover" in player.animation or player.current_action == "COVER"
            is_visible = dist < 50.0  # Simple visibility range observation

            flags["PlayerVisible"] = is_visible
            flags["PlayerRunning"] = is_running
            flags["PlayerReloading"] = is_reloading
            flags["PlayerEnteredCover"] = is_in_cover

            observations.append(
                Observation(
                    type="PLAYER_OBSERVATION",
                    source=player_id,
                    confidence=1.0,
                    timestamp=frame.timestamp,
                    metadata={
                        "distance": dist,
                        "health_pct": player.health / 100.0,
                        "is_running": is_running,
                        "is_reloading": is_reloading,
                        "is_in_cover": is_in_cover
                    }
                )
            )

            # Feature vector representation for perception pipeline
            feature_vector.extend([player.position.x, player.position.y, player.position.z, dist, player.health / 100.0])

        # 2. Observe Projectiles
        has_incoming_projectile = False
        for proj in frame.projectiles:
            p_dx = proj.position.x - boss_pos.x
            p_dz = proj.position.z - boss_pos.z
            p_dist = math.sqrt(p_dx * p_dx + p_dz * p_dz)
            if p_dist < 15.0:
                has_incoming_projectile = True
                observations.append(
                    Observation(
                        type="PROJECTILE_OBSERVATION",
                        source=proj.id,
                        confidence=1.0,
                        timestamp=frame.timestamp,
                        metadata={"distance": p_dist, "damage": proj.damage}
                    )
                )

        flags["ProjectileIncoming"] = has_incoming_projectile

        # 3. Observe Boss State
        boss_hit = False
        if frame.boss:
            boss_hit = frame.boss.health < 100.0 or "Hit" in frame.boss.animation
        flags["BossHit"] = boss_hit

        obs_set = ObservationSet(
            timestamp=frame.timestamp,
            frame_id=frame.frame_id,
            observations=observations,
            feature_vector=feature_vector,
            flags=flags
        )

        if self.event_bus:
            event = Event(
                event_type="OBSERVATION_SET",
                timestamp=frame.timestamp,
                source="PerceptionEngine",
                payload=obs_set
            )
            self.event_bus.publish(event)

        return obs_set
