"""Experiment data structure. Only data models, no logic."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class Experiment(BaseModel):
    experiment_id: int
    timestamp: float = Field(default_factory=time.time)
    model_name: str  # e.g. "BaselinePredictor", "XGBoostPredictor", "LSTMPredictor"
    dataset_version: str  # e.g. "v1.0.0", "v3.0.0"
    accuracy: float = 0.0  # Accuracy metric [0.0 - 1.0]
    precision: float = 0.0
    recall: float = 0.0
    training_time_seconds: float = 0.0
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
