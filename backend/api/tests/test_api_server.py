"""Unit tests for Phase 0 Backend REST & WebSocket APIs."""

import pytest
from fastapi.testclient import TestClient
from backend.api.server import app
from backend.api.websocket_manager import WebSocketManager

client = TestClient(app)


def test_root_status():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "MIRAI v2 API Server Active"


def test_get_state_endpoint():
    res = client.get("/api/state")
    assert res.status_code == 200
    data = res.json()
    assert "current_goal" in data
    assert "boss_hp" in data


def test_get_memory_endpoint():
    res = client.get("/api/memory")
    assert res.status_code == 200
    data = res.json()
    assert "working_memory" in data
    assert "vector_memory" in data


def test_get_behavior_endpoint():
    res = client.get("/api/behavior")
    assert res.status_code == 200
    assert "active_bt_node" in res.json()


def test_get_prediction_endpoint():
    res = client.get("/api/prediction")
    assert res.status_code == 200
    assert res.json()["intent_prediction"] == "Reload"


def test_get_planner_endpoint():
    res = client.get("/api/planner")
    assert res.status_code == 200
    assert "htn_decomposition" in res.json()


def test_get_emotion_endpoint():
    res = client.get("/api/emotion")
    assert res.status_code == 200
    assert res.json()["dominant_emotion"] == "Aggressive"


def test_battle_start_action_end_lifecycle():
    # 1. Start battle
    start_res = client.post("/api/battle/start", json={"session_id": "b_99", "player_id": "raja"})
    assert start_res.status_code == 200
    assert start_res.json()["status"] == "BATTLE_STARTED"

    # 2. Action
    act_res = client.post("/api/battle/action", json={"session_id": "b_99", "action": "Attack", "timestamp": 1.0})
    assert act_res.status_code == 200
    assert act_res.json()["status"] == "ACTION_PROCESSED"

    # 3. End battle
    end_res = client.post("/api/battle/end", json={"session_id": "b_99", "outcome": "VICTORY"})
    assert end_res.status_code == 200
    assert end_res.json()["status"] == "BATTLE_ENDED"


def test_websocket_telemetry_event_creation():
    mgr = WebSocketManager()
    evt = mgr.create_telemetry_event(
        player_hp=60.0,
        boss_hp=85.0,
        boss_action="Dash",
        player_action="Attack",
        threat_update={"healing": 0.91},
        prediction_update={"intent": "Reload", "confidence": 0.94},
        emotion_update="Aggressive",
        memory_trigger="Episode 102",
        planner_change="Plan A"
    )

    assert evt["player_hp"] == 60.0
    assert evt["boss_action"] == "Dash"
    assert evt["prediction_update"]["confidence"] == 0.94
