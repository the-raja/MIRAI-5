"""Memory API module for Runtime."""

from typing import Dict, Any, List
from backend.cognitive_os.vector_memory.retrieval_engine import ExperienceRetrievalEngine


class MemoryAPI:
    def __init__(self, retrieval_engine: ExperienceRetrievalEngine) -> None:
        self.retrieval_engine = retrieval_engine

    def query_experiences(self, situation: Dict[str, Any], top_k: int = 3) -> Dict[str, Any]:
        return self.retrieval_engine.query_experiences(situation, top_k=top_k)
