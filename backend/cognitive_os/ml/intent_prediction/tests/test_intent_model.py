"""Unit tests for IntentPredictionModel and IntentTrainer XGBoost model training."""

import pytest
import os
import shutil
from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel
from backend.cognitive_os.ml.intent_prediction.trainer import IntentTrainer


@pytest.fixture
def temp_trainer_dir(tmp_path):
    root_dir = str(tmp_path / "intent_datasets")
    yield root_dir
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir, ignore_errors=True)


def test_intent_prediction_model_interface_and_inference():
    model = IntentPredictionModel()

    sample_features = {
        "distance": 2.5,
        "player_hp": 80.0,
        "boss_hp": 70.0,
        "stamina": 90.0,
        "weapon": "Shotgun",
        "current_action": "RELOAD",
        "last_action": "ATTACK",
        "last_5_action_histogram": "ATTACK:3",
        "aggression_score": 0.85,
        "reload_frequency": 12,
        "preferred_dodge": "Left",
        "preferred_weapon": "Shotgun",
        "time_since_reload": 1.2,
        "time_since_heal": 40.0,
        "time_since_damage": 5.0,
        "boss_cooldown": 2.0,
        "player_cooldown": 0.0
    }

    pred = model.predict(sample_features)

    assert pred.action in ["Reload", "RELOAD"]
    assert pred.confidence >= 0.90
    assert "top_contributing_features" in pred.metadata
    assert pred.source == "XGBoost Intent Model"


def test_intent_trainer_end_to_end_training(temp_trainer_dir):
    trainer = IntentTrainer(dataset_root=temp_trainer_dir)
    model, exp = trainer.train_and_register(dataset_version="v1")

    assert model.is_trained is True
    assert exp.model_name == "XGBoost Intent Model"
    assert exp.dataset_version == "v1"
    assert exp.accuracy >= 0.80
    assert exp.metadata["status"] == "PASS"
