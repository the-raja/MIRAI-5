"""Unit tests for MIRAI SDK and Plugin Ecosystem."""

import pytest
from sdk.python.mirai_sdk import MiraiSDK
from plugins.prediction.prediction_plugins import XGBoostPlugin, TransformerPlugin, RuleBasedPlugin
from plugins.planner.planner_plugins import AStarPlugin, BeamSearchPlugin, GOAPPlugin
from plugins.memory.memory_plugins import FAISSPlugin, HNSWPlugin, SQLitePlugin
from plugins.pygame.mirai_pygame import PygameMiraiController


def test_python_sdk_observe_tick_learn():
    sdk = MiraiSDK(session_id="sdk_test_01")
    sdk.observe({"timestamp": 1.0, "metadata": {"player_hp": 80.0}})
    action = sdk.tick()

    assert action in ["Dash", "HeavyAttack", "Block", "Retreat", "Attack"]
    res = sdk.learn({"outcome": "VICTORY"})
    assert res["status"] == "LEARNING_UPDATED"


def test_swappable_prediction_plugins():
    xgb = XGBoostPlugin()
    tf = TransformerPlugin()
    rb = RuleBasedPlugin()

    r1 = xgb.predict({})
    r2 = tf.predict({})
    r3 = rb.predict({})

    assert r1["plugin"] == "XGBoost"
    assert r2["plugin"] == "Transformer"
    assert r3["plugin"] == "RuleBased"


def test_swappable_planner_plugins():
    astar = AStarPlugin()
    beam = BeamSearchPlugin()
    goap = GOAPPlugin()

    p1 = astar.plan("WIN")
    p2 = beam.plan("WIN")
    p3 = goap.plan("WIN")

    assert p1["plugin"] == "A*"
    assert p2["plugin"] == "BeamSearch"
    assert p3["plugin"] == "GOAP"


def test_swappable_memory_plugins():
    faiss = FAISSPlugin()
    hnsw = HNSWPlugin()
    sqlite = SQLitePlugin()

    m1 = faiss.query([0.1]*16)
    m2 = hnsw.query([0.1]*16)
    m3 = sqlite.query([0.1]*16)

    assert m1["backend"] == "FAISS"
    assert m2["backend"] == "HNSW"
    assert m3["backend"] == "SQLite"


def test_pygame_integration_plugin():
    ctrl = PygameMiraiController()
    act = ctrl.update_frame(pygame_player_pos=(100, 200), player_hp=50.0)
    assert act is not None
