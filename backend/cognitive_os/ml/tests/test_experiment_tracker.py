"""Unit tests for ExperimentTracker logging and leaderboard generation."""

import pytest
import os
import shutil
from backend.cognitive_os.ml.experiment_tracker import ExperimentTracker


@pytest.fixture
def temp_exp_dir(tmp_path):
    exp_dir = str(tmp_path / "experiments")
    yield exp_dir
    if os.path.exists(exp_dir):
        shutil.rmtree(exp_dir, ignore_errors=True)


def test_experiment_tracker_logging_and_comparison(temp_exp_dir):
    tracker = ExperimentTracker(storage_dir=temp_exp_dir)

    # Log Exp 21 (Baseline)
    exp21 = tracker.log_experiment(
        model_name="Baseline",
        dataset_version="v3",
        accuracy=0.74,
        precision=0.72,
        recall=0.71,
        training_time_seconds=0.03
    )

    card21 = tracker.format_ml_experiment_card(exp21)
    assert "Baseline" in card21
    assert "74%" in card21

    # Log Exp 35 (XGBoost)
    exp35 = tracker.log_experiment(
        model_name="XGBoost",
        dataset_version="v3",
        accuracy=0.91,
        precision=0.89,
        recall=0.88,
        training_time_seconds=0.45
    )

    leaderboard = tracker.format_leaderboard()
    assert "LEADERBOARD" in leaderboard
    assert "XGBoost" in leaderboard
    assert "91.0%" in leaderboard
