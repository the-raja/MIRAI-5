"""Unit tests for WorldModelEngine."""

import pytest
from backend.cognitive_os.telemetry.collector import TelemetryCollector
from backend.cognitive_os.context.world_model import WorldModelEngine
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


def test_world_model_telemetry_updates():
    collector = TelemetryCollector()
    wm_engine = WorldModelEngine()

    frame = collector.generate_fake_frame(current_time=1.0)
    wm = wm_engine.update_from_telemetry(frame)

    assert wm.timestamp == 1.0
    assert "player_raja_01" in wm.estimated_player_positions
    assert "player_raja_01" in wm.visible_entities
    assert len(wm.cover_nodes) == 3


def test_world_model_event_bus_pipeline():
    bus = EventBus()
    collector = TelemetryCollector(event_bus=bus)
    wm_engine = WorldModelEngine(event_bus=bus)

    updates = []

    def on_world_model(event: Event):
        updates.append(event.payload)

    bus.subscribe("WORLD_MODEL_UPDATED", on_world_model)

    collector.generate_fake_frame(current_time=1.0)
    bus.dispatch()

    assert len(updates) > 0
    assert "player_raja_01" in updates[0].estimated_player_positions
