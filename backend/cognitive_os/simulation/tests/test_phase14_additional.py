"""Additional unit tests for Phase 14 Simulation Framework."""

import pytest
from backend.cognitive_os.simulation.match_runner import MatchRunner
from backend.cognitive_os.simulation.tournament import TournamentRunner
from backend.cognitive_os.simulation.scenario import BattleScenario


def test_match_runner_opponent_variations():
    runner = MatchRunner()
    r1 = runner.run_match(opponent_type="Random AI")
    r2 = runner.run_match(opponent_type="Previous Version")

    assert r1["opponent_type"] == "Random AI"
    assert r2["opponent_type"] == "Previous Version"


def test_tournament_runner_scenario_cycling():
    t_runner = TournamentRunner()
    res = t_runner.run_tournament(num_matches=6)
    assert res["total_matches"] == 6


def test_scenario_custom_creation():
    scen = BattleScenario(
        scenario_id="custom_01",
        name="Custom Scenario",
        player_style="Sniper",
        weapon="Rifle",
        player_hp=50.0
    )
    assert scen.scenario_id == "custom_01"
    assert scen.player_style == "Sniper"
