"""Unit tests for DatasetManager dataset splitting and normalization."""

import pytest
from backend.cognitive_os.ml.dataset import DatasetManager, DatasetMetadata, DatasetSplit


def test_dataset_manager_train_val_test_split():
    mgr = DatasetManager()
    rows = [{"distance": float(i), "hp": 100.0, "target_next_action": "Reload"} for i in range(100)]

    split = mgr.create_split(rows, dataset_id="ds_test", train_ratio=0.8, val_ratio=0.1, test_ratio=0.1)

    assert split.metadata.num_samples == 100
    assert len(split.train_data) == 80
    assert len(split.val_data) == 10
    assert len(split.test_data) == 10
    assert "distance" in split.metadata.feature_names
    assert "target_next_action" in split.metadata.label_names


def test_dataset_manager_normalization_hooks():
    mgr = DatasetManager()
    rows = [
        {"distance": 10.0, "target_next_action": "Reload"},
        {"distance": 20.0, "target_next_action": "Dodge"},
        {"distance": 30.0, "target_next_action": "Attack"}
    ]

    norm = mgr.apply_normalization_hooks(rows, feature_keys=["distance"])
    assert norm[0]["distance_normalized"] == 0.0
    assert norm[1]["distance_normalized"] == 0.5
    assert norm[2]["distance_normalized"] == 1.0
