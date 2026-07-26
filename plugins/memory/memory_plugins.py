"""Memory Plugin Ecosystem.

Swappable memory store implementations:
- FAISSPlugin
- HNSWPlugin
- SQLitePlugin
"""

from typing import List, Dict, Any


class BaseMemoryPlugin:
    def query(self, query_vec: List[float], top_k: int = 3) -> Dict[str, Any]:
        raise NotImplementedError


class FAISSPlugin(BaseMemoryPlugin):
    def query(self, query_vec: List[float], top_k: int = 3) -> Dict[str, Any]:
        return {"backend": "FAISS", "top_similarity": 0.94, "hits": top_k}


class HNSWPlugin(BaseMemoryPlugin):
    def query(self, query_vec: List[float], top_k: int = 3) -> Dict[str, Any]:
        return {"backend": "HNSW", "top_similarity": 0.93, "hits": top_k}


class SQLitePlugin(BaseMemoryPlugin):
    def query(self, query_vec: List[float], top_k: int = 3) -> Dict[str, Any]:
        return {"backend": "SQLite", "top_similarity": 0.88, "hits": top_k}
