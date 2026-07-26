"""Unit tests for IntentDatasetPreprocessor dataset v1 creation."""

import pytest
import os
import json
import shutil
from backend.cognitive_os.ml.intent_prediction.preprocessing import IntentDatasetPreprocessor


@pytest.fixture
def temp_dataset_v1_dir(tmp_path):
    root_dir = str(tmp_path / "intent_prediction")
    yield root_dir
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir, ignore_errors=True)


def test_intent_dataset_v1_creation(temp_dataset_v1_dir):
    preprocessor = IntentDatasetPreprocessor(dataset_root=temp_dataset_v1_dir)
    paths = preprocessor.build_and_save_v1_dataset()

    assert os.path.exists(paths["train_path"])
    assert os.path.exists(paths["validation_path"])
    assert os.path.exists(paths["test_path"])
    assert os.path.exists(paths["metadata_path"])

    with open(paths["metadata_path"], "r", encoding="utf-8") as f:
        meta = json.load(f)

    assert meta["dataset_version"] == "v1"
    assert meta["sample_count"] == 1000
    assert len(meta["feature_names"]) == 17
    assert len(meta["label_names"]) == 9
    assert "creation_date" in meta
