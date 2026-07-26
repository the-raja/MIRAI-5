"""Unit tests for EpisodeManager CRUD and search operations."""

import pytest
import os
import shutil
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.episode_manager import EpisodeManager


@pytest.fixture
def temp_manager_dir(tmp_path):
    storage_dir = str(tmp_path / "episodes")
    yield storage_dir
    if os.path.exists(storage_dir):
        shutil.rmtree(storage_dir, ignore_errors=True)


def test_episode_manager_crud_operations(temp_manager_dir):
    manager = EpisodeManager(storage_dir=temp_manager_dir)

    # 1. Create and Save
    ep = Episode(episode_id="battle_12", timestamp=1000.0, winner="Player")
    saved_path = manager.save_episode(ep)
    assert os.path.exists(saved_path)

    # 2. List
    episodes = manager.list_episodes()
    assert episodes == ["battle_12"]

    # 3. Load
    loaded = manager.load_episode("battle_12")
    assert loaded is not None
    assert loaded.episode_id == "battle_12"
    assert loaded.winner == "Player"

    # 4. Search
    results = manager.search_by_id("12")
    assert len(results) == 1
    assert results[0].episode_id == "battle_12"

    # 5. Delete
    deleted = manager.delete_episode("battle_12")
    assert deleted is True
    assert manager.get_total_count() == 0
