"""ModelRegistry module for ML Infrastructure.

Registers and hot-swaps active ML models per task:
- intent_prediction -> BaselinePredictor
- (Later) intent_prediction -> XGBoostPredictor / LSTMPredictor

Allows Cognitive OS to switch models dynamically without changing any surrounding code.
"""

from typing import Dict, Any, Optional
from backend.cognitive_os.ml.model import BaseMLModel


class ModelRegistry:
    _instance: Optional["ModelRegistry"] = None

    def __init__(self) -> None:
        self._models: Dict[str, BaseMLModel] = {}

    @classmethod
    def get_registry(cls) -> "ModelRegistry":
        """Singleton pattern for global model registry access."""
        if cls._instance is None:
            cls._instance = ModelRegistry()
        return cls._instance

    def register_model(self, task_name: str, model: BaseMLModel) -> None:
        """Registers an active ML model for a specific cognitive task."""
        self._models[task_name] = model

    def get_model(self, task_name: str) -> Optional[BaseMLModel]:
        """Retrieves the active registered ML model for a cognitive task."""
        return self._models.get(task_name)

    def hot_swap_model(self, task_name: str, new_model: BaseMLModel) -> str:
        """Hot-swaps the active model for a cognitive task without restarting Cognitive OS."""
        old_model = self._models.get(task_name)
        old_name = old_model.metadata().get("name", "Unknown") if old_model else "None"
        new_name = new_model.metadata().get("name", "Unknown")

        self._models[task_name] = new_model
        return f"Hot-swapped '{task_name}': {old_name} -> {new_name} ({new_model.version()})"

    def list_models(self) -> Dict[str, str]:
        """Lists all registered tasks and their active model versions."""
        return {
            task: f"{model.metadata().get('name', 'Model')} ({model.version()})"
            for task, model in self._models.items()
        }
