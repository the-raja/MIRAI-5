"""ExperienceEmbeddingEngine module.

Transforms an Experience or Battle Summary into a normalized fixed-length (16-D) vector embedding.
Decoupled: handcrafted features can be hot-swapped for learned neural/LLM embeddings with zero Cognitive OS changes.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from backend.cognitive_os.vector_memory.experience import Experience


class ExperienceEmbeddingEngine:
    def __init__(self, vector_dim: int = 16) -> None:
        self.vector_dim = vector_dim

    def embed_experience(self, exp: Experience) -> List[float]:
        """Maps an Experience instance into a normalized 16-dimensional embedding vector."""
        if exp.feature_vector and len(exp.feature_vector) == self.vector_dim:
            return self._normalize(exp.feature_vector)

        # Handcrafted feature extraction from Experience metadata
        profile = exp.player_profile
        boss_prof = exp.boss_profile

        vec = [
            float(profile.get("player_hp", 80.0)) / 100.0,
            float(profile.get("boss_hp", 70.0)) / 100.0,
            float(profile.get("distance", 5.0)) / 30.0,
            float(profile.get("stamina", 80.0)) / 100.0,
            float(profile.get("aggression_score", 0.7)),
            float(profile.get("reload_frequency", 5)) / 20.0,
            float(boss_prof.get("phase", 1)) / 3.0,
            1.0 if exp.outcome == "VICTORY" else 0.0,
            float(exp.duration) / 300.0,
            1.0 if "high_aggression" in exp.tags else 0.0,
            1.0 if "low_hp_clutch" in exp.tags else 0.0,
            0.5, 0.5, 0.5, 0.5, 0.5
        ]
        return self._normalize(vec[:self.vector_dim])

    def embed_current_situation(self, situation: Dict[str, Any]) -> List[float]:
        """Embeds real-time battle situation into a query vector."""
        vec = [
            float(situation.get("player_hp", 80.0)) / 100.0,
            float(situation.get("boss_hp", 70.0)) / 100.0,
            float(situation.get("distance", 5.0)) / 30.0,
            float(situation.get("stamina", 80.0)) / 100.0,
            float(situation.get("aggression_score", 0.7)),
            float(situation.get("reload_frequency", 5)) / 20.0,
            float(situation.get("boss_phase", 1)) / 3.0,
            1.0,
            0.2,
            1.0 if float(situation.get("aggression_score", 0.7)) > 0.8 else 0.0,
            1.0 if float(situation.get("player_hp", 80.0)) < 30.0 else 0.0,
            0.5, 0.5, 0.5, 0.5, 0.5
        ]
        return self._normalize(vec[:self.vector_dim])

    def _normalize(self, vec: List[float]) -> List[float]:
        arr = np.array(vec, dtype=np.float32)
        norm = np.linalg.norm(arr)
        if norm == 0:
            return vec
        return (arr / norm).tolist()
