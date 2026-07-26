"""FeatureExtractor module.

Transforms real-time Game State (Telemetry, WorldModel, WorkingMemory, SemanticMemory) into structured ML feature vectors.
Establishes the tabular dataset format for future XGBoost, LightGBM, and PyTorch ML models.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import numpy as np
from backend.cognitive_os.telemetry.telemetry_frame import TelemetryFrame
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager


class FeatureVector(BaseModel):
    distance: float = 5.0
    player_hp: float = 100.0
    boss_hp: float = 100.0
    weapon: str = "Katana"
    stamina: float = 100.0
    cooldowns: Dict[str, float] = Field(default_factory=dict)
    current_action: str = "IDLE"
    last_5_actions: List[str] = Field(default_factory=list)
    aggression_score: float = 0.5
    reload_count: int = 0
    preferred_dodge: str = "Left"
    preferred_weapon: str = "Katana"
    time_since_last_heal: float = 999.0

    def to_dict(self) -> Dict[str, Any]:
        """Converts feature vector to dictionary format for tabular ML."""
        d = self.model_dump()
        d["last_5_actions_str"] = ",".join(self.last_5_actions)
        return d

    def to_numpy_array(self) -> np.ndarray:
        """Converts numerical features to a NumPy array for ML model inference."""
        return np.array([
            self.distance,
            self.player_hp,
            self.boss_hp,
            self.stamina,
            self.aggression_score,
            float(self.reload_count),
            self.time_since_last_heal
        ], dtype=np.float32)


class FeatureExtractor:
    def extract_features(
        self,
        telemetry_frame: Optional[TelemetryFrame] = None,
        world_model: Optional[WorldModel] = None,
        memory_manager: Optional[MemoryManager] = None,
        semantic_manager: Optional[SemanticManager] = None,
        recent_actions: Optional[List[str]] = None
    ) -> FeatureVector:
        """Extracts complete ML feature vector from active game state components."""
        vector = FeatureVector()

        # 1. Telemetry Features
        if telemetry_frame:
            player = telemetry_frame.players.get("player_raja_01")
            boss = telemetry_frame.boss
            if player:
                vector.player_hp = player.health
                vector.stamina = player.stamina
                vector.weapon = player.weapon
                vector.current_action = player.current_action
            if boss:
                vector.boss_hp = boss.health

        # 2. World Model Features
        if world_model:
            player_pos = world_model.estimated_player_positions.get("player_raja_01")
            if player_pos:
                vector.distance = round(float(np.sqrt(player_pos.x**2 + player_pos.z**2)), 2)

        # 3. Working Memory Features
        if memory_manager and world_model:
            current_time = world_model.timestamp
            time_heal = memory_manager.time_since_event("PlayerHeal", current_time=current_time)
            if time_heal is not None:
                vector.time_since_last_heal = round(time_heal, 1)

            recent_reloads = memory_manager.count_events_in_window("PlayerReloading", time_window_seconds=10.0, current_time=current_time)
            vector.reload_count = recent_reloads

        # 4. Semantic Memory Features
        if semantic_manager:
            k_dodge = semantic_manager.memory.get_knowledge_by_type("PreferredDodge")
            if k_dodge:
                vector.preferred_dodge = k_dodge.metadata.get("preferred_dodge", "Left")

            k_wep = semantic_manager.memory.get_knowledge_by_type("PreferredWeapon")
            if k_wep:
                vector.preferred_weapon = k_wep.metadata.get("preferred_weapon", "Katana")

            k_range = semantic_manager.memory.get_knowledge_by_type("EngagementRange")
            if k_range:
                vector.aggression_score = k_range.metadata.get("aggression_score", 0.5)

        # 5. Recent Actions History
        if recent_actions:
            vector.last_5_actions = recent_actions[-5:]

        return vector
