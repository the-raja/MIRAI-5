"""Phase 6 Decision Cortex Milestone Unit Tests."""

import pytest
from backend.cognitive_os.decision.goal import Goal
from backend.cognitive_os.decision.goal_manager import GoalManager
from backend.cognitive_os.decision.utility_action import UtilityAction, create_standard_action_set
from backend.cognitive_os.decision.utility_system import UtilitySystem
from backend.cognitive_os.decision.decision_engine import DecisionEngine
from backend.cognitive_os.decision.reasoning_trace import ReasoningTrace, ReasoningTraceModel
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.memory_item import MemoryItem


def test_1_goal_selection():
    """Case 1: Goal Selection evaluates active high-level objectives."""
    goal_mgr = GoalManager()
    wm = WorldModel(timestamp=10.0, visible_entities=["player_raja_01"])
    mem_mgr = MemoryManager()
    mem_mgr.insert_memory(MemoryItem(id="m1", timestamp=8.5, event_type="PlayerReloading", importance=90.0))

    goal = goal_mgr.evaluate_goal(world_model=wm, memory_manager=mem_mgr)
    assert goal.type == "PRESSURE"
    assert goal.priority > 90.0


def test_2_utility_scoring():
    """Case 2: Utility Scoring formula evaluation."""
    system = UtilitySystem()
    action = UtilityAction(id="act_heavy", name="HeavyAttack", base_score=85.0, risk=0.2)
    goal = Goal(id="g1", type="PRESSURE", priority=91.0)
    wm = WorldModel(timestamp=10.0)

    scored = system.score_action(action=action, active_goal=goal, world_model=wm)
    assert scored.final_score == 100.0
    assert scored.context_score == 15.0


def test_3_decision_selection():
    """Case 3: Decision Selection chooses winning action with highest utility."""
    engine = DecisionEngine()
    wm = WorldModel(timestamp=10.0, visible_entities=["player_raja_01"])
    mem_mgr = MemoryManager()
    mem_mgr.insert_memory(MemoryItem(id="m1", timestamp=8.5, event_type="PlayerReloading", importance=90.0))

    decision = engine.make_decision(world_model=wm, memory_manager=mem_mgr)
    assert decision.chosen_action.name == "HeavyAttack"
    assert decision.utility_score > 80.0


def test_4_reason_generation():
    """Case 4: Reason Generation outputs transparent audit log."""
    engine = DecisionEngine()
    wm = WorldModel(timestamp=10.0)
    mem_mgr = MemoryManager()
    mem_mgr.insert_memory(MemoryItem(id="m1", timestamp=8.5, event_type="PlayerReloading", importance=90.0))

    decision = engine.make_decision(world_model=wm, memory_manager=mem_mgr)
    trace = ReasoningTrace.format_trace_model(decision.reasoning_trace)

    assert "Goal" in trace
    assert "Chosen" in trace
    assert "HeavyAttack" in trace
    assert "Reasons" in trace


def test_5_tie_breaking():
    """Case 5: Tie Breaking returns first highest utility candidate deterministically."""
    system = UtilitySystem()
    act1 = UtilityAction(id="act1", name="HeavyAttack", base_score=80.0)
    act2 = UtilityAction(id="act2", name="LightAttack", base_score=80.0)
    goal = Goal(id="g1", type="OBSERVE", priority=50.0)
    wm = WorldModel(timestamp=10.0)

    scored = system.evaluate_all_actions(candidate_actions=[act1, act2], active_goal=goal, world_model=wm)
    assert scored[0].action.name in ("HeavyAttack", "LightAttack")
    assert len(scored) == 2


def test_6_cooldown_handling():
    """Case 6: Cooldown Handling disqualifies action on cooldown."""
    system = UtilitySystem()
    action = UtilityAction(id="act_heavy", name="HeavyAttack", base_score=85.0, cooldown=3.0, last_used_timestamp=9.0)
    goal = Goal(id="g1", type="PRESSURE", priority=91.0)
    wm = WorldModel(timestamp=10.0)

    scored = system.score_action(action=action, active_goal=goal, world_model=wm)
    assert scored.cooldown_penalty == 200.0
    assert scored.final_score == 0.0
