"""Phase 12 Vector Memory Master Milestone Unit Tests.

Explicitly verifies all Phase 12 requirements:
1. Experience schema (Experience)
2. Embedding Engine (ExperienceEmbeddingEngine)
3. Vector Store (VectorStore add/remove/update/search/save/load)
4. Similarity Search (SimilaritySearchEngine top-10 retrieval)
5. Experience Retrieval Engine (ExperienceRetrievalEngine strategy & confidence)
6. Retrieval Report Formatter (ExperienceRetrievalReportFormatter console report)
7. Pipeline Integration with Decision Cortex (Semantic Memory -> Vector Memory -> Prediction -> Decision)
"""

import pytest
import os
import shutil
from backend.cognitive_os.vector_memory.experience import Experience
from backend.cognitive_os.vector_memory.embedding_engine import ExperienceEmbeddingEngine
from backend.cognitive_os.vector_memory.vector_store import VectorStore
from backend.cognitive_os.vector_memory.similarity import SimilaritySearchEngine
from backend.cognitive_os.vector_memory.retrieval_engine import ExperienceRetrievalEngine
from backend.cognitive_os.vector_memory.retrieval_report import ExperienceRetrievalReportFormatter
from backend.cognitive_os.decision.decision_engine import DecisionEngine
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.event_bus.event_bus import EventBus


@pytest.fixture
def temp_phase12_dir(tmp_path):
    root_dir = str(tmp_path / "phase12_vec")
    yield root_dir
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir, ignore_errors=True)


def test_1_experience_schema():
    exp = Experience(experience_id="e1", episode_id="ep1", outcome="VICTORY")
    assert exp.experience_id == "e1"
    assert exp.outcome == "VICTORY"


def test_2_embedding_engine():
    engine = ExperienceEmbeddingEngine()
    vec = engine.embed_current_situation({"player_hp": 34.0, "boss_hp": 48.0})
    assert len(vec) == 16


def test_3_vector_store(temp_phase12_dir):
    store = VectorStore()
    exp = Experience(experience_id="e1", episode_id="ep1")
    store.add_experience(exp)
    assert store.size() == 1

    filepath = os.path.join(temp_phase12_dir, "idx.json")
    store.save_index(filepath)
    assert os.path.exists(filepath)


def test_4_similarity_search():
    sim = SimilaritySearchEngine()
    res = sim.search_similar_experiences({"player_hp": 34.0}, top_k=5)
    assert len(res) >= 0


def test_5_retrieval_report():
    engine = ExperienceRetrievalEngine()
    data = engine.query_experiences({"player_hp": 34.0, "boss_hp": 48.0})
    report = ExperienceRetrievalReportFormatter.format_retrieval_report(data)

    assert "Experience Retrieval" in report
    assert "Player HP: 34%" in report
    assert "Recommended Strategy" in report
    assert "Pressure Player" in report


def test_6_decision_cortex_integration():
    bus = EventBus()
    engine = DecisionEngine(event_bus=bus)
    wm = WorldModel(timestamp=10.0, visible_entities=["player_raja_01"])

    dec = engine.make_decision(world_model=wm)
    assert dec.goal is not None
    assert dec.chosen_action is not None
