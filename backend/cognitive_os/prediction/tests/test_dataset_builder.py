"""Unit tests for DatasetBuilder supervised training dataset creation."""

import pytest
import os
import shutil
from backend.cognitive_os.prediction.dataset_builder import DatasetBuilder
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.timeline_event import TimelineEvent
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary


@pytest.fixture
def temp_dataset_dir(tmp_path):
    dataset_dir = str(tmp_path / "datasets")
    yield dataset_dir
    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir, ignore_errors=True)


def test_dataset_builder_build_and_csv_export(temp_dataset_dir):
    builder = DatasetBuilder(dataset_dir=temp_dataset_dir)

    episode = Episode(
        episode_id="ep_dataset_01",
        timestamp=1000.0,
        timeline=[
            TimelineEvent(event_id="e1", timestamp=1005.0, event_type="Player Reloaded", importance=90.0),
            TimelineEvent(event_id="e2", timestamp=1010.0, event_type="Player Dodged Left", importance=70.0),
            TimelineEvent(event_id="e3", timestamp=1015.0, event_type="BossHit", importance=80.0)
        ],
        battle_summary=BattleSummary(match_id="ep_dataset_01", most_used_weapon="Shotgun", preferred_dodge="Left")
    )

    rows = builder.build_dataset_from_episode(episode)
    assert len(rows) == 2  # (e1 -> e2), (e2 -> e3)

    assert rows[0]["current_action"] == "Player Reloaded"
    assert rows[0]["target_next_action"] == "Player Dodged Left"
    assert rows[1]["target_next_action"] == "BossHit"

    filepath = builder.save_dataset_to_csv(rows, filename="test_dataset.csv")
    assert os.path.exists(filepath)

    loaded = builder.load_dataset_from_csv(filename="test_dataset.csv")
    assert len(loaded) == 2
    assert loaded[0]["target_next_action"] == "Player Dodged Left"
