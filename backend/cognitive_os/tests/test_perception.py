"""Unit tests for PerceptionEngine."""

import pytest
from backend.cognitive_os.telemetry.collector import TelemetryCollector
from backend.cognitive_os.perception.perception_engine import PerceptionEngine
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


def test_perception_engine_observation_extraction():
    collector = TelemetryCollector()
    perception = PerceptionEngine()

    frame = collector.generate_fake_frame(current_time=1.0)
    obs_set = perception.process_frame(frame)

    assert obs_set.frame_id == 1
    assert "PlayerVisible" in obs_set.flags
    assert "PlayerRunning" in obs_set.flags
    assert "ProjectileIncoming" in obs_set.flags
    assert len(obs_set.observations) > 0


def test_perception_engine_event_bus_pipeline():
    bus = EventBus()
    collector = TelemetryCollector(event_bus=bus)
    perception = PerceptionEngine(event_bus=bus)

    received_obs = []

    def on_observation(event: Event):
        received_obs.append(event.payload)

    bus.subscribe("OBSERVATION_SET", on_observation)

    collector.generate_fake_frame(current_time=1.0)
    bus.dispatch()  # TelemetryCollector publishes -> PerceptionEngine receives & publishes -> Observation subscriber receives

    assert len(received_obs) == 1
    assert received_obs[0].flags["PlayerVisible"] is True
