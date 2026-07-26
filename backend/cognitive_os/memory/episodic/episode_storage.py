"""EpisodeStorage module.

Persists finished Episode objects to disk as JSON files inside `backend/data/episodes/`.
No database, no FAISS, no embeddings—pure JSON serialization and disk storage.
"""

from typing import List, Optional
import os
import json
from backend.cognitive_os.memory.episodic.episode import Episode


class EpisodeStorage:
    def __init__(self, storage_dir: str = r"backend/data/episodes") -> None:
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def _get_episode_filepath(self, episode_id: str) -> str:
        # Sanitize episode_id filename
        clean_id = episode_id.replace(" ", "_").replace("#", "")
        return os.path.join(self.storage_dir, f"{clean_id}.json")

    def save_episode(self, episode: Episode) -> str:
        """Serializes and saves an Episode object as a JSON file."""
        filepath = self._get_episode_filepath(episode.episode_id)
        json_data = episode.model_dump_json(indent=2)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_data)
        return filepath

    def load_episode(self, episode_id: str) -> Optional[Episode]:
        """Loads and deserializes an Episode object from its JSON file."""
        filepath = self._get_episode_filepath(episode_id)
        if not os.path.exists(filepath):
            return None
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            return Episode.model_validate_json(content)
        except Exception:
            return None

    def list_episodes(self) -> List[str]:
        """Returns a list of all stored episode IDs sorted by filename."""
        if not os.path.exists(self.storage_dir):
            return []
        files = [f for f in os.listdir(self.storage_dir) if f.endswith(".json")]
        files.sort()
        return [f.replace(".json", "") for f in files]

    def get_total_episode_count(self) -> int:
        """Returns total stored episode count."""
        return len(self.list_episodes())
