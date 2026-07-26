"""ModelVersionManager module.

Manages semantic model versioning for Predictors, Utility Scoring, and Semantic Memory weights:
Model v1 -> Model v2 -> Model v3...
Establishes model lineage tracking for future XGBoost, LightGBM, and PyTorch LSTM models.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class ModelVersion(BaseModel):
    version_id: str  # e.g. "v1.0.0", "v1.0.1", "v2.0.0"
    version_number: int = 1
    timestamp: float = Field(default_factory=time.time)
    change_description: str = ""
    active_components: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ModelVersionManager:
    def __init__(self) -> None:
        self.major: int = 1
        self.minor: int = 0
        self.patch: int = 0
        self.version_history: List[ModelVersion] = []

        # Initialize initial v1.0.0 version
        init_ver = self._create_version_object("Initial system baseline version v1.0.0")
        self.version_history.append(init_ver)

    def _create_version_object(self, description: str) -> ModelVersion:
        version_id = f"v{self.major}.{self.minor}.{self.patch}"
        v_num = self.major * 1000 + self.minor * 100 + self.patch
        return ModelVersion(
            version_id=version_id,
            version_number=v_num,
            change_description=description,
            active_components={
                "prediction_model": f"baseline_predictor_{version_id}",
                "utility_system": f"utility_cortex_v0.5.0",
                "semantic_memory": f"semantic_store_v0.4.0"
            }
        )

    def create_next_version(self, description: str = "Post-match continuous learning adaptation") -> ModelVersion:
        """Increments patch version and appends to version lineage history (Model v1 -> Model v2 -> Model v3)."""
        self.patch += 1
        new_ver = self._create_version_object(description)
        self.version_history.append(new_ver)
        return new_ver

    def bump_minor(self, description: str = "New feature model architecture release") -> ModelVersion:
        """Increments minor version."""
        self.minor += 1
        self.patch = 0
        new_ver = self._create_version_object(description)
        self.version_history.append(new_ver)
        return new_ver

    def get_current_version(self) -> ModelVersion:
        """Returns the latest active ModelVersion."""
        return self.version_history[-1]

    def get_version_dict(self) -> Dict[str, str]:
        """Returns dictionary of active component versions."""
        curr = self.get_current_version()
        res = dict(curr.active_components)
        res["active_model_version"] = curr.version_id
        return res

    def get_version_history(self) -> List[ModelVersion]:
        """Returns full lineage history of model versions."""
        return list(self.version_history)
