"""Telemetry Collector module.

Ingests or generates synthetic 60 Hz TelemetryFrames (Player, Boss, Projectiles, Inputs) and publishes them to the EventBus.
"""

from typing import Optional, Dict, Any, List
import time
import math
from backend.cognitive_os.telemetry.telemetry_frame import (
    TelemetryFrame,
    EntityStateData,
    Vector3Data,
    ProjectileData
)
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class TelemetryCollector:
    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.event_bus = event_bus
        self._frame_counter = 0

    def generate_fake_frame(self, current_time: Optional[float] = None) -> TelemetryFrame:
        """Generates a synthetic 60 Hz telemetry frame for testing/simulation."""
        if current_time is None:
            current_time = time.time()

        self._frame_counter += 1

        # Simulate synthetic player movement along a circle
        angle = self._frame_counter * 0.05
        player_x = round(10.0 * math.cos(angle), 3)
        player_z = round(10.0 * math.sin(angle), 3)

        player_data = EntityStateData(
            id="player_raja_01",
            position=Vector3Data(x=player_x, y=0.0, z=player_z),
            velocity=Vector3Data(x=-0.5 * math.sin(angle), y=0.0, z=0.5 * math.cos(angle)),
            health=85.0,
            stamina=60.0,
            posture=90.0,
            weapon="Katana",
            animation="Sprint_Forward",
            current_action="SPRINT",
            team="PLAYERS",
            alive=True
        )

        boss_data = EntityStateData(
            id="boss_mirai",
            position=Vector3Data(x=0.0, y=0.0, z=0.0),
            velocity=Vector3Data(x=0.0, y=0.0, z=0.0),
            health=100.0,
            stamina=100.0,
            posture=100.0,
            weapon="Greatsword",
            animation="Guard_Stance",
            current_action="GUARD",
            team="BOSS",
            alive=True
        )

        # Faked projectile
        projectiles: List[ProjectileData] = []
        if self._frame_counter % 30 == 0:
            projectiles.append(
                ProjectileData(
                    id=f"proj_{self._frame_counter}",
                    owner_id="player_raja_01",
                    position=Vector3Data(x=player_x, y=1.2, z=player_z),
                    velocity=Vector3Data(x=-player_x, y=0.0, z=-player_z),
                    damage=25.0
                )
            )

        frame = TelemetryFrame(
            timestamp=current_time,
            frame_id=self._frame_counter,
            players={"player_raja_01": player_data},
            boss=boss_data,
            projectiles=projectiles,
            keyboard=["W", "Shift"] if self._frame_counter % 2 == 0 else ["W"],
            mouse=Vector3Data(x=12.0, y=-4.0, z=0.0),
            world_time=current_time
        )

        if self.event_bus:
            event = Event(
                event_type="TELEMETRY_FRAME",
                timestamp=current_time,
                source="TelemetryCollector",
                payload=frame
            )
            self.event_bus.publish(event)

        return frame
