"""Unit tests for ExperienceRetrievalEngine and ExperienceRetrievalReportFormatter."""

import pytest
from backend.cognitive_os.vector_memory.retrieval_engine import ExperienceRetrievalEngine
from backend.cognitive_os.vector_memory.retrieval_report import ExperienceRetrievalReportFormatter


def test_experience_retrieval_and_report_formatter():
    engine = ExperienceRetrievalEngine()
    current_situation = {"player_hp": 34.0, "boss_hp": 48.0}

    data = engine.query_experiences(current_situation, top_k=3)

    assert data["recommended_strategy"] == "Pressure Player"
    assert data["confidence"] == 0.93
    assert len(data["top_matches"]) == 3

    report = ExperienceRetrievalReportFormatter.format_retrieval_report(data)
    assert "Experience Retrieval" in report
    assert "Player HP: 34%" in report
    assert "Boss HP: 48%" in report
    assert "Episode 102" in report
    assert "Similarity 0.94" in report
    assert "Winner: Boss" in report
    assert "Pressure Player" in report
    assert "93%" in report
