"""Unit tests for UtilitySystem scoring formula and explainable sub-scores."""

import pytest
from backend.cognitive_os.decision.utility_action import UtilityAction, create_standard_action_set
from backend.cognitive_os.decision.goal import Goal
from backend.cognitive_os.decision.utility_system import UtilitySystem
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.memory_item import MemoryItem


def test_utility_system_heavy_attack_example_scoring():
    system = UtilitySystem()
    action = UtilityAction(id="act_heavy", name="HeavyAttack", base_score=60.0)
    goal = Goal(id="g1", type="PRESSURE", priority=91.0)
    wm = WorldModel(timestamp=10.0, metadata={"boss_hp_pct": 0.15})

    mem_mgr = MemoryManager()
    mem_mgr.insert_memory(MemoryItem(id="m1", timestamp=8.5, event_type="PlayerReloading", importance=90.0))

    scored = system.score_action(action=action, active_goal=goal, world_model=wm, memory_manager=mem_mgr)

    # Base(60) + Context(15) + Reload(25) + Range(15) - LowBossHP(30) = 85.0 (without range) or 70.0
    assert scored.base_score == 60.0
    assert scored.reload_bonus == 25.0
    assert scored.boss_low_hp_modifier == -30.0
    assert scored.final_score > 0.0


def test_utility_system_heal_example_scoring():
    system = UtilitySystem()
    action = UtilityAction(id="act_heal", name="Heal", base_score=30.0)
    goal = Goal(id="g1", type="HEAL", priority=95.0)
    wm = WorldModel(timestamp=10.0, metadata={"boss_hp_pct": 0.15})

    scored = system.score_action(action=action, active_goal=goal, world_model=wm)

    # Base(30) + Context(25) + BossHPLow(50) + EnemyFar(20) = 125.0
    assert scored.base_score == 30.0
    assert scored.boss_low_hp_modifier == 50.0
    assert scored.range_bonus == 20.0
    assert scored.final_score >= 85.0
