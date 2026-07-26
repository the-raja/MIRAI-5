"""Unit tests for EventBus functionality."""

import pytest
from backend.cognitive_os.event_bus.events import Event
from backend.cognitive_os.event_bus.event_bus import EventBus


def test_event_bus_publish_and_dispatch():
    bus = EventBus()
    received_events = []

    def sample_callback(event: Event):
        received_events.append(event)

    bus.subscribe("TELEMETRY_FRAME", sample_callback)

    event = Event(event_type="TELEMETRY_FRAME", source="TEST", payload={"frame_id": 100})
    bus.publish(event)

    assert len(received_events) == 0  # Not dispatched yet
    count = bus.dispatch()
    assert count == 1
    assert len(received_events) == 1
    assert received_events[0].payload["frame_id"] == 100


def test_event_bus_unsubscribe():
    bus = EventBus()
    received_events = []

    def sample_callback(event: Event):
        received_events.append(event)

    bus.subscribe("TELEMETRY_FRAME", sample_callback)
    bus.unsubscribe("TELEMETRY_FRAME", sample_callback)

    bus.publish(Event(event_type="TELEMETRY_FRAME", source="TEST"))
    bus.dispatch()

    assert len(received_events) == 0
