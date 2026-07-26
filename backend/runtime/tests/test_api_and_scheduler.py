"""Unit tests for EventAPI, StateAPI, and 7-Stage Tick Scheduler."""

import pytest
from backend.runtime.runtime import MiraiRuntime
from backend.runtime.event_api import EventAPI
from backend.runtime.state_api import StateAPI


def test_event_api_emitting_game_events():
    api = EventAPI()
    # Emits high-level game events without throwing exceptions
    api.emit_event("PlayerMoved", {"x": 10, "y": 5})
    api.emit_event("PlayerAttacked", {"weapon": "Sword"})
    api.emit_event("PlayerReloaded", {})
    api.emit_event("BossDamaged", {"amount": 45})


def test_state_api_summary_exposure():
    api = StateAPI()
    summary = api.get_state_summary()

    assert "current_goal" in summary
    assert "current_plan" in summary
    assert "current_prediction" in summary
    assert "current_confidence" in summary
    assert "memory_summary" in summary


def test_7_stage_single_tick_scheduler():
    runtime = MiraiRuntime()

    # Single tick executes Observe -> Perceive -> Predict -> Plan -> Decide -> Execute -> Learn
    action = runtime.tick({"timestamp": 12.0, "metadata": {"player_hp": 75.0}})
    assert action in ["Dash", "HeavyAttack", "Block", "Retreat", "Attack"]

    summary = runtime.get_state_summary()
    assert summary["current_goal"] is not None
    assert len(summary["current_plan"]) > 0
