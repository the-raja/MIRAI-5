"""VectorStore module.

Fast approximate nearest-neighbor vector memory store supporting:
- add_experience
- remove_experience
- update_experience
- search_nearest_neighbors (Cosine Similarity)
- save_index / load_index
"""

from typing import List, Dict, Any, Tuple, Optional
import os
import json
import numpy as np
from backend.cognitive_os.vector_memory.experience import Experience
from backend.cognitive_os.vector_memory.embedding_engine import ExperienceEmbeddingEngine


class VectorStore:
    def __init__(self, embedding_engine: Optional[ExperienceEmbeddingEngine] = None) -> None:
        self.embedding_engine = embedding_engine or ExperienceEmbeddingEngine()
        self._experiences: Dict[str, Experience] = {}
        self._vectors: Dict[str, List[float]] = {}

    def add_experience(self, exp: Experience) -> None:
        """Adds or indexes an Experience into the VectorStore."""
        vec = self.embedding_engine.embed_experience(exp)
        exp.feature_vector = vec
        self._experiences[exp.experience_id] = exp
        self._vectors[exp.experience_id] = vec

    def remove_experience(self, experience_id: str) -> bool:
        """Removes an Experience by experience_id."""
        if experience_id in self._experiences:
            del self._experiences[experience_id]
            del self._vectors[experience_id]
            return True
        return False

    def update_experience(self, exp: Experience) -> None:
        """Updates an existing Experience."""
        self.add_experience(exp)

    def search_nearest_neighbors(
        self,
        query_vector: List[float],
        top_k: int = 10
    ) -> List[Tuple[Experience, float]]:
        """Performs Cosine Similarity nearest neighbor search across vector memory."""
        if not self._vectors:
            return []

        q_arr = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q_arr)

        scored_results: List[Tuple[Experience, float]] = []

        for exp_id, vec in self._vectors.items():
            v_arr = np.array(vec, dtype=np.float32)
            v_norm = np.linalg.norm(v_arr)

            if q_norm == 0 or v_norm == 0:
                sim = 0.0
            else:
                sim = float(np.dot(q_arr, v_arr) / (q_norm * v_norm))

            exp = self._experiences[exp_id]
            scored_results.append((exp, round(sim, 4)))

        scored_results.sort(key=lambda x: -x[1])
        return scored_results[:top_k]

    def size(self) -> int:
        return len(self._experiences)

    def save_index(self, filepath: str) -> None:
        """Saves vector memory index to disk."""
        data = {
            "experiences": {eid: exp.to_dict() for eid, exp in self._experiences.items()},
            "vectors": self._vectors
        }
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_index(self, filepath: str) -> bool:
        """Loads vector memory index from disk."""
        if not os.path.exists(filepath):
            return False
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._experiences = {
            eid: Experience(**exp_dict)
            for eid, exp_dict in data.get("experiences", {}).items()
        }
        self._vectors = data.get("vectors", {})
        return True
