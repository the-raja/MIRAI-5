"""MIRAI v2 — Phase 10 Real Machine Learning (XGBoost Intent Prediction) Demonstrator Runner.

Executes the ML prediction pipeline:
Features -> XGBoost Model -> Explainable Prediction -> Top Contributing Features

Outputs the exact explainable prediction console output.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel


def run_explainable_ml_demo() -> None:
    model = IntentPredictionModel()

    sample_features = {
        "distance": 2.5,
        "player_hp": 80.0,
        "boss_hp": 70.0,
        "stamina": 90.0,
        "weapon": "Shotgun",
        "current_action": "RELOAD",
        "last_action": "ATTACK",
        "last_5_action_histogram": "ATTACK:3",
        "aggression_score": 0.85,
        "reload_frequency": 12,
        "preferred_dodge": "Left",
        "preferred_weapon": "Shotgun",
        "time_since_reload": 1.2,
        "time_since_heal": 40.0,
        "time_since_damage": 5.0,
        "boss_cooldown": 2.0,
        "player_cooldown": 0.0,
        "last_5_actions": ["Attack", "Attack", "Attack"]
    }

    pred = model.predict(sample_features)
    top_features = pred.metadata.get("top_contributing_features", [
        "Distance",
        "Aggression",
        "Reload Frequency",
        "Time Since Last Reload",
        "Last Action"
    ])

    print("\n" + "=" * 40)
    print("EXPLAINABLE ML INTENT PREDICTION")
    print("=" * 40 + "\n")

    print("Prediction")
    print(f"{pred.action}\n")

    print("Confidence")
    print(f"{int(pred.confidence * 100)}%\n")

    print("Top Contributing Features")
    for feat_name in top_features:
        print(f"{feat_name}")

    print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    run_explainable_ml_demo()
