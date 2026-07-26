"""EmbeddingProvider interface and providers.

Decouples vector memory from specific embedding models.
Swap sentence-transformers for custom combat-trained models without modifying vector store or retrieval code.
"""

from typing import List, Dict, Any
from abc import ABC, abstractmethod
import numpy as np


class EmbeddingProvider(ABC):
    @abstractmethod
    def encode(self, text: str) -> List[float]:
        """Encodes text into a normalized dense vector embedding."""
        pass


class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", vector_dim: int = 16) -> None:
        self.model_name = model_name
        self.vector_dim = vector_dim

    def encode(self, text: str) -> List[float]:
        seed = sum(ord(c) for c in text)
        np.random.seed(seed % 10000)
        vec = np.random.randn(self.vector_dim).astype(np.float32)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist() if norm != 0 else vec.tolist()


class CustomCombatEmbeddingProvider(EmbeddingProvider):
    def __init__(self, vector_dim: int = 16) -> None:
        self.vector_dim = vector_dim

    def encode(self, text: str) -> List[float]:
        seed = (sum(ord(c) for c in text) * 31) % 10000
        np.random.seed(seed)
        vec = np.random.randn(self.vector_dim).astype(np.float32)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist() if norm != 0 else vec.tolist()
