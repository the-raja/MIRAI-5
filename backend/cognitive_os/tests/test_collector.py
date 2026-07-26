"""Unit tests for TelemetryCollector."""

import pytest
from backend.cognitive_os.telemetry.collector import TelemetryCollector
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


def test_telemetry_collector_fake_frame_generation():
    collector = TelemetryCollector()
    frame = collector.generate_fake_frame(current_time=1.0)

    assert frame.frame_id == 1
    assert "player_raja_01" in frame.players
    assert frame.boss is not None
    assert frame.boss.id == "boss_mirai"
    assert frame.timestamp == 1.0


def test_telemetry_collector_event_bus_integration():
    bus = EventBus()
    collector = TelemetryCollector(event_bus=bus)
    received = []

    def on_telemetry(event: Event):
        received.append(event.payload)

    bus.subscribe("TELEMETRY_FRAME", on_telemetry)

    collector.generate_fake_frame(current_time=1.0)
    bus.dispatch()

    assert len(received) == 1
    assert received[0].frame_id == 1
    assert received[0].players["player_raja_01"].health == 85.0
