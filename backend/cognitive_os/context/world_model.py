"""World Model data structures and belief maintenance engine.

Maintains current spatial beliefs, line-of-sight visibility, estimated player positions, and cover node states.
Updated via Working Memory and Telemetry streams.
Contains NO ML predictions — purely maintains current spatial world understanding.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from backend.cognitive_os.telemetry.telemetry_frame import Vector3Data, TelemetryFrame
from backend.cognitive_os.attention.salience import AttentionState
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class CoverNodeData(BaseModel):
    id: str
    position: Vector3Data = Field(default_factory=Vector3Data)
    height: float = 1.5
    is_occupied: bool = False
    occupied_by_id: Optional[str] = None


class ZoneData(BaseModel):
    id: str
    center: Vector3Data = Field(default_factory=Vector3Data)
    radius: float = 5.0
    hazard_level: float = 0.0


class WorldModel(BaseModel):
    timestamp: float = 0.0
    estimated_player_positions: Dict[str, Vector3Data] = Field(default_factory=dict)
    visible_entities: List[str] = Field(default_factory=list)
    cover_nodes: List[CoverNodeData] = Field(default_factory=list)
    danger_zones: List[ZoneData] = Field(default_factory=list)
    safe_zones: List[ZoneData] = Field(default_factory=list)


class WorldModelEngine:
    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.event_bus = event_bus
        self.world_model = WorldModel(
            cover_nodes=[
                CoverNodeData(id="Cover_A", position=Vector3Data(x=10.0, y=0.0, z=5.0)),
                CoverNodeData(id="Cover_B", position=Vector3Data(x=-8.0, y=0.0, z=-3.0)),
                CoverNodeData(id="Cover_C", position=Vector3Data(x=0.0, y=0.0, z=15.0)),
            ]
        )

        if self.event_bus:
            self.event_bus.subscribe("TELEMETRY_FRAME", self._on_telemetry_frame)
            self.event_bus.subscribe("ATTENTION_STATE", self._on_attention_state)
            self.event_bus.subscribe("WORKING_MEMORY_UPDATED", self._on_working_memory_updated)

    def _on_telemetry_frame(self, event: Event) -> None:
        if isinstance(event.payload, TelemetryFrame):
            self.update_from_telemetry(event.payload)

    def _on_attention_state(self, event: Event) -> None:
        if isinstance(event.payload, AttentionState):
            self.update_from_attention(event.payload)

    def _on_working_memory_updated(self, event: Event) -> None:
        if isinstance(event.payload, list):
            self.update_from_working_memory(event.payload)

    def update_from_telemetry(self, frame: TelemetryFrame) -> WorldModel:
        """Update spatial beliefs based on latest physical frame telemetry."""
        self.world_model.timestamp = frame.timestamp
        self.world_model.visible_entities = list(frame.players.keys())

        # Update estimated positions for visible players
        for pid, player in frame.players.items():
            self.world_model.estimated_player_positions[pid] = player.position

            # Check cover node occupancy
            for node in self.world_model.cover_nodes:
                dx = player.position.x - node.position.x
                dz = player.position.z - node.position.z
                dist = (dx * dx + dz * dz) ** 0.5
                if dist < 2.0:
                    node.is_occupied = True
                    node.occupied_by_id = pid
                elif node.occupied_by_id == pid:
                    node.is_occupied = False
                    node.occupied_by_id = None

        # Update danger zones from projectiles
        danger_zones: List[ZoneData] = []
        for proj in frame.projectiles:
            danger_zones.append(
                ZoneData(
                    id=f"danger_{proj.id}",
                    center=proj.position,
                    radius=3.0,
                    hazard_level=proj.damage / 50.0
                )
            )
        self.world_model.danger_zones = danger_zones

        if self.event_bus:
            self._publish_update()

        return self.world_model

    def update_from_attention(self, att_state: AttentionState) -> WorldModel:
        """Update beliefs based on attention saliency events."""
        for event in att_state.salient_events:
            if event.event_id == "evt_PlayerEnteredCover" and att_state.primary_target_id:
                pid = att_state.primary_target_id
                if pid in self.world_model.estimated_player_positions:
                    self.world_model.estimated_player_positions[pid] = self.world_model.cover_nodes[0].position

        if self.event_bus:
            self._publish_update()

        return self.world_model

    def update_from_working_memory(self, memories: List[MemoryItem]) -> WorldModel:
        """Update spatial beliefs from Working Memory items."""
        for mem in memories:
            if mem.event_type == "PlayerEnteredCover" and mem.related_entity:
                self.world_model.estimated_player_positions[mem.related_entity] = self.world_model.cover_nodes[0].position

        if self.event_bus:
            self._publish_update()

        return self.world_model

    def _publish_update(self) -> None:
        if self.event_bus:
            event = Event(
                event_type="WORLD_MODEL_UPDATED",
                timestamp=self.world_model.timestamp,
                source="WorldModelEngine",
                payload=self.world_model
            )
            self.event_bus.publish(event)
