"""Unit tests for Skill Rating modules."""

import pytest
from backend.cognitive_os.skill.skill_model import SkillModel, PlayerSkillProfile
from backend.cognitive_os.skill.bayesian_rating import BayesianSkillRating


def test_skill_model_evaluation_and_adaptation():
    # Novice player (Reaction time 380ms, low accuracy 20%, low dodge 20%)
    novice_prof = SkillModel.evaluate_skill({"reaction_time_ms": 380.0, "accuracy_pct": 20.0, "dodge_success_pct": 20.0, "combo_length": 1, "average_damage": 20.0})
    assert novice_prof.skill_score < 30.0
    assert novice_prof.skill_tier == "Novice"
    assert novice_prof.forgiving_mode is True
    assert novice_prof.planning_depth == 2

    # Professional player (Reaction time 170ms, high accuracy 92%, high dodge 90%)
    pro_prof = SkillModel.evaluate_skill({"reaction_time_ms": 170.0, "accuracy_pct": 92.0, "dodge_success_pct": 90.0, "combo_length": 8, "average_damage": 95.0})
    assert pro_prof.skill_score >= 80.0
    assert pro_prof.skill_tier in ["Expert", "Professional"]
    assert pro_prof.forgiving_mode is False
    assert pro_prof.planning_depth in [4, 5]


def test_bayesian_skill_rating():
    rating = BayesianSkillRating(mu=50.0, sigma=8.0)
    mu1, sig1 = rating.update_rating(match_outcome_win=True)
    assert mu1 > 50.0

    mu2, sig2 = rating.update_rating(match_outcome_win=False)
    assert mu2 < mu1
