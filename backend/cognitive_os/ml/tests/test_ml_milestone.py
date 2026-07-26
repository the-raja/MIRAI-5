"""Phase 9 ML Infrastructure Milestone Unit Tests.

Explicitly verifies the 7 core ML Infrastructure contracts:
1. Registry
2. Dataset Manager
3. Experiment Tracking
4. Model Loading
5. Model Saving
6. Metrics Engine
7. Model Versioning
"""

import pytest
import os
import shutil
from typing import Dict, Any, List
from backend.cognitive_os.ml.model import BaseMLModel
from backend.cognitive_os.ml.model_registry import ModelRegistry
from backend.cognitive_os.ml.dataset import DatasetManager
from backend.cognitive_os.ml.experiment_tracker import ExperimentTracker
from backend.cognitive_os.ml.model_saver import ModelSaver
from backend.cognitive_os.ml.model_loader import ModelLoader
from backend.cognitive_os.ml.metrics import MetricsEngine
from backend.cognitive_os.prediction.prediction import Prediction


class BaselineTestModel(BaseMLModel):
    def __init__(self, ver: str = "v1.0") -> None:
        self.ver = ver
    def train(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]: return {"epochs": 1}
    def predict(self, features: Dict[str, Any]) -> Prediction: return Prediction(action="Reload", confidence=0.74, time_horizon=2.0, reason="Base", source="Baseline")
    def evaluate(self, test_dataset: List[Dict[str, Any]]) -> Dict[str, float]: return {"accuracy": 0.74}
    def save(self, filepath: str) -> str:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.ver)
        return filepath
    def load(self, filepath: str) -> bool:
        with open(filepath, "r", encoding="utf-8") as f:
            self.ver = f.read()
        return True
    def version(self) -> str: return self.ver
    def metadata(self) -> Dict[str, Any]: return {"name": "Baseline Predictor"}


@pytest.fixture
def temp_ml_dirs(tmp_path):
    m_dir = str(tmp_path / "models")
    e_dir = str(tmp_path / "experiments")
    d_dir = str(tmp_path / "datasets")
    yield m_dir, e_dir, d_dir
    for p in (m_dir, e_dir, d_dir):
        if os.path.exists(p):
            shutil.rmtree(p, ignore_errors=True)


def test_1_model_registry():
    """Case 1: Model Registry registration and lookup."""
    reg = ModelRegistry()
    m = BaselineTestModel()
    reg.register_model("intent_prediction", m)
    found = reg.get_model("intent_prediction")
    assert found is not None
    assert found.metadata()["name"] == "Baseline Predictor"


def test_2_dataset_manager():
    """Case 2: Dataset Manager train/val/test splitting."""
    mgr = DatasetManager()
    rows = [{"distance": float(i), "target_next_action": "Reload"} for i in range(100)]
    split = mgr.create_split(rows, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1)
    assert len(split.train_data) == 80
    assert len(split.val_data) == 10
    assert len(split.test_data) == 10


def test_3_experiment_tracking(temp_ml_dirs):
    """Case 3: Experiment Tracking logging and card formatting."""
    _, e_dir, _ = temp_ml_dirs
    tracker = ExperimentTracker(storage_dir=e_dir)
    exp = tracker.log_experiment(
        model_name="Baseline Predictor",
        dataset_version="v5",
        accuracy=0.74,
        precision=0.71,
        recall=0.72,
        training_time_seconds=0.03
    )
    card = tracker.format_ml_experiment_card(exp)
    assert "Baseline Predictor" in card
    assert "Dataset\nv5" in card
    assert "74%" in card
    assert "PASS" in card


def test_4_and_5_model_saving_and_loading(temp_ml_dirs):
    """Cases 4 & 5: Model Saving and Model Loading."""
    m_dir, _, _ = temp_ml_dirs
    saver = ModelSaver(models_dir=m_dir)
    loader = ModelLoader(models_dir=m_dir)

    model = BaselineTestModel("v1.0")
    saved_path = saver.save_model_version(model, task_name="intent_prediction", version_str="v1.0")
    assert os.path.exists(saved_path)

    loaded = loader.load_model_version("intent_prediction", "v1.0", BaselineTestModel)
    assert loaded is not None
    assert loaded.version() == "v1.0"


def test_6_metrics_engine():
    """Case 6: Metrics Engine computation."""
    metrics = MetricsEngine.compute_all_metrics(
        predictions=["Reload", "Dodge"],
        actuals=["Reload", "Dodge"],
        inference_times_ms=[0.3, 0.3],
        training_time_seconds=0.03,
        model_size_bytes=1024
    )
    assert metrics.accuracy == 1.0
    assert metrics.inference_time_ms == 0.3


def test_7_versioning(temp_ml_dirs):
    """Case 7: Semantic Versioning (v1.0 -> v1.1 -> v1.2)."""
    m_dir, _, _ = temp_ml_dirs
    saver = ModelSaver(models_dir=m_dir)
    loader = ModelLoader(models_dir=m_dir)

    for v in ["v1.0", "v1.1", "v1.2"]:
        m = BaselineTestModel(v)
        saver.save_model_version(m, task_name="intent_prediction", version_str=v)

    versions = loader.list_available_versions("intent_prediction")
    assert versions == ["v1.0", "v1.1", "v1.2"]
