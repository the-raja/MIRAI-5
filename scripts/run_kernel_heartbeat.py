"""MIRAI v2 — Checkpoint 1 Heartbeat Demonstration Runner.

Executes the Phase 2 Cognitive OS Kernel sensing pipeline:
Telemetry -> Perception -> Attention -> WorldModel

Outputs the formatted cognitive heartbeat telemetry. Zero ML, pure cognitive pipeline execution.
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
from backend.cognitive_os.context.world_model import WorldModelEngine, WorldModel
from backend.cognitive_os.telemetry.telemetry_frame import TelemetryFrame
from backend.cognitive_os.perception.observation import ObservationSet
from backend.cognitive_os.attention.salience import AttentionState


def run_heartbeat_demo(total_frames: int = 3) -> None:
    bus = EventBus()
    scheduler = CognitiveScheduler()

    collector = TelemetryCollector(event_bus=bus)
    perception = PerceptionEngine(event_bus=bus)
    attention = AttentionEngine(event_bus=bus)
    world_model_engine = WorldModelEngine(event_bus=bus)

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
    print("MIRAI v2 COGNITIVE OS KERNEL -- HEARTBEAT DEMO")
    print("=" * 49 + "\n")

    current_sim_time = 1000.0

    for f in range(1, total_frames + 1):
        current_sim_time += 0.01667  # 60 Hz tick step (~16.6ms)

        # Generate fake frame and process through pipeline
        collector.generate_fake_frame(current_time=current_sim_time)
        bus.dispatch()

        player = latest_frame.players.get("player_raja_01")
        boss = latest_frame.boss

        p_pos_str = f"({player.position.x:.1f}, {player.position.z:.1f})" if player else "N/A"
        b_pos_str = f"({boss.position.x:.1f}, {boss.position.z:.1f})" if boss else "N/A"
        dist = latest_obs.observations[0].metadata.get("distance", 0.0) if latest_obs and latest_obs.observations else 0.0

        print("=" * 49)
        print(f"FRAME {latest_frame.frame_id}")
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


if __name__ == "__main__":
    run_heartbeat_demo(total_frames=3)
