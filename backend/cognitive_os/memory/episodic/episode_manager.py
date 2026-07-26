"""EpisodeManager module.

High-level manager for creating, persisting, loading, deleting, listing, and searching historical battle episodes.
Contains NO ML—pure episodic memory management.
"""

from typing import List, Optional, Dict, Any
import os
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.episode_builder import EpisodeBuilder
from backend.cognitive_os.memory.episodic.episode_storage import EpisodeStorage
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class EpisodeManager:
    def __init__(self, storage_dir: str = r"backend/data/episodes", event_bus: Optional[EventBus] = None) -> None:
        self.storage = EpisodeStorage(storage_dir=storage_dir)
        self.event_bus = event_bus

        if self.event_bus:
            self.event_bus.subscribe("EPISODE_COMPLETED", self._on_episode_completed)

    def _on_episode_completed(self, event: Event) -> None:
        if isinstance(event.payload, Episode):
            self.save_episode(event.payload)

    def create_builder(self, match_id: str) -> EpisodeBuilder:
        """Create a new EpisodeBuilder (Historian) instance for an active battle match."""
        return EpisodeBuilder(match_id=match_id, event_bus=self.event_bus)

    def save_episode(self, episode: Episode) -> str:
        """Persist an episode to disk storage."""
        path = self.storage.save_episode(episode)
        if self.event_bus:
            event = Event(
                event_type="EPISODE_SAVED",
                timestamp=episode.timestamp,
                source="EpisodeManager",
                payload={"episode_id": episode.episode_id, "filepath": path}
            )
            self.event_bus.publish(event)
        return path

    def load_episode(self, episode_id: str) -> Optional[Episode]:
        """Load an episode by ID."""
        return self.storage.load_episode(episode_id)

    def delete_episode(self, episode_id: str) -> bool:
        """Delete an episode file by ID."""
        filepath = self.storage._get_episode_filepath(episode_id)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except OSError:
                return False
        return False

    def list_episodes(self) -> List[str]:
        """Return list of all stored episode IDs."""
        return self.storage.list_episodes()

    def search_by_id(self, query_id: str) -> List[Episode]:
        """Search and load episodes whose IDs contain query_id."""
        matching_episodes: List[Episode] = []
        for ep_id in self.list_episodes():
            if query_id.lower() in ep_id.lower():
                loaded = self.load_episode(ep_id)
                if loaded:
                    matching_episodes.append(loaded)
        return matching_episodes

    def get_total_count(self) -> int:
        """Return total stored episode count."""
        return self.storage.get_total_episode_count()
