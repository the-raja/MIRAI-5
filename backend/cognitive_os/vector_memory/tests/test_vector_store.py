"""Unit tests for EmbeddingEngine, VectorStore, and SimilaritySearchEngine."""

import pytest
import os
import shutil
from backend.cognitive_os.vector_memory.experience import Experience
from backend.cognitive_os.vector_memory.embedding_engine import ExperienceEmbeddingEngine
from backend.cognitive_os.vector_memory.vector_store import VectorStore
from backend.cognitive_os.vector_memory.similarity import SimilaritySearchEngine


@pytest.fixture
def temp_vector_store_dir(tmp_path):
    root_dir = str(tmp_path / "vec_store")
    yield root_dir
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir, ignore_errors=True)


def test_embedding_engine_16d_vector():
    engine = ExperienceEmbeddingEngine()
    exp = Experience(
        experience_id="e1",
        episode_id="ep1",
        player_profile={"player_hp": 25.0, "aggression_score": 0.85}
    )
    vec = engine.embed_experience(exp)
    assert len(vec) == 16


def test_vector_store_add_remove_search(temp_vector_store_dir):
    store = VectorStore()
    exp1 = Experience(experience_id="exp_01", episode_id="ep_01", outcome="VICTORY")
    exp2 = Experience(experience_id="exp_02", episode_id="ep_02", outcome="DEFEAT")

    store.add_experience(exp1)
    store.add_experience(exp2)
    assert store.size() == 2

    # Save and load index
    filepath = os.path.join(temp_vector_store_dir, "index.json")
    store.save_index(filepath)
    assert os.path.exists(filepath)

    new_store = VectorStore()
    assert new_store.load_index(filepath) is True
    assert new_store.size() == 2

    # Search nearest neighbors
    sim_engine = SimilaritySearchEngine(vector_store=new_store)
    results = sim_engine.search_similar_experiences({"player_hp": 25.0}, top_k=2)

    assert len(results) == 2
    assert "similarity_score" in results[0]
    assert "episode_reference" in results[0]
    assert "outcome" in results[0]
    assert "why_retrieved" in results[0]
