"""Unit tests for Threat Ranking modules."""

import pytest
from backend.cognitive_os.threat.feature_builder import ThreatFeatureBuilder
from backend.cognitive_os.threat.threat_model import XGBoostThreatModel
from backend.cognitive_os.threat.threat_ranker import ThreatRanker
from backend.cognitive_os.threat.online_updater import OnlineThreatUpdater
from backend.cognitive_os.threat.calibration import ThreatCalibrator
from backend.cognitive_os.threat.threat_report import ThreatReportFormatter


def test_threat_feature_builder_17_features():
    vec = ThreatFeatureBuilder.build_threat_feature_vector({"player_hp": 34.0, "ultimate_charge": 0.95})
    assert len(vec) == 17


def test_xgboost_threat_model_evaluation():
    model = XGBoostThreatModel()
    s_ult = model.evaluate_threat_score("Ultimate", {})
    s_heal = model.evaluate_threat_score("Healing", {})
    s_reload = model.evaluate_threat_score("Reload", {})
    s_retreat = model.evaluate_threat_score("Retreat", {})

    assert s_ult == 0.95
    assert s_heal == 0.91
    assert s_reload == 0.28
    assert s_retreat == 0.16


def test_threat_ranker_ordering():
    ranker = ThreatRanker()
    ranked = ranker.rank_threats(["Healing", "Reload", "Ultimate", "Retreat"])

    assert ranked[0][0] == "Ultimate"
    assert ranked[0][1] == 0.95
    assert ranked[1][0] == "Healing"
    assert ranked[1][1] == 0.91
    assert ranked[2][0] == "Reload"
    assert ranked[2][1] == 0.28
    assert ranked[3][0] == "Retreat"
    assert ranked[3][1] == 0.16


def test_threat_calibrator_and_updater():
    cal = ThreatCalibrator.calibrate_score(0.91, confidence=0.95)
    assert 0.0 <= cal <= 1.0

    updater = OnlineThreatUpdater()
    res = updater.update_threat_weights("Healing", 45.0)
    assert res["status"] == "THREAT_WEIGHTS_UPDATED"


def test_threat_report_formatter():
    report = ThreatReportFormatter.format_threat_report([
        ("Ultimate", 0.95),
        ("Healing", 0.91),
        ("Reload", 0.28),
        ("Retreat", 0.16)
    ])
    assert "Threat Ranking" in report
    assert "Ultimate" in report
    assert "0.95" in report
    assert "0.91" in report
