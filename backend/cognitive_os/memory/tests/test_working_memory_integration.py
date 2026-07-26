"""Integration tests for Working Memory pipeline cascade:

Telemetry -> Perception -> Attention -> MemoryManager (Working Memory) -> WorldModel
"""

import pytest
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event
from backend.cognitive_os.telemetry.collector import TelemetryCollector
from backend.cognitive_os.perception.perception_engine import PerceptionEngine
from backend.cognitive_os.attention.attention_engine import AttentionEngine
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.context.world_model import WorldModelEngine


def test_working_memory_pipeline_cascade():
    bus = EventBus()

    collector = TelemetryCollector(event_bus=bus)
    perception = PerceptionEngine(event_bus=bus)
    attention = AttentionEngine(event_bus=bus)
    memory_manager = MemoryManager(event_bus=bus)
    world_model = WorldModelEngine(event_bus=bus)

    received_wm_updates = []

    def on_wm_update(event: Event):
        received_wm_updates.append(event.payload)

    bus.subscribe("WORKING_MEMORY_UPDATED", on_wm_update)

    # Trigger synthetic 60 Hz frame telemetry
    collector.generate_fake_frame(current_time=1.0)
    bus.dispatch()  # Telemetry -> Perception -> Attention -> MemoryManager -> WorldModel

    # Verify that Perception observations automatically became Working Memory items
    assert len(received_wm_updates) > 0
    active_memories = memory_manager.retrieve_recent(time_window_seconds=5.0, current_time=1.0)
    assert len(active_memories) > 0

    # Verify top priority memory item
    top_memories = memory_manager.retrieve_highest_priority(top_k=1)
    assert len(top_memories) == 1
    assert top_memories[0].importance > 0.0
