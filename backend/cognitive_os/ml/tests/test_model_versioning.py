"""Unit tests for ModelSaver and ModelLoader semantic versioning."""

import pytest
import os
import shutil
from typing import Dict, Any, List
from backend.cognitive_os.ml.model import BaseMLModel
from backend.cognitive_os.ml.model_saver import ModelSaver
from backend.cognitive_os.ml.model_loader import ModelLoader
from backend.cognitive_os.prediction.prediction import Prediction


class DummyVersionedModel(BaseMLModel):
    def __init__(self, ver: str = "v1.0") -> None:
        self.ver = ver
    def train(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]: return {}
    def predict(self, features: Dict[str, Any]) -> Prediction: return Prediction(action="Reload", confidence=0.80, time_horizon=2.0, reason="Ver", source="Ver")
    def evaluate(self, test_dataset: List[Dict[str, Any]]) -> Dict[str, float]: return {"accuracy": 0.80}
    def save(self, filepath: str) -> str:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.ver)
        return filepath
    def load(self, filepath: str) -> bool:
        with open(filepath, "r", encoding="utf-8") as f:
            self.ver = f.read()
        return True
    def version(self) -> str: return self.ver
    def metadata(self) -> Dict[str, Any]: return {"name": "DummyVersionedModel"}


@pytest.fixture
def temp_models_dir(tmp_path):
    models_dir = str(tmp_path / "models")
    yield models_dir
    if os.path.exists(models_dir):
        shutil.rmtree(models_dir, ignore_errors=True)


def test_model_versioning_save_and_load_v1_v11_v12(temp_models_dir):
    saver = ModelSaver(models_dir=temp_models_dir)
    loader = ModelLoader(models_dir=temp_models_dir)

    # Save v1.0, v1.1, v1.2
    m10 = DummyVersionedModel("v1.0")
    m11 = DummyVersionedModel("v1.1")
    m12 = DummyVersionedModel("v1.2")

    saver.save_model_version(m10, task_name="intent_prediction", version_str="v1.0")
    saver.save_model_version(m11, task_name="intent_prediction", version_str="v1.1")
    saver.save_model_version(m12, task_name="intent_prediction", version_str="v1.2")

    versions = loader.list_available_versions("intent_prediction")
    assert versions == ["v1.0", "v1.1", "v1.2"]

    loaded_11 = loader.load_model_version("intent_prediction", "v1.1", DummyVersionedModel)
    assert loaded_11 is not None
    assert loaded_11.version() == "v1.1"
