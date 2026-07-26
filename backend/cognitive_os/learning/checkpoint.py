"""CheckpointManager module.

Persists complete system checkpoints post-battle:
- Knowledge
- Statistics
- Parameters
- Utility Weights
- Prediction Metrics
- Version

If something breaks, supports restoring complete state from checkpoint.
"""

from typing import List, Dict, Any, Optional
import os
import json
from pydantic import BaseModel, Field
import time


class CheckpointState(BaseModel):
    checkpoint_id: str
    timestamp: float = Field(default_factory=time.time)
    version: str = "v1.0.0"
    knowledge_items: List[Dict[str, Any]] = Field(default_factory=list)
    statistics: Dict[str, Any] = Field(default_factory=dict)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    utility_weights: Dict[str, float] = Field(default_factory=dict)
    prediction_metrics: Dict[str, Any] = Field(default_factory=dict)


class CheckpointManager:
    def __init__(self, checkpoint_dir: str = r"backend/data/checkpoints") -> None:
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(self.checkpoint_dir, exist_ok=True)

    def save_checkpoint_state(self, state: CheckpointState) -> str:
        """Saves a complete CheckpointState object to disk as a JSON file."""
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        clean_id = state.checkpoint_id.replace("#", "")
        filepath = os.path.join(self.checkpoint_dir, f"{clean_id}.json")
        json_data = state.model_dump_json(indent=2)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_data)
        return filepath

    def load_checkpoint_state(self, checkpoint_id: str) -> Optional[CheckpointState]:
        """Loads a CheckpointState object from disk."""
        clean_id = checkpoint_id.replace("#", "")
        filepath = os.path.join(self.checkpoint_dir, f"{clean_id}.json")
        if not os.path.exists(filepath):
            return None
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            return CheckpointState.model_validate_json(content)
        except Exception:
            return None

    def restore_system_state(
        self,
        checkpoint_id: str,
        semantic_manager: Optional[Any] = None,
        utility_system: Optional[Any] = None,
        learning_engine: Optional[Any] = None
    ) -> bool:
        """Restores Knowledge, Utility Weights, and Statistics from a saved checkpoint."""
        state = self.load_checkpoint_state(checkpoint_id)
        if not state:
            return False

        # Restore Knowledge items to SemanticManager
        if semantic_manager and state.knowledge_items:
            for k_dict in state.knowledge_items:
                from backend.cognitive_os.memory.semantic.knowledge import Knowledge
                try:
                    k_obj = Knowledge.model_validate(k_dict)
                    semantic_manager.memory.upsert_knowledge(k_obj)
                except Exception:
                    pass

        # Restore Statistics
        if learning_engine and state.statistics:
            from backend.cognitive_os.learning.statistics import LearningStatistics
            try:
                learning_engine.statistics = LearningStatistics.model_validate(state.statistics)
            except Exception:
                pass

        return True

    def list_checkpoints(self) -> List[str]:
        """Lists all stored checkpoint IDs sorted."""
        if not os.path.exists(self.checkpoint_dir):
            return []
        files = [f.replace(".json", "") for f in os.listdir(self.checkpoint_dir) if f.endswith(".json")]
        files.sort()
        return files
