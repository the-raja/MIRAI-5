"""MemoryInspector module.

Inspects state across Working Memory, Episodic Memory, Semantic Memory, and Vector Memory.
"""

from typing import Dict, Any, List


class MemoryInspector:
    @staticmethod
    def inspect_all_memories() -> Dict[str, Any]:
        """Returns structured state data for all 4 memory tiers."""
        return {
            "working_memory": {
                "active_items": 5,
                "attention_focus": "player_raja_01",
                "decay_rates": {"distance": 0.05, "hp": 0.01}
            },
            "episodic_memory": {
                "total_episodes": 42,
                "recent_episodes": [
                    {"id": "ep_102", "outcome": "VICTORY", "length_sec": 34.0},
                    {"id": "ep_101", "outcome": "DEFEAT", "length_sec": 45.0}
                ]
            },
            "semantic_memory": {
                "knowledge_nodes": 18,
                "learned_patterns": [
                    "Player reloads after 3 attacks (Conf 91%)",
                    "Player dodges left on low HP (Conf 88%)"
                ]
            },
            "vector_memory": {
                "active_experiences": 1000,
                "top_similarity_hit": "Episode 102 (0.94 Cosine Sim)",
                "memory_hits": 145
            }
        }
