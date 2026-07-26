"""Telemetry frame data structures. Only data models, no logic."""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class Vector3Data(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class EntityStateData(BaseModel):
    id: str
    position: Vector3Data = Field(default_factory=Vector3Data)
    velocity: Vector3Data = Field(default_factory=Vector3Data)
    health: float = 100.0
    stamina: float = 100.0
    posture: float = 100.0
    weapon: str = "Unarmed"
    animation: str = "Idle"
    current_action: str = "IDLE"
    target_id: Optional[str] = None
    status_effects: List[str] = Field(default_factory=list)
    team: str = "UNKNOWN"
    alive: bool = True


class ProjectileData(BaseModel):
    id: str
    owner_id: str
    position: Vector3Data = Field(default_factory=Vector3Data)
    velocity: Vector3Data = Field(default_factory=Vector3Data)
    damage: float = 10.0


class InputData(BaseModel):
    keyboard: List[str] = Field(default_factory=list)
    mouse_delta: Vector3Data = Field(default_factory=Vector3Data)
    buttons: List[str] = Field(default_factory=list)


class TelemetryFrame(BaseModel):
    timestamp: float
    frame_id: int
    players: Dict[str, EntityStateData] = Field(default_factory=dict)
    boss: Optional[EntityStateData] = None
    projectiles: List[ProjectileData] = Field(default_factory=list)
    keyboard: List[str] = Field(default_factory=list)
    mouse: Vector3Data = Field(default_factory=Vector3Data)
    world_time: float = 0.0
