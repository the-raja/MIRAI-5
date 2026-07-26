"""MIRAI v2 — Phase 8 Continuous Learning Engine & Closed-Loop Cognitive OS Kernel Demonstrator Runner.

Executes the full 12-Stage Closed-Loop Cognitive OS Pipeline:
Telemetry -> Perception -> Attention -> Working Memory -> World Model -> Episodic Memory -> Semantic Memory -> Prediction -> Goal -> Utility -> Decision -> Learning Engine

Outputs the post-match Training Report and closes the cognitive loop.
"""

import time
import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event
from backend.cognitive_os.telemetry.collector import TelemetryCollector
from backend.cognitive_os.perception.perception_engine import PerceptionEngine
from backend.cognitive_os.attention.attention_engine import AttentionEngine
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.episodic.episode_manager import EpisodeManager
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager
from backend.cognitive_os.context.world_model import WorldModelEngine, WorldModel
from backend.cognitive_os.decision.decision_engine import DecisionEngine
from backend.cognitive_os.learning.learning_engine import LearningEngine
from backend.cognitive_os.learning.training_report import TrainingReport


def run_closed_loop_cognitive_os_demo() -> None:
    bus = EventBus()

    collector = TelemetryCollector(event_bus=bus)
    perception = PerceptionEngine(event_bus=bus)
    attention = AttentionEngine(event_bus=bus)
    memory_manager = MemoryManager(event_bus=bus)
    world_model_engine = WorldModelEngine(event_bus=bus)
    episode_manager = EpisodeManager(storage_dir=r"backend/data/episodes", event_bus=bus)
    semantic_manager = SemanticManager(event_bus=bus)
    decision_engine = DecisionEngine(event_bus=bus)
    learning_engine = LearningEngine(event_bus=bus)

    current_sim_time = 1000.0

    # 1. Prediction Generation (Frame 402)
    prediction = decision_engine.prediction_engine.generate_prediction(
        world_model=WorldModel(timestamp=current_sim_time),
        memory_manager=memory_manager,
        semantic_manager=semantic_manager,
        recent_actions=["Attack", "Attack", "Attack"]
    )

    # 2. Decision Cortex Execution
    decision = decision_engine.make_decision(
        world_model=WorldModel(timestamp=current_sim_time),
        memory_manager=memory_manager,
        semantic_manager=semantic_manager,
        recent_actions=["Attack", "Attack", "Attack"]
    )

    # 3. Battle Finished -> Episode Created
    completed_episode = Episode(
        episode_id="34",
        timestamp=current_sim_time + 85.0,
        winner="Boss",
        battle_summary=BattleSummary(
            match_id="34",
            winner="Boss",
            duration_seconds=85.0,
            reload_count=12,
            preferred_dodge="Left"
        )
    )

    # 4. Learning Engine Processing -> LearningSession
    session = learning_engine.process_completed_episode(completed_episode)

    # 5. Print Closed-Loop Training Report
    TrainingReport.print_learning_report(session)


if __name__ == "__main__":
    run_closed_loop_cognitive_os_demo()
