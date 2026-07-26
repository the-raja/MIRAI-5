"""Unit tests for BaseMLModel universal interface."""

import pytest
from typing import Dict, Any, List
from backend.cognitive_os.ml.model import BaseMLModel
from backend.cognitive_os.prediction.prediction import Prediction


class DummyModel(BaseMLModel):
    def train(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"loss": 0.01, "epochs": 10}

    def predict(self, features: Dict[str, Any]) -> Prediction:
        return Prediction(action="Reload", confidence=0.85, time_horizon=2.0, reason="Dummy", source="DummyModel")

    def evaluate(self, test_dataset: List[Dict[str, Any]]) -> Dict[str, float]:
        return {"accuracy": 0.85, "precision": 0.80}

    def save(self, filepath: str) -> str:
        return filepath

    def load(self, filepath: str) -> bool:
        return True

    def version(self) -> str:
        return "v1.0.0"

    def metadata(self) -> Dict[str, Any]:
        return {"name": "DummyModel", "type": "Dummy"}


def test_base_ml_model_interface_contract():
    model = DummyModel()

    assert model.version() == "v1.0.0"
    assert model.metadata()["name"] == "DummyModel"

    train_res = model.train([])
    assert train_res["loss"] == 0.01

    pred = model.predict({})
    assert pred.action == "Reload"
    assert pred.confidence == 0.85

    eval_res = model.evaluate([])
    assert eval_res["accuracy"] == 0.85

    assert model.save("test.bin") == "test.bin"
    assert model.load("test.bin") is True
