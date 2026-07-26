"""PlannerInspector & PredictionTimelineTracker module.

Inspects Current Goal -> Current Plan -> Execution Progress and tracks Prediction Confidence Timeline over combat time.
"""

from typing import Dict, Any, List


class PlannerInspector:
    @staticmethod
    def get_planner_inspection_data() -> Dict[str, Any]:
        """Returns Current Goal -> Current Plan -> Execution Progress state."""
        return {
            "current_goal": "Pressure Player",
            "current_plan": [
                {"step": 1, "action": "Dash", "status": "COMPLETED"},
                {"step": 2, "action": "Heavy Attack", "status": "EXECUTING"},
                {"step": 3, "action": "Block", "status": "PENDING"},
                {"step": 4, "action": "Retreat", "status": "PENDING"}
            ],
            "execution_progress_pct": 50.0,
            "overall_status": "EXECUTING",
            "risk_score": 0.15,
            "expected_reward": 85.0
        }

    @staticmethod
    def get_prediction_confidence_timeline() -> List[Dict[str, Any]]:
        """Returns time series of Prediction Confidence over time."""
        return [
            {"time_sec": 1.0, "confidence_pct": 74.0, "prediction": "Idle"},
            {"time_sec": 2.0, "confidence_pct": 81.0, "prediction": "Attack"},
            {"time_sec": 3.0, "confidence_pct": 88.0, "prediction": "Attack"},
            {"time_sec": 4.0, "confidence_pct": 94.0, "prediction": "Reload"},
            {"time_sec": 5.0, "confidence_pct": 91.0, "prediction": "DodgeLeft"}
        ]
