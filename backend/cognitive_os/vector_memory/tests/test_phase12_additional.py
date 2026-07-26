"""Additional unit tests for Phase 12 Vector Memory & Retrieval."""

import pytest
from backend.cognitive_os.vector_memory.experience import Experience
from backend.cognitive_os.vector_memory.vector_store import VectorStore
from backend.cognitive_os.vector_memory.retrieval_engine import ExperienceRetrievalEngine


def test_vector_store_remove_nonexistent():
    store = VectorStore()
    assert store.remove_experience("nonexistent") is False


def test_vector_store_update_existing():
    store = VectorStore()
    exp = Experience(experience_id="exp_x", episode_id="ep_x", outcome="DEFEAT")
    store.add_experience(exp)

    exp.outcome = "VICTORY"
    store.update_experience(exp)
    assert store._experiences["exp_x"].outcome == "VICTORY"


def test_experience_retrieval_engine_strategy_defend():
    store = VectorStore()
    # Add player win experiences to trigger Defend & Counter strategy
    e1 = Experience(experience_id="e1", episode_id="ep1", outcome="Player")
    e2 = Experience(experience_id="e2", episode_id="ep2", outcome="Player")
    store.add_experience(e1)
    store.add_experience(e2)

    engine = ExperienceRetrievalEngine(vector_store=store)
    data = engine.query_experiences({"player_hp": 90.0}, top_k=2)

    assert data["recommended_strategy"] in ["Defend & Counter", "Pressure Player"]
    assert data["confidence"] >= 0.80
