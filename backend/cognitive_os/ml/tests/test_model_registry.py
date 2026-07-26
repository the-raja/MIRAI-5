"""Unit tests for ModelRegistry hot-swapping functionality."""

import pytest
from backend.cognitive_os.ml.model import BaseMLModel
from backend.cognitive_os.ml.model_registry import ModelRegistry
from backend.cognitive_os.prediction.prediction import Prediction
from typing import Dict, Any, List


class BaselineMock(BaseMLModel):
    def train(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]: return {}
    def predict(self, features: Dict[str, Any]) -> Prediction: return Prediction(action="Reload", confidence=0.74, time_horizon=2.0, reason="Base", source="Baseline")
    def evaluate(self, test_dataset: List[Dict[str, Any]]) -> Dict[str, float]: return {"accuracy": 0.74}
    def save(self, filepath: str) -> str: return filepath
    def load(self, filepath: str) -> bool: return True
    def version(self) -> str: return "v1.0.0"
    def metadata(self) -> Dict[str, Any]: return {"name": "BaselinePredictor"}


class XGBoostMock(BaseMLModel):
    def train(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]: return {}
    def predict(self, features: Dict[str, Any]) -> Prediction: return Prediction(action="Reload", confidence=0.92, time_horizon=2.0, reason="Trees", source="XGBoost")
    def evaluate(self, test_dataset: List[Dict[str, Any]]) -> Dict[str, float]: return {"accuracy": 0.92}
    def save(self, filepath: str) -> str: return filepath
    def load(self, filepath: str) -> bool: return True
    def version(self) -> str: return "v2.0.0"
    def metadata(self) -> Dict[str, Any]: return {"name": "XGBoostPredictor"}


def test_model_registry_registration_and_hot_swap():
    registry = ModelRegistry()

    # 1. Register Baseline
    baseline = BaselineMock()
    registry.register_model("intent_prediction", baseline)

    active = registry.get_model("intent_prediction")
    assert active.metadata()["name"] == "BaselinePredictor"
    assert active.predict({}).confidence == 0.74

    # 2. Hot-swap to XGBoost
    xgboost = XGBoostMock()
    msg = registry.hot_swap_model("intent_prediction", xgboost)

    assert "BaselinePredictor -> XGBoostPredictor" in msg
    new_active = registry.get_model("intent_prediction")
    assert new_active.metadata()["name"] == "XGBoostPredictor"
    assert new_active.predict({}).confidence == 0.92
