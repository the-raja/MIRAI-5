"""More unit tests for Phase 12 Vector Memory & Retrieval."""

import pytest
from backend.cognitive_os.vector_memory.embedding_engine import ExperienceEmbeddingEngine
from backend.cognitive_os.vector_memory.experience import Experience
from backend.cognitive_os.vector_memory.vector_store import VectorStore


def test_embedding_engine_zero_vector_norm():
    engine = ExperienceEmbeddingEngine()
    normed = engine._normalize([0.0] * 16)
    assert len(normed) == 16


def test_vector_store_load_nonexistent(tmp_path):
    store = VectorStore()
    assert store.load_index(str(tmp_path / "nonexistent.json")) is False


def test_vector_store_empty_search():
    store = VectorStore()
    results = store.search_nearest_neighbors([0.1] * 16)
    assert results == []


def test_experience_to_dict():
    exp = Experience(experience_id="e_dict", episode_id="ep_dict")
    d = exp.to_dict()
    assert d["experience_id"] == "e_dict"
    assert d["episode_id"] == "ep_dict"
