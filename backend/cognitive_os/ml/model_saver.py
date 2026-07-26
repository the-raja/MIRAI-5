"""ModelSaver module for ML Infrastructure.

Persists proper semantically-versioned model artifacts:
`backend/data/models/<task_name>/<version_str>.bin`
No single overwriting "latest.pkl"—maintains strict historical model version archives (v1.0 -> v1.1 -> v1.2).
"""

from typing import Dict, Any, Optional
import os
import json
from backend.cognitive_os.ml.model import BaseMLModel


class ModelSaver:
    def __init__(self, models_dir: str = r"backend/data/models") -> None:
        self.models_dir = models_dir
        os.makedirs(self.models_dir, exist_ok=True)

    def save_model_version(self, model: BaseMLModel, task_name: str, version_str: str = "v1.0") -> str:
        """Saves model weights and metadata to semantically versioned file path."""
        task_dir = os.path.join(self.models_dir, task_name)
        os.makedirs(task_dir, exist_ok=True)

        clean_ver = version_str if version_str.startswith("v") else f"v{version_str}"
        filepath = os.path.join(task_dir, f"{clean_ver}.bin")

        # Invoke model's custom save logic
        saved_path = model.save(filepath)

        # Save metadata sidecar
        meta_filepath = os.path.join(task_dir, f"{clean_ver}_metadata.json")
        meta = model.metadata()
        meta["version"] = clean_ver
        meta["task_name"] = task_name
        with open(meta_filepath, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return saved_path
