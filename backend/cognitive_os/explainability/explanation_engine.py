"""ExplanationEngine module.

Merges multi-subsystem evidence (Prediction, Threat, Experience, Skill, Planner, Utility) into a unified ReasoningTrace.
Renders clean console explanation cards.
"""

from typing import Dict, Any, Optional
from backend.cognitive_os.explainability.reasoning_trace import ReasoningTrace


class ExplanationEngine:
    def __init__(self) -> None:
        pass

    def merge_subsystem_trace(
        self,
        frame_index: int = 1,
        prediction: Optional[Dict[str, Any]] = None,
        threat: Optional[Dict[str, float]] = None,
        experience: Optional[Dict[str, Any]] = None,
        skill: Optional[Dict[str, Any]] = None,
        planner: Optional[Dict[str, Any]] = None,
        utility: Optional[Dict[str, float]] = None,
        final_decision: str = "Dash"
    ) -> ReasoningTrace:
        """Merges all Cognitive OS subsystem evidence into a single ReasoningTrace."""
        pred = prediction or {"intent": "Reload", "confidence": 0.94}
        thr = threat or {"healing": 0.91}
        exp = experience or {"episode": "Episode 102", "similarity": 0.94}
        skl = skill or {"tier": "Expert", "score": 92}
        pln = planner or {"goal": "Pressure Player", "plan": "Plan A"}
        utl = utility or {"Dash": 0.88, "Block": 0.63}

        summary = (
            f"Prediction: {pred['intent']} ({pred['confidence']*100:.0f}%) | "
            f"Threat: Healing = {thr.get('healing', 0.91):.2f} | "
            f"Goal: {pln['goal']} -> {final_decision}"
        )

        return ReasoningTrace(
            frame_index=frame_index,
            prediction=pred,
            threat=thr,
            experience=exp,
            skill=skl,
            planner=pln,
            utility=utl,
            final_decision=final_decision,
            reasoning_summary=summary
        )

    def format_explanation_card(self, trace: ReasoningTrace) -> str:
        """Renders explanation trace into exact requested XAI console report card."""
        lines = []
        lines.append("====================================")
        lines.append(f"Decision: {trace.final_decision}")
        lines.append("====================================")
        lines.append("\nReasoning")
        lines.append("\nPrediction\n-------------")
        lines.append(f"{trace.prediction['intent']} ({trace.prediction['confidence']*100:.0f}%)")

        lines.append("\nThreat\n-------------")
        for k, v in trace.threat.items():
            lines.append(f"{k.capitalize()} = {v:.2f}")

        lines.append("\nExperience\n-------------")
        lines.append(f"{trace.experience['episode']}")
        lines.append(f"Similarity {trace.experience['similarity']:.2f}")

        lines.append("\nSkill Rating\n-------------")
        lines.append(f"{trace.skill['tier']} ({trace.skill['score']})")

        lines.append("\nPlanner\n-------------")
        lines.append(f"{trace.planner['plan']}")

        lines.append("\nGoal\n-------------")
        lines.append(f"{trace.planner['goal']}")

        lines.append("\nUtility\n-------------")
        for act, score in trace.utility.items():
            lines.append(f"{act}: {score:.2f}")

        lines.append("\nFinal Decision\n-------------")
        lines.append(trace.final_decision)
        lines.append("====================================")

        return "\n".join(lines)
