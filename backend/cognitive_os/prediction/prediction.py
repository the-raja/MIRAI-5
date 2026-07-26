"""Prediction data structure. Only data models, no logic."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class Prediction(BaseModel):
    prediction_id: str = Field(default_factory=lambda: f"pred_{int(time.time()*1000)}")
    timestamp: float = Field(default_factory=time.time)
    action: str  # e.g. "Reload", "Dodge", "Heal", "Attack", "Retreat", "Block"
    confidence: float = 0.74  # Confidence / probability [0.0 - 1.0]
    time_horizon: float = 2.0  # Time horizon window in seconds
    reason: str = ""
    source: str = "Baseline Predictor"  # e.g. "Semantic Memory", "Baseline Predictor", "XGBoost Model"
    metadata: Dict[str, Any] = Field(default_factory=dict)
