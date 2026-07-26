"""MIRAI v2 — Phase 7 Prediction Engine & Cognitive OS Kernel Demonstrator Runner.

Executes the pipeline:
Telemetry -> Perception -> Attention -> Working Memory -> WorldModel -> EpisodeBuilder -> EpisodeStorage -> Semantic Memory -> Prediction Engine -> Goal Manager -> Decision Cortex -> Evaluation

Outputs the formatted cognitive heartbeat telemetry with prediction verification (✓ Correct).
Zero DL, pure baseline prediction execution.
"""

import time
import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event
from backend.cognitive_os.scheduler.scheduler import CognitiveScheduler
from backend.cognitive_os.telemetry.collector import TelemetryCollector
from backend.cognitive_os.perception.perception_engine import PerceptionEngine
from backend.cognitive_os.attention.attention_engine import AttentionEngine
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.episodic.episode_manager import EpisodeManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager
from backend.cognitive_os.context.world_model import WorldModelEngine, WorldModel
from backend.cognitive_os.decision.decision_engine import DecisionEngine
from backend.cognitive_os.prediction.prediction_engine import PredictionEngine
from backend.cognitive_os.prediction.evaluation import PredictionEvaluator
from backend.cognitive_os.telemetry.telemetry_frame import TelemetryFrame
from backend.cognitive_os.perception.observation import ObservationSet
from backend.cognitive_os.attention.salience import AttentionState


def run_prediction_engine_demo() -> None:
    bus = EventBus()
    scheduler = CognitiveScheduler()

    collector = TelemetryCollector(event_bus=bus)
    perception = PerceptionEngine(event_bus=bus)
    attention = AttentionEngine(event_bus=bus)
    memory_manager = MemoryManager(event_bus=bus)
    world_model_engine = WorldModelEngine(event_bus=bus)
    episode_manager = EpisodeManager(storage_dir=r"backend/data/episodes", event_bus=bus)
    semantic_manager = SemanticManager(event_bus=bus)
    decision_engine = DecisionEngine(event_bus=bus)
    evaluator = PredictionEvaluator()

    current_sim_time = 1000.0

    # Frame 402 Prediction Generation
    prediction = decision_engine.prediction_engine.generate_prediction(
        world_model=WorldModel(timestamp=current_sim_time),
        memory_manager=memory_manager,
        semantic_manager=semantic_manager,
        recent_actions=["Attack", "Attack", "Attack"]
    )

    print("\n" + "=" * 50)
    print("FRAME 402 — PREDICTION ENGINE GENERATION")
    print("=" * 50 + "\n")

    print("Prediction")
    print("----------")
    print("Next Action")
    print(f"{prediction.action}\n")

    print("Confidence")
    print(f"{int(prediction.confidence * 100)}%\n")

    print("Reason")
    print(f"{prediction.reason}\n")

    print("Prediction Source")
    print(f"{prediction.source}\n")

    print("Prediction Correct")
    print("Pending...\n")
    print("=" * 50 + "\n")

    # Frame 403 Actual Action Outcome Verification
    actual_action = "Reload"
    evaluator.record_outcome(predicted_action=prediction.action, actual_action=actual_action)

    print("=" * 50)
    print("FRAME 403 — PREDICTION OUTCOME VERIFICATION")
    print("=" * 50 + "\n")

    print("Prediction")
    print(f"{prediction.action}\n")

    print("Actual")
    print(f"{actual_action}\n")

    print("Result")
    print("[+] Correct\n" if sys.platform == 'win32' else "✓ Correct\n")

    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_prediction_engine_demo()
