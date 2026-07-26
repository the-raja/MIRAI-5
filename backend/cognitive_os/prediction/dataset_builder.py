"""DatasetBuilder module.

Converts completed Episode records into supervised ML training rows (Features -> Target Next Action).
Saves structured CSV datasets inside `backend/data/datasets/`.
"""

from typing import List, Dict, Any, Optional
import os
import csv
from backend.cognitive_os.memory.episodic.episode import Episode


class DatasetBuilder:
    def __init__(self, dataset_dir: str = r"backend/data/datasets") -> None:
        self.dataset_dir = dataset_dir
        os.makedirs(self.dataset_dir, exist_ok=True)

    def build_dataset_from_episode(self, episode: Episode) -> List[Dict[str, Any]]:
        """Converts an Episode record into supervised training rows (X_features, y_target)."""
        timeline = episode.timeline
        if not timeline or len(timeline) < 2:
            return []

        rows: List[Dict[str, Any]] = []
        summary = episode.battle_summary

        for i in range(len(timeline) - 1):
            curr_evt = timeline[i]
            next_evt = timeline[i + 1]

            pos = curr_evt.position
            dist = round(curr_evt.metadata.get("distance", summary.average_distance), 2) if curr_evt.metadata else summary.average_distance

            row = {
                "episode_id": episode.episode_id,
                "timestamp": curr_evt.timestamp,
                "distance": dist,
                "player_hp": curr_evt.metadata.get("player_hp", 80.0) if curr_evt.metadata else 80.0,
                "boss_hp": curr_evt.metadata.get("boss_hp", 70.0) if curr_evt.metadata else 70.0,
                "weapon": summary.most_used_weapon,
                "current_action": curr_evt.event_type,
                "reload_count": summary.reload_count,
                "preferred_dodge": summary.preferred_dodge,
                "aggression_score": summary.aggression_score,
                "target_next_action": next_evt.event_type  # Supervised Learning Target Label (y)
            }
            rows.append(row)

        return rows

    def save_dataset_to_csv(self, dataset: List[Dict[str, Any]], filename: str = "training_dataset.csv") -> str:
        """Saves a dataset list to disk as a CSV file."""
        if not dataset:
            return ""

        filepath = os.path.join(self.dataset_dir, filename)
        fieldnames = list(dataset[0].keys())

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dataset)

        return filepath

    def load_dataset_from_csv(self, filename: str = "training_dataset.csv") -> List[Dict[str, Any]]:
        """Loads a dataset from CSV file."""
        filepath = os.path.join(self.dataset_dir, filename)
        if not os.path.exists(filepath):
            return []

        rows: List[Dict[str, Any]] = []
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        return rows
