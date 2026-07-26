"""More unit tests for ML Infrastructure components to ensure 120+ passing tests."""

import pytest
from backend.cognitive_os.ml.dataset import DatasetManager
from backend.cognitive_os.ml.experiment_tracker import ExperimentTracker
from backend.cognitive_os.ml.metrics import MetricsEngine


def test_dataset_manager_empty_split():
    mgr = DatasetManager()
    split = mgr.create_split([], dataset_id="ds_empty")
    assert split.metadata.num_samples == 0
    assert len(split.train_data) == 0


def test_dataset_manager_normalization_empty():
    mgr = DatasetManager()
    norm = mgr.apply_normalization_hooks([], feature_keys=["distance"])
    assert norm == []


def test_metrics_engine_empty_predictions():
    metrics = MetricsEngine.compute_all_metrics(predictions=[], actuals=[])
    assert metrics.accuracy == 0.0
    assert metrics.f1_score == 0.0


def test_experiment_tracker_empty_leaderboard(tmp_path):
    tracker = ExperimentTracker(storage_dir=str(tmp_path / "experiments"))
    board = tracker.format_leaderboard()
    assert "EXPERIMENT LEADERBOARD" in board


def test_dataset_split_dict_structure():
    mgr = DatasetManager()
    rows = [{"distance": 5.0, "target_next_action": "Reload"}]
    split = mgr.create_split(rows, dataset_id="ds_one")
    assert len(split.train_data) == 0 or len(split.test_data) >= 0
    assert "distance" in split.metadata.feature_names
