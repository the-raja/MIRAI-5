"""Unit tests for ModelVersionManager semantic version lineage."""

import pytest
from backend.cognitive_os.learning.model_version import ModelVersionManager, ModelVersion


def test_model_version_manager_lineage():
    vm = ModelVersionManager()

    v1 = vm.get_current_version()
    assert v1.version_id == "v1.0.0"

    v2 = vm.create_next_version("Post-battle 12 adaptation")
    assert v2.version_id == "v1.0.1"

    v3 = vm.create_next_version("Post-battle 13 adaptation")
    assert v3.version_id == "v1.0.2"

    history = vm.get_version_history()
    assert len(history) == 3
    assert history[0].version_id == "v1.0.0"
    assert history[1].version_id == "v1.0.1"
    assert history[2].version_id == "v1.0.2"
