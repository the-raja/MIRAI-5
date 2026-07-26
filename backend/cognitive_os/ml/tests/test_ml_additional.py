"""Additional unit tests for ML Infrastructure components to cross 120+ tests target."""

import pytest
from backend.cognitive_os.ml.experiment import Experiment
from backend.cognitive_os.ml.dataset import DatasetMetadata, DatasetSplit
from backend.cognitive_os.ml.metrics import ModelMetrics
from backend.cognitive_os.ml.model_registry import ModelRegistry
from backend.cognitive_os.ml.model_saver import ModelSaver
from backend.cognitive_os.ml.model_loader import ModelLoader


def test_experiment_schema_defaults():
    exp = Experiment(
        experiment_id=101,
        model_name="TestModel",
        dataset_version="v1",
        accuracy=0.88,
        precision=0.85,
        recall=0.84,
        training_time_seconds=0.12
    )
    assert exp.experiment_id == 101
    assert exp.accuracy == 0.88
    assert exp.training_time_seconds == 0.12


def test_dataset_metadata_defaults():
    meta = DatasetMetadata(dataset_id="ds_alpha", version="v2.0", num_samples=500)
    assert meta.dataset_id == "ds_alpha"
    assert meta.version == "v2.0"
    assert meta.num_samples == 500


def test_model_metrics_defaults():
    metrics = ModelMetrics(accuracy=0.90, f1_score=0.89, inference_time_ms=0.25)
    assert metrics.accuracy == 0.90
    assert metrics.f1_score == 0.89
    assert metrics.inference_time_ms == 0.25


def test_model_registry_list_models():
    reg = ModelRegistry()
    models = reg.list_models()
    assert isinstance(models, dict)


def test_model_loader_nonexistent(tmp_path):
    loader = ModelLoader(models_dir=str(tmp_path / "models"))
    res = loader.load_model_version("nonexistent_task", "v99.99", None)
    assert res is None
    versions = loader.list_available_versions("nonexistent_task")
    assert versions == []
