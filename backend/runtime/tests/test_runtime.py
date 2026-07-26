"""Unit tests for MiraiRuntime and RuntimeSession."""

import pytest
from backend.runtime.runtime import MiraiRuntime
from backend.runtime.session import RuntimeSession


def test_mirai_runtime_observe_tick_learn_loop():
    session = MiraiRuntime(session_id="test_sess_01")

    # 1. Observe frame
    session.observe({"timestamp": 10.0, "visible_entities": ["player_01"], "metadata": {"player_hp": 80.0}})

    # 2. Tick action
    action = session.tick()
    assert action in ["Dash", "HeavyAttack", "Block", "Retreat", "Attack"]

    # 3. Learn result
    learn_res = session.learn({"outcome": "VICTORY", "damage_dealt": 95.0})
    assert learn_res["status"] == "LEARNING_UPDATED"
    assert learn_res["outcome"] == "VICTORY"


def test_runtime_session_wrapper():
    sess = RuntimeSession(session_id="wrapper_sess")

    sess.observe({"timestamp": 5.0})
    act = sess.tick()
    assert act is not None

    res = sess.learn({"outcome": "DEFEAT"})
    assert res["outcome"] == "DEFEAT"
