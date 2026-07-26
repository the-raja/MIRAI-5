"""Unit tests for AttentionEngine."""

import pytest
from backend.cognitive_os.telemetry.collector import TelemetryCollector
from backend.cognitive_os.perception.perception_engine import PerceptionEngine
from backend.cognitive_os.attention.attention_engine import AttentionEngine
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


def test_attention_engine_priority_ranking():
    collector = TelemetryCollector()
    perception = PerceptionEngine()
    attention = AttentionEngine()

    frame = collector.generate_fake_frame(current_time=1.0)
    obs_set = perception.process_frame(frame)
    att_state = attention.process_observations(obs_set)

    assert att_state.timestamp == 1.0
    assert len(att_state.salient_events) > 0

    # Ensure events are sorted descending by saliency score
    scores = [e.saliency_score for e in att_state.salient_events]
    assert scores == sorted(scores, reverse=True)


def test_attention_engine_event_bus_pipeline():
    bus = EventBus()
    collector = TelemetryCollector(event_bus=bus)
    perception = PerceptionEngine(event_bus=bus)
    attention = AttentionEngine(event_bus=bus)

    received_attention = []

    def on_attention(event: Event):
        received_attention.append(event.payload)

    bus.subscribe("ATTENTION_STATE", on_attention)

    collector.generate_fake_frame(current_time=1.0)
    bus.dispatch()  # Telemetry -> Perception -> Attention -> AttentionState subscriber

    assert len(received_attention) == 1
    top_event = received_attention[0].salient_events[0]
    assert top_event.saliency_score > 0
