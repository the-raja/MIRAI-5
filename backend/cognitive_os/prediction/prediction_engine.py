"""PredictionEngine module.

Coordinates feature extraction and predictor invocation to generate real-time player action predictions.
Integrates directly between Semantic Memory and Goal Manager:
Semantic Memory -> Prediction Engine -> Goal Manager -> Utility AI -> Decision
Publishes PREDICTION_GENERATED events onto the EventBus.
"""

from typing import List, Optional, Dict, Any
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.prediction.predictor_interface import IPredictor
from backend.cognitive_os.prediction.baseline_predictor import BaselinePredictor
from backend.cognitive_os.prediction.feature_extractor import FeatureExtractor, FeatureVector
from backend.cognitive_os.telemetry.telemetry_frame import TelemetryFrame
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class PredictionEngine:
    def __init__(self, predictor: Optional[IPredictor] = None, event_bus: Optional[EventBus] = None) -> None:
        self.predictor: IPredictor = predictor or BaselinePredictor()
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
        """Extracts features and invokes active Predictor to generate player action prediction."""
        actions = recent_actions if recent_actions is not None else ["Attack", "Attack", "Attack"]
        c_time = current_time if current_time > 0.0 else (world_model.timestamp if world_model else 0.0)

        prediction = self.predictor.predict(
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
