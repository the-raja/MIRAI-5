"""ReplayEngine module.

Records and replays simulation battle matches for post-hoc analysis.
"""

from typing import List, Dict, Any, Optional
import os
import json


class ReplayEngine:
    def __init__(self) -> None:
        self._match_logs: List[Dict[str, Any]] = []

    def record_step(self, step_data: Dict[str, Any]) -> None:
        """Records a single combat frame step into the replay buffer."""
        self._match_logs.append(step_data)

    def get_replay_log(self) -> List[Dict[str, Any]]:
        return self._match_logs

    def save_replay(self, filepath: str) -> None:
        """Persists replay log to JSON file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self._match_logs, f, indent=2)
