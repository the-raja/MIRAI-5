"""Prediction API module for Runtime."""

from typing import Dict, Any
from backend.cognitive_os.prediction.baseline_predictor import BaselinePredictor


class PredictionAPI:
    def __init__(self) -> None:
        self.predictor = BaselinePredictor()

    def predict_next_action(self, situation: Dict[str, Any]) -> str:
        return "RELOAD"
