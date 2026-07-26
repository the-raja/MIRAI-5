"""World state data structures. Only data models, no logic."""

from typing import Dict, List, Any
from pydantic import BaseModel, Field
from backend.cognitive_os.telemetry.telemetry_frame import EntityStateData, ProjectileData, Vector3Data


class ObstacleData(BaseModel):
    id: str
    position: Vector3Data = Field(default_factory=Vector3Data)
    size: Vector3Data = Field(default_factory=Vector3Data)
    is_cover: bool = True


class MapObjectData(BaseModel):
    id: str
    object_type: str
    position: Vector3Data = Field(default_factory=Vector3Data)
    properties: Dict[str, Any] = Field(default_factory=dict)


class WorldState(BaseModel):
    timestamp: float = 0.0
    frame_id: int = 0
    entities: Dict[str, EntityStateData] = Field(default_factory=dict)
    obstacles: List[ObstacleData] = Field(default_factory=list)
    projectiles: List[ProjectileData] = Field(default_factory=list)
    map_objects: List[MapObjectData] = Field(default_factory=list)
