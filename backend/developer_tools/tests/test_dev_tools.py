"""Unit tests for Developer Tools & Visualization Suite modules."""

import pytest
from backend.developer_tools.cognitive_graph import CognitiveGraphTracker
from backend.developer_tools.memory_inspector import MemoryInspector
from backend.developer_tools.planner_inspector import PlannerInspector
from backend.developer_tools.replay_viewer import ReplayViewer
from backend.developer_tools.benchmark_dashboard import BenchmarkDashboard


def test_cognitive_graph_tracker():
    tracker = CognitiveGraphTracker()
    state = tracker.get_live_graph_state(frame_index=10)

    assert state["frame_index"] == 10
    assert len(state["nodes"]) == 5
    assert len(state["edges"]) == 4


def test_memory_inspector_all_tiers():
    memories = MemoryInspector.inspect_all_memories()

    assert "working_memory" in memories
    assert "episodic_memory" in memories
    assert "semantic_memory" in memories
    assert "vector_memory" in memories


def test_planner_inspector_and_timeline():
    data = PlannerInspector.get_planner_inspection_data()
    timeline = PlannerInspector.get_prediction_confidence_timeline()

    assert data["current_goal"] == "Pressure Player"
    assert data["execution_progress_pct"] == 50.0
    assert len(timeline) > 0


def test_replay_viewer_frame_inspection():
    viewer = ReplayViewer()
    state = viewer.get_frame_state(frame_index=24)

    assert state["frame_index"] == 24
    assert "memories" in state
    assert "predictions" in state
    assert "plan" in state
    assert "reasoning" in state


def test_benchmark_dashboard_kpis():
    data = BenchmarkDashboard.get_benchmark_dashboard_data()

    assert data["win_rate_pct"] == 93.4
    assert data["avg_latency_ms"] == 4.2
    assert data["prediction_accuracy_pct"] == 91.0
