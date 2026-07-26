"""MIRAI v2 — Phase 11 Temporal Intelligence Demonstrator Runner.

Executes temporal action sequence prediction:
Sequence -> LSTM Temporal Model -> Explainable Sequence Prediction

Outputs the exact temporal prediction console output.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.temporal.temporal_model import LSTMTemporalModel


def run_temporal_demo() -> None:
    model = LSTMTemporalModel()

    input_sequence = ["Attack", "Attack", "Reload", "Attack"]
    pred = model.predict_sequence(input_sequence)

    print("\n" + "=" * 40)
    print("Temporal Prediction")
    print("=" * 40 + "\n")

    print("Sequence")
    for act in input_sequence:
        print(act)
    print()

    print("Prediction")
    display_action = "Left Dodge" if pred.action == "DodgeLeft" else pred.action
    print(f"{display_action}\n")

    print("Confidence")
    print(f"{int(pred.confidence * 100)}%\n")

    print("Reason")
    print(f"{pred.reason}")

    print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    run_temporal_demo()
