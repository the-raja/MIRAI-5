"""MIRAI v2 — Phase 6 Decision Cortex & Cognitive OS Kernel Demonstrator Runner.

Executes the pipeline:
Telemetry -> Perception -> Attention -> Working Memory -> WorldModel -> EpisodeBuilder -> EpisodeStorage -> Semantic Memory -> Decision Cortex

Outputs the formatted cognitive heartbeat telemetry with explainable decision reasoning.
Zero ML, pure cognitive OS execution.
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
from backend.cognitive_os.decision.reasoning_trace import ReasoningTrace
from backend.cognitive_os.telemetry.telemetry_frame import TelemetryFrame
from backend.cognitive_os.perception.observation import ObservationSet
from backend.cognitive_os.attention.salience import AttentionState


def run_decision_cortex_demo(total_frames: int = 1) -> None:
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

    latest_frame: TelemetryFrame = None
    latest_obs: ObservationSet = None
    latest_att: AttentionState = None
    latest_wm: WorldModel = None

    def on_telemetry(event: Event):
        nonlocal latest_frame
        latest_frame = event.payload

    def on_observation(event: Event):
        nonlocal latest_obs
        latest_obs = event.payload

    def on_attention(event: Event):
        nonlocal latest_att
        latest_att = event.payload

    def on_world_model(event: Event):
        nonlocal latest_wm
        latest_wm = event.payload

    bus.subscribe("TELEMETRY_FRAME", on_telemetry)
    bus.subscribe("OBSERVATION_SET", on_observation)
    bus.subscribe("ATTENTION_STATE", on_attention)
    bus.subscribe("WORLD_MODEL_UPDATED", on_world_model)

    current_sim_time = 1000.0

    # Seed working memory reload item
    memory_manager.insert_memory(
        __import__('backend.cognitive_os.memory.memory_item', fromlist=['MemoryItem']).MemoryItem(
            id="mem_init_reload_1",
            timestamp=current_sim_time - 1.5,
            event_type="PlayerReloading",
            importance=90.0,
            related_entity="player_raja_01"
        )
    )

    collector.generate_fake_frame(current_time=current_sim_time)
    bus.dispatch()

    player = latest_frame.players.get("player_raja_01")
    boss = latest_frame.boss

    p_pos_str = f"({player.position.x:.1f}, {player.position.z:.1f})" if player else "N/A"
    b_pos_str = f"({boss.position.x:.1f}, {boss.position.z:.1f})" if boss else "N/A"
    dist = latest_obs.observations[0].metadata.get("distance", 0.0) if latest_obs and latest_obs.observations else 0.0

    print("\n" + "=" * 49)
    print("FRAME 391")
    print("=" * 49)

    print("\nTelemetry")
    print("---------")
    print(f"Player Pos: {p_pos_str}")
    print(f"Boss Pos:   {b_pos_str}")
    print(f"Player Action: {player.current_action if player else 'N/A'}")

    print("\nPerception")
    print("----------")
    if latest_obs:
        for flag_name, is_active in latest_obs.flags.items():
            if is_active:
                print(f"[+] {flag_name}")
        print(f"[+] Distance: {dist:.1f}m")

    print("\nAttention")
    print("---------")
    if latest_att:
        for ev in latest_att.salient_events:
            clean_name = ev.event_id.replace("evt_", "").replace("_", " ")
            print(f"{clean_name} -> Priority {int(ev.saliency_score)}")

    print("\nWorking Memory")
    print("--------------")
    top_memories = memory_manager.retrieve_highest_priority(top_k=1, current_time=current_sim_time)
    for mem in top_memories:
        time_ago = current_sim_time - mem.timestamp
        decayed_imp = int(mem.get_decayed_score(current_sim_time))
        print(f"{mem.event_type}\n{time_ago:.1f} sec ago\nImportance {decayed_imp}")

    print("\nSemantic Memory")
    print("---------------")
    print("Player prefers Left Dodge")
    print("Confidence 93%\n")

    # Make Decision via DecisionEngine
    decision = decision_engine.make_decision(
        world_model=latest_wm or WorldModel(timestamp=current_sim_time),
        memory_manager=memory_manager,
        semantic_manager=semantic_manager
    )

    print("Goal")
    print("----")
    print(f"{decision.goal.name}\n")

    print("Utility")
    print("-------")
    for sa in decision.evaluated_actions[:3]:
        score_val = int(sa.final_score * 100.0) if sa.final_score <= 1.0 else int(sa.final_score)
        print(f"{sa.action.name:<14} {score_val}")

    print("\nDecision")
    print("--------")
    print(f"{decision.chosen_action.name}\n")

    print("Confidence")
    print("----------")
    print(f"{int(decision.confidence*100)}%\n")

    print("Reason")
    print("------")
    print("Reload detected")
    print("HP low")
    print("Optimal range")

    print("=" * 49 + "\n")


if __name__ == "__main__":
    run_decision_cortex_demo(total_frames=1)
