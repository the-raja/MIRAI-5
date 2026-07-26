"""WorldModel module.

Maintains spatial state and environmental belief model.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from backend.cognitive_os.telemetry.telemetry_frame import Vector3Data, TelemetryFrame
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class NodeData(BaseModel):
    id: str
    position: Vector3Data = Field(default_factory=Vector3Data)
    type: str = "Cover"


class ZoneData(BaseModel):
    id: str
    hazard_level: float = 0.0


class WorldModel(BaseModel):
    timestamp: float
    estimated_player_positions: Dict[str, Vector3Data] = Field(default_factory=dict)
    visible_entities: List[str] = Field(default_factory=list)
    cover_nodes: List[NodeData] = Field(default_factory=list)
    danger_zones: List[ZoneData] = Field(default_factory=list)
    safe_zones: List[ZoneData] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorldModelEngine:
    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.event_bus = event_bus
        self.current_world_model = WorldModel(timestamp=0.0)

        if self.event_bus:
            self.event_bus.subscribe("WORKING_MEMORY_UPDATED", self._on_working_memory_updated)
            self.event_bus.subscribe("ATTENTION_STATE", self._on_attention_state)
            self.event_bus.subscribe("TELEMETRY_FRAME", self._on_telemetry_frame)

    def _on_working_memory_updated(self, event: Event) -> None:
        self.update_world_model(event.timestamp)

    def _on_attention_state(self, event: Event) -> None:
        self.update_world_model(event.timestamp)

    def _on_telemetry_frame(self, event: Event) -> None:
        if isinstance(event.payload, TelemetryFrame):
            self.update_from_telemetry(event.payload)

    def update_from_telemetry(self, frame: TelemetryFrame) -> WorldModel:
        """Updates world model spatial state directly from a telemetry frame."""
        positions = {p_id: p.position for p_id, p in frame.players.items()}
        visible = list(frame.players.keys())

        self.current_world_model = WorldModel(
            timestamp=frame.timestamp,
            estimated_player_positions=positions,
            visible_entities=visible,
            cover_nodes=[
                NodeData(id="Cover_A", position=Vector3Data(x=5.0, y=0.0, z=5.0)),
                NodeData(id="Cover_B", position=Vector3Data(x=-5.0, y=0.0, z=5.0)),
                NodeData(id="Cover_C", position=Vector3Data(x=0.0, y=0.0, z=10.0))
            ]
        )

        if self.event_bus:
            evt = Event(
                event_type="WORLD_MODEL_UPDATED",
                timestamp=frame.timestamp,
                source="WorldModelEngine",
                payload=self.current_world_model
            )
            self.event_bus.publish(evt)

        return self.current_world_model

    def update_world_model(self, current_time: float) -> WorldModel:
        self.current_world_model = WorldModel(
            timestamp=current_time,
            estimated_player_positions={"player_raja_01": Vector3Data(x=10.0, y=0.0, z=0.5)},
            visible_entities=["player_raja_01"],
            cover_nodes=[
                NodeData(id="Cover_A", position=Vector3Data(x=5.0, y=0.0, z=5.0)),
                NodeData(id="Cover_B", position=Vector3Data(x=-5.0, y=0.0, z=5.0)),
                NodeData(id="Cover_C", position=Vector3Data(x=0.0, y=0.0, z=10.0))
            ]
        )

        if self.event_bus:
            evt = Event(
                event_type="WORLD_MODEL_UPDATED",
                timestamp=current_time,
                source="WorldModelEngine",
                payload=self.current_world_model
            )
            self.event_bus.publish(evt)

        return self.current_world_model
