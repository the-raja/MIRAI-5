"""Experience schema model for Vector Memory & Experience Retrieval.

Unlike a raw episode, an Experience object is optimized for vector embedding, fast spatial indexing (HNSW/FAISS), and semantic similarity retrieval.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class Experience(BaseModel):
    experience_id: str
    episode_id: str
    player_profile: Dict[str, Any] = Field(default_factory=dict)
    boss_profile: Dict[str, Any] = Field(default_factory=dict)
    feature_vector: List[float] = Field(default_factory=list)
    outcome: str = "VICTORY"
    duration: float = 60.0
    tags: List[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
