"""TemporalSequenceDatasetBuilder module.

Converts episode action timelines into sliding window sequence samples:
Input Window: [Attack, Attack, Reload, Heal] -> Target: Attack

Generates thousands of supervised temporal sequence training pairs from battle history.
"""

from typing import List, Dict, Any, Optional, Tuple
import os
import json
import random
from backend.cognitive_os.memory.episodic.episode import Episode


class TemporalSequenceDatasetBuilder:
    def __init__(self, window_size: int = 4) -> None:
        self.window_size = window_size

    def build_sequence_samples(self, action_sequence: List[str]) -> List[Dict[str, Any]]:
        """Converts a raw list of chronological actions into sliding window input/target sequence pairs."""
        samples: List[Dict[str, Any]] = []
        if len(action_sequence) <= self.window_size:
            return samples

        for i in range(len(action_sequence) - self.window_size):
            input_window = action_sequence[i : i + self.window_size]
            target_action = action_sequence[i + self.window_size]

            sample = {
                "sample_id": f"seq_{i}",
                "sequence_input": input_window,
                "sequence_length": len(input_window),
                "target_next_action": target_action
            }
            samples.append(sample)

        return samples

    def build_dataset_from_episodes(
        self,
        episodes: List[Episode],
        train_ratio: float = 0.8,
        val_ratio: float = 0.1
    ) -> Dict[str, Any]:
        """Generates full train/val/test splits from a list of battle episodes."""
        all_samples: List[Dict[str, Any]] = []

        for ep in episodes:
            actions = []
            for evt in ep.timeline:
                # Extract action string from timeline event
                act_str = evt.event_type.replace("Player ", "").replace("ed", "").replace("d", "")
                actions.append(act_str)

            if len(actions) > self.window_size:
                ep_samples = self.build_sequence_samples(actions)
                all_samples.extend(ep_samples)

        random.seed(42)
        random.shuffle(all_samples)

        total = len(all_samples)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)

        return {
            "train": all_samples[:train_end],
            "validation": all_samples[train_end:val_end],
            "test": all_samples[val_end:],
            "total_samples": total,
            "window_size": self.window_size
        }
