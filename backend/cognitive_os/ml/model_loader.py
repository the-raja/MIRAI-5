"""ModelLoader module for ML Infrastructure.

Loads exact semantically versioned model artifacts:
`backend/data/models/<task_name>/<version_str>.bin`
Supports loading historical model versions (v1.0, v1.1, v1.2) for fallback or comparison.
"""

from typing import Dict, Any, Optional, Type
import os
import json
from backend.cognitive_os.ml.model import BaseMLModel


class ModelLoader:
    def __init__(self, models_dir: str = r"backend/data/models") -> None:
        self.models_dir = models_dir

    def load_model_version(self, task_name: str, version_str: str, model_class: Type[BaseMLModel]) -> Optional[BaseMLModel]:
        """Instantiates and loads an exact semantic version of an ML model from disk."""
        task_dir = os.path.join(self.models_dir, task_name)
        clean_ver = version_str if version_str.startswith("v") else f"v{version_str}"
        filepath = os.path.join(task_dir, f"{clean_ver}.bin")

        if not os.path.exists(filepath):
            return None

        try:
            model = model_class()
            model.load(filepath)
            return model
        except Exception:
            return None

    def list_available_versions(self, task_name: str) -> list[str]:
        """Lists all stored version strings for a given task."""
        task_dir = os.path.join(self.models_dir, task_name)
        if not os.path.exists(task_dir):
            return []
        files = [f.replace(".bin", "") for f in os.listdir(task_dir) if f.endswith(".bin")]
        files.sort()
        return files
