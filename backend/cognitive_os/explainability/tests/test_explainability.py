"""Unit tests for Explainability (XAI) modules."""

import pytest
from backend.cognitive_os.explainability.reasoning_trace import ReasoningTrace
from backend.cognitive_os.explainability.explanation_engine import ExplanationEngine
from backend.cognitive_os.explainability.decision_audit import DecisionAuditEngine


def test_reasoning_trace_schema():
    trace = ReasoningTrace(
        frame_index=10,
        final_decision="Heavy Attack"
    )
    assert trace.frame_index == 10
    assert trace.final_decision == "Heavy Attack"
    assert "intent" in trace.prediction


def test_explanation_engine_merge_and_format():
    engine = ExplanationEngine()
    trace = engine.merge_subsystem_trace(
        frame_index=24,
        prediction={"intent": "Reload", "confidence": 0.94},
        threat={"healing": 0.91},
        experience={"episode": "Episode 102", "similarity": 0.94},
        skill={"tier": "Expert", "score": 92},
        planner={"goal": "Pressure Player", "plan": "Plan A"},
        utility={"Dash": 0.88, "Block": 0.63},
        final_decision="Dash"
    )

    card = engine.format_explanation_card(trace)
    assert "Decision: Dash" in card
    assert "Reload (94%)" in card
    assert "Healing = 0.91" in card
    assert "Episode 102" in card
    assert "Expert (92)" in card
    assert "Pressure Player" in card


def test_decision_audit_engine():
    audit = DecisionAuditEngine()
    engine = ExplanationEngine()

    t1 = engine.merge_subsystem_trace(frame_index=1, final_decision="Dash")
    t2 = engine.merge_subsystem_trace(frame_index=2, final_decision="Heavy Attack")

    audit.record_trace(t1)
    audit.record_trace(t2)

    assert len(audit.get_all_traces()) == 2
    fetched = audit.get_trace_at_frame(2)
    assert fetched.final_decision == "Heavy Attack"
