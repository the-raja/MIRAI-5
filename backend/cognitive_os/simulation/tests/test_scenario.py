"""Unit tests for BattleScenario."""

import pytest
from backend.cognitive_os.simulation.scenario import BattleScenario


def test_battle_scenario_suite():
    scenarios = BattleScenario.get_standard_scenarios()
    assert len(scenarios) == 3

    assert scenarios[0].scenario_id == "scenario_a"
    assert scenarios[0].player_style == "Aggressive"
    assert scenarios[0].weapon == "Sword"

    assert scenarios[1].scenario_id == "scenario_b"
    assert scenarios[1].player_hp == 30.0

    assert scenarios[2].scenario_id == "scenario_c"
    assert scenarios[2].player_style == "Random"
