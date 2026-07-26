"""Unit tests for MatchRunner and TournamentRunner."""

import pytest
from backend.cognitive_os.simulation.match_runner import MatchRunner
from backend.cognitive_os.simulation.tournament import TournamentRunner


def test_match_runner_single_match():
    runner = MatchRunner()
    res = runner.run_match(mirai_version="v1.2-planner", opponent_type="Scripted AI")

    assert "winner" in res
    assert "duration_sec" in res
    assert "mirai_damage_dealt" in res


def test_tournament_runner_series():
    t_runner = TournamentRunner()
    res = t_runner.run_tournament(
        mirai_version="MIRAI v2",
        opponent_type="Scripted AI",
        num_matches=100
    )

    assert res["total_matches"] == 100
    assert res["mirai_wins"] + res["mirai_losses"] == 100
    assert 0.0 <= res["win_rate_pct"] <= 100.0
    assert res["average_duration_sec"] > 0.0
