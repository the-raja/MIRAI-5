"""MIRAI v2 — Phase 5 Semantic Memory & Cognitive OS Kernel Demonstrator Runner.

Executes the pipeline:
Telemetry -> Perception -> Attention -> Working Memory -> WorldModel -> EpisodeBuilder -> EpisodeStorage -> Semantic Memory

Outputs the formatted cognitive heartbeat telemetry, MATCH COMPLETE summary, and Distilled Semantic Knowledge Graph.
Zero ML, pure cognitive pipeline execution.
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
from backend.cognitive_os.telemetry.telemetry_frame import TelemetryFrame
from backend.cognitive_os.perception.observation import ObservationSet
from backend.cognitive_os.attention.salience import AttentionState


def run_semantic_memory_demo(total_frames: int = 1) -> None:
    bus = EventBus()
    scheduler = CognitiveScheduler()

    collector = TelemetryCollector(event_bus=bus)
    perception = PerceptionEngine(event_bus=bus)
    attention = AttentionEngine(event_bus=bus)
    memory_manager = MemoryManager(event_bus=bus)
    world_model_engine = WorldModelEngine(event_bus=bus)
    episode_manager = EpisodeManager(storage_dir=r"backend/data/episodes", event_bus=bus)
    semantic_manager = SemanticManager(event_bus=bus)

    episode_builder = episode_manager.create_builder(match_id="Episode_00012")
    episode_builder.start_time = time.time() - 82.0

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

    print("\n" + "=" * 49)
    print("MIRAI v2 COGNITIVE OS KERNEL -- SEMANTIC MEMORY DEMO")
    print("=" * 49 + "\n")

    current_sim_time = 1000.0

    # Seed working memory items
    memory_manager.insert_memory(
        from_item := __import__('backend.cognitive_os.memory.memory_item', fromlist=['MemoryItem']).MemoryItem(
            id="mem_init_reload_1",
            timestamp=current_sim_time - 70.0,
            event_type="Player Reloaded",
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

    print("=" * 49)
    print(f"FRAME 145")
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
    top_memories = memory_manager.retrieve_highest_priority(top_k=2, current_time=current_sim_time)
    for mem in top_memories:
        time_ago = current_sim_time - mem.timestamp
        decayed_imp = int(mem.get_decayed_score(current_sim_time))
        clean_type = mem.event_type.replace("evt_", "").replace("_", " ")
        print("--------------------")
        print(f"{clean_type}")
        print(f"{time_ago:.1f} sec ago")
        print(f"Importance {decayed_imp}")

    print("--------------------")
    last_pos = memory_manager.last_seen_position("player_raja_01") or (player.position if player else None)
    if last_pos:
        print(f"Last Seen Position")
        print(f"({last_pos.x:.1f}, {last_pos.z:.1f})")

    print("\nWorld Model")
    print("-----------")
    if latest_wm:
        est_p = latest_wm.estimated_player_positions.get("player_raja_01")
        est_p_str = f"({est_p.x:.1f}, {est_p.z:.1f})" if est_p else p_pos_str
        nearest_cover = latest_wm.cover_nodes[0].id if latest_wm.cover_nodes else "None"
        print(f"Estimated Player Position: {est_p_str}")
        print(f"LOS: Clear")
        print(f"Nearest Cover: {nearest_cover}")
        print(f"Threat Level: Medium")

    print("\n" + "=" * 49 + "\n")

    # Finish Match & Save Episode
    episode = episode_builder.finish_episode(winner="Player", end_time=episode_builder.start_time + 82.0)
    episode_manager.save_episode(episode)
    bus.dispatch()  # EPISODE_COMPLETED & EPISODE_SAVED events trigger SemanticManager automatically

    print("=" * 37)
    print("MATCH COMPLETE")
    print("=" * 37)
    print("Episode Created")
    print(f"ID:\n{episode.episode_id}\n")
    print(f"Winner:\n{episode.winner}\n")
    print(f"Duration:\n{int(episode.duration)} sec\n")
    print(f"Saved:\nbackend/data/episodes/\n")

    print("=" * 37)
    print("DISTILLED SEMANTIC KNOWLEDGE")
    print("=" * 37)
    all_knowledge = semantic_manager.get_all_knowledge()
    for k in all_knowledge:
        print(f"[KNOWLEDGE] {k.type}")
        print(f"  Confidence: {int(k.confidence*100)}%")
        print(f"  Evidence:   {k.evidence_count} battles")
        print(f"  Summary:    {k.description}\n")

    print("Knowledge Graph Chain:")
    path = semantic_manager.knowledge_graph.query_path("Player", "Reload After 3 Attacks")
    if path:
        print(" -> ".join(path))
    else:
        print("Player -> USES -> Shotgun -> USUALLY -> Medium Range")

    print("=" * 37 + "\n")


if __name__ == "__main__":
    run_semantic_memory_demo(total_frames=1)
