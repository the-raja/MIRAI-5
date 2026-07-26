"""End-to-End integration test for Phase 2 Cognitive OS Kernel sub-pipeline:

Telemetry -> Perception -> Attention -> WorldModel

Verifies that the entire sensing pipeline flows seamlessly through the EventBus
and handles module fault-tolerance without crashing the kernel.
"""

import pytest
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event
from backend.cognitive_os.scheduler.scheduler import CognitiveScheduler
from backend.cognitive_os.telemetry.collector import TelemetryCollector
from backend.cognitive_os.perception.perception_engine import PerceptionEngine
from backend.cognitive_os.attention.attention_engine import AttentionEngine
from backend.cognitive_os.context.world_model import WorldModelEngine


def test_full_sensing_pipeline_integration():
    bus = EventBus()
    scheduler = CognitiveScheduler()

    collector = TelemetryCollector(event_bus=bus)
    perception = PerceptionEngine(event_bus=bus)
    attention = AttentionEngine(event_bus=bus)
    world_model = WorldModelEngine(event_bus=bus)

    pipeline_log = []

    def log_world_model(event: Event):
        pipeline_log.append(event.payload)

    bus.subscribe("WORLD_MODEL_UPDATED", log_world_model)

    # Register multi-rate tasks with scheduler
    scheduler.register_task("telemetry", 60.0, lambda: collector.generate_fake_frame(current_time=1.0))

    # Tick scheduler at t=1.0 and dispatch events across the pipeline
    scheduler.tick(1.0)
    bus.dispatch()  # Telemetry -> Perception -> Attention -> WorldModel pipeline cascade

    # Verify complete data flow: Telemetry -> Perception -> Attention -> WorldModel
    assert len(pipeline_log) > 0
    final_wm = pipeline_log[-1]
    assert "player_raja_01" in final_wm.estimated_player_positions
    assert len(final_wm.visible_entities) == 1
    assert final_wm.timestamp == 1.0


def test_sensing_pipeline_resilience_on_module_failure():
    """Verifies that if a subscriber/module fails, other modules continue processing."""
    bus = EventBus()

    collector = TelemetryCollector(event_bus=bus)
    perception = PerceptionEngine(event_bus=bus)  # Automatically subscribes to TELEMETRY_FRAME

    # Broken subscriber that raises an Exception
    def broken_subscriber(event: Event):
        raise RuntimeError("Simulated module crash!")

    received_observations = []

    def healthy_subscriber(event: Event):
        received_observations.append(event.payload)

    bus.subscribe("TELEMETRY_FRAME", broken_subscriber)
    bus.subscribe("OBSERVATION_SET", healthy_subscriber)

    collector.generate_fake_frame(current_time=1.0)
    bus.dispatch()  # Built-in fault-tolerant dispatch

    assert len(received_observations) == 1
    assert received_observations[0].flags["PlayerVisible"] is True
