"""PredictorInterface abstract base class."""

from abc import ABC, abstractmethod
from typing import List, Optional
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager


class IPredictor(ABC):
    @abstractmethod
    def predict(
        self,
        recent_actions: List[str],
        memory_manager: Optional[MemoryManager] = None,
        semantic_manager: Optional[SemanticManager] = None,
        current_time: float = 0.0
    ) -> Prediction:
        """Predicts the next probable player action or event."""
        pass
