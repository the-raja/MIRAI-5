"""BaseMLModel abstract interface module.

Defines the universal model interface for all ML/DL models in MIRAI:
- train()
- predict()
- evaluate()
- save()
- load()
- version()
- metadata()

Enables seamless plug-and-play model swapping across Baseline, XGBoost, LSTM, Random Forest, and Transformer architectures.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from backend.cognitive_os.prediction.prediction import Prediction


class BaseMLModel(ABC):
    @abstractmethod
    def train(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Trains the ML model on structured dataset rows."""
        pass

    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Prediction:
        """Generates real-time action prediction from input features."""
        pass

    @abstractmethod
    def evaluate(self, test_dataset: List[Dict[str, Any]]) -> Dict[str, float]:
        """Evaluates model performance metrics on test dataset."""
        pass

    @abstractmethod
    def save(self, filepath: str) -> str:
        """Saves model weights/state to disk."""
        pass

    @abstractmethod
    def load(self, filepath: str) -> bool:
        """Loads model weights/state from disk."""
        pass

    @abstractmethod
    def version(self) -> str:
        """Returns semantic version string of the model."""
        pass

    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        """Returns model metadata schema and hyperparameters."""
        pass
