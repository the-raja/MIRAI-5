"""PredictionEngine module.

Coordinates feature extraction, Inference Service, and Predictors to generate real-time player action predictions.
Pipeline Integration:
Semantic Memory -> Inference Service -> XGBoost -> Prediction -> Goal Manager

The BaselinePredictor remains fully available as a fallback if ML inference is unavailable.
Publishes PREDICTION_GENERATED events onto the EventBus.
"""

from typing import List, Optional, Dict, Any
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.prediction.predictor_interface import IPredictor
from backend.cognitive_os.prediction.baseline_predictor import BaselinePredictor
from backend.cognitive_os.prediction.feature_extractor import FeatureExtractor
from backend.cognitive_os.ml.intent_prediction.inference_service import IntentInferenceService
from backend.cognitive_os.ml.model_registry import ModelRegistry
from backend.cognitive_os.telemetry.telemetry_frame import TelemetryFrame
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class PredictionEngine:
    def __init__(self, predictor: Optional[IPredictor] = None, event_bus: Optional[EventBus] = None) -> None:
        self.fallback_predictor: IPredictor = predictor or BaselinePredictor()
        self.inference_service = IntentInferenceService(registry=ModelRegistry.get_registry())
        self.feature_extractor = FeatureExtractor()
        self.event_bus = event_bus

        if self.event_bus:
            self.event_bus.subscribe("WORLD_MODEL_UPDATED", self._on_world_model_updated)

    def _on_world_model_updated(self, event: Event) -> None:
        if isinstance(event.payload, WorldModel):
            pass

    def generate_prediction(
        self,
        telemetry_frame: Optional[TelemetryFrame] = None,
        world_model: Optional[WorldModel] = None,
        memory_manager: Optional[MemoryManager] = None,
        semantic_manager: Optional[SemanticManager] = None,
        recent_actions: Optional[List[str]] = None,
        current_time: float = 0.0
    ) -> Prediction:
        """Executes IntentInferenceService (XGBoost) if registered, with graceful fallback to BaselinePredictor."""
        actions = recent_actions if recent_actions is not None else ["Attack", "Attack", "Attack"]
        c_time = current_time if current_time > 0.0 else (world_model.timestamp if world_model else 0.0)

        registered_model = ModelRegistry.get_registry().get_model("intent_prediction")

        if registered_model is not None:
            try:
                prediction = self.inference_service.predict_intent(
                    telemetry_frame=telemetry_frame,
                    world_model=world_model,
                    memory_manager=memory_manager,
                    semantic_manager=semantic_manager,
                    recent_actions=actions,
                    current_time=c_time
                )
            except Exception:
                prediction = self.fallback_predictor.predict(
                    recent_actions=actions,
                    memory_manager=memory_manager,
                    semantic_manager=semantic_manager,
                    current_time=c_time
                )
        else:
            prediction = self.fallback_predictor.predict(
                recent_actions=actions,
                memory_manager=memory_manager,
                semantic_manager=semantic_manager,
                current_time=c_time
            )

        if self.event_bus:
            event = Event(
                event_type="PREDICTION_GENERATED",
                timestamp=prediction.timestamp,
                source="PredictionEngine",
                payload=prediction
            )
            self.event_bus.publish(event)

        return prediction
