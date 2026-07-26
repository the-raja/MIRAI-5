"""SimilaritySearchEngine module.

Step 5: Executes nearest neighbor similarity search over Vector Store given real-time battle situation.

Returns Top 10 Similar Experiences:
- similarity score
- episode reference
- outcome
- why it was retrieved
"""

from typing import List, Dict, Any, Optional
from backend.cognitive_os.vector_memory.vector_store import VectorStore
from backend.cognitive_os.vector_memory.embedding_engine import ExperienceEmbeddingEngine


class SimilaritySearchEngine:
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        embedding_engine: Optional[ExperienceEmbeddingEngine] = None
    ) -> None:
        self.embedding_engine = embedding_engine or ExperienceEmbeddingEngine()
        self.vector_store = vector_store or VectorStore(embedding_engine=self.embedding_engine)

    def search_similar_experiences(
        self,
        current_situation: Dict[str, Any],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """Queries vector memory store and formats Top K experience retrieval results."""
        query_vec = self.embedding_engine.embed_current_situation(current_situation)
        neighbors = self.vector_store.search_nearest_neighbors(query_vec, top_k=top_k)

        results: List[Dict[str, Any]] = []

        for exp, sim_score in neighbors:
            # Build human-explainable reason why retrieved
            p_wep = exp.player_profile.get("preferred_weapon", "Shotgun")
            aggr = exp.player_profile.get("aggression_score", 0.7)
            why = f"Matches player profile: {p_wep} weapon, high aggression ({aggr:.2f}), and HP state below 30%."

            res = {
                "similarity_score": sim_score,
                "episode_reference": exp.episode_id,
                "experience_id": exp.experience_id,
                "outcome": exp.outcome,
                "duration": exp.duration,
                "why_retrieved": why,
                "experience": exp
            }
            results.append(res)

        return results
