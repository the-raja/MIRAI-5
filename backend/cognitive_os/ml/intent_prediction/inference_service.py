"""IntentInferenceService module.

Decouples Cognitive OS core from direct ML model calls:
World State -> Feature Extractor -> Inference Service -> Prediction Object

The Cognitive OS remains completely unaware of whether Baseline, XGBoost, or LSTM is executing underneath.
"""

from typing import List, Dict, Any, Optional
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.prediction.feature_extractor import FeatureExtractor
from backend.cognitive_os.ml.model_registry import ModelRegistry
from backend.cognitive_os.ml.intent_prediction.predictor import IntentPredictor
from backend.cognitive_os.telemetry.telemetry_frame import TelemetryFrame
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager


class IntentInferenceService:
    def __init__(self, registry: Optional[ModelRegistry] = None) -> None:
        self.feature_extractor = FeatureExtractor()
        self.registry = registry or ModelRegistry.get_registry()
        self.fallback_predictor = IntentPredictor()

    def predict_intent(
        self,
        telemetry_frame: Optional[TelemetryFrame] = None,
        world_model: Optional[WorldModel] = None,
        memory_manager: Optional[MemoryManager] = None,
        semantic_manager: Optional[SemanticManager] = None,
        recent_actions: Optional[List[str]] = None,
        current_time: float = 0.0
    ) -> Prediction:
        """Processes World State through Feature Extractor and active ModelRegistry model to return Prediction."""
        # 1. Feature Extraction (Canonical 17 features)
        vector = self.feature_extractor.extract_features(
            telemetry_frame=telemetry_frame,
            world_model=world_model,
            memory_manager=memory_manager,
            semantic_manager=semantic_manager,
            recent_actions=recent_actions
        )
        features_dict = vector.to_dict()
        features_dict["timestamp"] = current_time if current_time > 0.0 else (world_model.timestamp if world_model else 0.0)

        # 2. Query active model from ModelRegistry
        active_model = self.registry.get_model("intent_prediction")
        if active_model:
            return active_model.predict(features_dict)

        # 3. Fallback to IntentPredictor
        return self.fallback_predictor.predict(features_dict)
