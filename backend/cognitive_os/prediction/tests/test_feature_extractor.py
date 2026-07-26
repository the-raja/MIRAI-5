"""Unit tests for FeatureExtractor ML feature vector creation."""

import pytest
from backend.cognitive_os.prediction.feature_extractor import FeatureExtractor, FeatureVector
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.telemetry.telemetry_frame import TelemetryFrame, EntityStateData, Vector3Data


def test_feature_extractor_vector_creation():
    extractor = FeatureExtractor()

    frame = TelemetryFrame(
        timestamp=10.0,
        frame_id=402,
        players={"player_raja_01": EntityStateData(id="player_raja_01", health=85.0, stamina=90.0, weapon="Shotgun", current_action="RELOAD")},
        boss=EntityStateData(id="boss_mirai", health=75.0)
    )
    wm = WorldModel(timestamp=10.0, estimated_player_positions={"player_raja_01": Vector3Data(x=6.0, y=0.0, z=8.0)})

    vec = extractor.extract_features(
        telemetry_frame=frame,
        world_model=wm,
        recent_actions=["Attack", "Attack", "Attack", "Reload"]
    )

    assert vec.player_hp == 85.0
    assert vec.boss_hp == 75.0
    assert vec.weapon == "Shotgun"
    assert vec.distance == 10.0  # sqrt(6^2 + 8^2) = 10.0
    assert len(vec.last_5_actions) == 4
    assert vec.to_numpy_array().shape == (7,)
