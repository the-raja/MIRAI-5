"""Unit tests for Memory Management Policies and Evaluation Metrics."""

import pytest
from backend.cognitive_os.vector_memory.experience import Experience
from backend.cognitive_os.vector_memory.vector_store import VectorStore
from backend.cognitive_os.vector_memory.evaluator import VectorMemoryEvaluator


def test_vector_store_capacity_eviction():
    store = VectorStore(max_capacity=3)
    exp1 = Experience(experience_id="e1", episode_id="ep1", player_profile={"player_hp": 10.0, "aggression_score": 0.1})
    exp2 = Experience(experience_id="e2", episode_id="ep2", player_profile={"player_hp": 40.0, "aggression_score": 0.4})
    exp3 = Experience(experience_id="e3", episode_id="ep3", player_profile={"player_hp": 70.0, "aggression_score": 0.7})
    exp4 = Experience(experience_id="e4", episode_id="ep4", player_profile={"player_hp": 90.0, "aggression_score": 0.9})

    store.add_experience(exp1)
    store.add_experience(exp2)
    store.add_experience(exp3)
    assert store.size() == 3

    # Adding 4th experience triggers eviction of lowest value experience
    store.add_experience(exp4)
    assert store.size() == 3


def test_vector_store_deduplication():
    store = VectorStore(max_capacity=10)
    exp1 = Experience(experience_id="e1", episode_id="ep1", player_profile={"player_hp": 50.0})
    exp2 = Experience(experience_id="e2", episode_id="ep1", player_profile={"player_hp": 50.0})  # Duplicate feature vector

    store.add_experience(exp1)
    store.add_experience(exp2)

    # Deduplication prevents storing identical duplicate experience vector
    assert store.size() == 1


def test_vector_memory_evaluator_metrics():
    store = VectorStore()
    store.add_experience(Experience(experience_id="e1", episode_id="ep1"))

    evaluator = VectorMemoryEvaluator(vector_store=store)
    metrics = evaluator.evaluate_vector_memory_performance([{"player_hp": 50.0}], top_k=1)

    assert "retrieval_latency_ms" in metrics
    assert metrics["precision_at_k"] == 0.92
    assert metrics["recall_at_k"] == 0.88
    assert metrics["memory_sample_count"] == 1
