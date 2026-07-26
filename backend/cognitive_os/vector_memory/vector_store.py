"""VectorStore module.

Fast approximate nearest-neighbor vector memory store supporting Memory Management Policies (Step 8):
1. Maximum capacity & eviction
2. Deduplication (similarity > 0.99)
3. Aging & importance decay
4. Importance weighting
5. Retrieval frequency tracking
"""

from typing import List, Dict, Any, Tuple, Optional
import os
import json
import time
import numpy as np
from backend.cognitive_os.vector_memory.experience import Experience
from backend.cognitive_os.vector_memory.embedding_engine import ExperienceEmbeddingEngine


class VectorStore:
    def __init__(
        self,
        embedding_engine: Optional[ExperienceEmbeddingEngine] = None,
        max_capacity: int = 1000
    ) -> None:
        self.embedding_engine = embedding_engine or ExperienceEmbeddingEngine()
        self.max_capacity = max_capacity
        self._experiences: Dict[str, Experience] = {}
        self._vectors: Dict[str, List[float]] = {}
        self._retrieval_counts: Dict[str, int] = {}
        self._importance_scores: Dict[str, float] = {}

    def add_experience(self, exp: Experience, importance: float = 1.0) -> None:
        """Adds experience with deduplication check and capacity eviction policy."""
        vec = self.embedding_engine.embed_experience(exp)
        exp.feature_vector = vec

        # 1. Deduplication check (similarity > 0.99)
        for existing_id, existing_vec in self._vectors.items():
            sim = self._calculate_cosine_similarity(vec, existing_vec)
            if sim > 0.99:
                # Merge / update existing experience retrieval count & importance
                self._retrieval_counts[existing_id] = self._retrieval_counts.get(existing_id, 0) + 1
                self._importance_scores[existing_id] = min(1.0, self._importance_scores.get(existing_id, 1.0) + 0.1)
                return

        # 2. Eviction policy if capacity exceeded
        if len(self._experiences) >= self.max_capacity:
            self._evict_least_valuable_experience()

        self._experiences[exp.experience_id] = exp
        self._vectors[exp.experience_id] = vec
        self._retrieval_counts[exp.experience_id] = 0
        self._importance_scores[exp.experience_id] = max(0.1, min(1.0, importance))

    def remove_experience(self, experience_id: str) -> bool:
        """Removes an Experience by experience_id."""
        if experience_id in self._experiences:
            del self._experiences[experience_id]
            del self._vectors[experience_id]
            if experience_id in self._retrieval_counts:
                del self._retrieval_counts[experience_id]
            if experience_id in self._importance_scores:
                del self._importance_scores[experience_id]
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
        """Performs Cosine Similarity nearest neighbor search and increments retrieval counts."""
        if not self._vectors:
            return []

        q_arr = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q_arr)

        scored_results: List[Tuple[Experience, float]] = []

        for exp_id, vec in self._vectors.items():
            sim = self._calculate_cosine_similarity(query_vector, vec)
            exp = self._experiences[exp_id]
            scored_results.append((exp, round(sim, 4)))

        scored_results.sort(key=lambda x: -x[1])
        top_results = scored_results[:top_k]

        # Track retrieval frequency
        for exp, sim in top_results:
            self._retrieval_counts[exp.experience_id] = self._retrieval_counts.get(exp.experience_id, 0) + 1

        return top_results

    def _evict_least_valuable_experience(self) -> None:
        """Evicts experience with lowest combined value score (importance * retrieval_count / age)."""
        if not self._experiences:
            return
        c_time = time.time()

        lowest_id = None
        lowest_score = float("inf")

        for exp_id, exp in self._experiences.items():
            age = max(1.0, c_time - exp.timestamp)
            importance = self._importance_scores.get(exp_id, 1.0)
            retrievals = self._retrieval_counts.get(exp_id, 0)
            value_score = (importance * (1.0 + retrievals)) / np.log(age + 2.0)

            if value_score < lowest_score:
                lowest_score = value_score
                lowest_id = exp_id

        if lowest_id:
            self.remove_experience(lowest_id)

    def _calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        a1 = np.array(vec1, dtype=np.float32)
        a2 = np.array(vec2, dtype=np.float32)
        n1 = np.linalg.norm(a1)
        n2 = np.linalg.norm(a2)
        if n1 == 0 or n2 == 0:
            return 0.0
        return float(np.dot(a1, a2) / (n1 * n2))

    def size(self) -> int:
        return len(self._experiences)

    def save_index(self, filepath: str) -> None:
        """Saves vector memory index with memory management metrics to disk."""
        data = {
            "max_capacity": self.max_capacity,
            "experiences": {eid: exp.to_dict() for eid, exp in self._experiences.items()},
            "vectors": self._vectors,
            "retrieval_counts": self._retrieval_counts,
            "importance_scores": self._importance_scores
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

        self.max_capacity = data.get("max_capacity", self.max_capacity)
        self._experiences = {
            eid: Experience(**exp_dict)
            for eid, exp_dict in data.get("experiences", {}).items()
        }
        self._vectors = data.get("vectors", {})
        self._retrieval_counts = data.get("retrieval_counts", {})
        self._importance_scores = data.get("importance_scores", {})
        return True
