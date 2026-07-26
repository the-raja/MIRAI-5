"""Unit tests for IntentDataValidator pre-training dataset validation."""

import pytest
from backend.cognitive_os.ml.intent_prediction.preprocessing import IntentDataValidator


def test_validator_detects_invalid_label_and_aborts():
    validator = IntentDataValidator()

    bad_rows = [
        {"distance": 5.0, "player_hp": 80.0, "target_next_action": "INVALID_ACTION_NAME"}
    ]

    is_valid, errors = validator.validate_dataset(bad_rows)
    assert is_valid is False
    assert any("Invalid label" in err for err in errors)


def test_validator_detects_missing_required_feature():
    validator = IntentDataValidator()

    bad_rows = [
        {"player_hp": 80.0, "target_next_action": "RELOAD"}  # Missing distance and other required 16 features
    ]

    is_valid, errors = validator.validate_dataset(bad_rows)
    assert is_valid is False
    assert any("Missing value for required feature" in err for err in errors)
