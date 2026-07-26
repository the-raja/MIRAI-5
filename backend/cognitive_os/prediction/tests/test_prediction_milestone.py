"""Phase 7 Prediction Engine Milestone Unit Tests.

Explicitly verifies the 6 core prediction contracts:
1. Feature extraction
2. Dataset generation
3. Baseline prediction
4. Prediction evaluation
5. Pipeline integration
6. Accuracy tracking
"""

import pytest
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.prediction.feature_extractor import FeatureExtractor, FeatureVector
from backend.cognitive_os.prediction.dataset_builder import DatasetBuilder
from backend.cognitive_os.prediction.baseline_predictor import BaselinePredictor
from backend.cognitive_os.prediction.evaluation import PredictionEvaluator
from backend.cognitive_os.prediction.prediction_engine import PredictionEngine
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.timeline_event import TimelineEvent
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary


def test_1_feature_extraction():
    """Case 1: Feature Extraction vector creation."""
    extractor = FeatureExtractor()
    wm = WorldModel(timestamp=10.0)
    vec = extractor.extract_features(world_model=wm, recent_actions=["Attack", "Attack"])

    assert vec.distance >= 0.0
    assert len(vec.to_numpy_array()) == 7


def test_2_dataset_generation():
    """Case 2: Dataset Generation creates supervised training rows."""
    builder = DatasetBuilder()
    ep = Episode(
        episode_id="ep_milestone_1",
        timestamp=1000.0,
        timeline=[
            TimelineEvent(event_id="e1", timestamp=1005.0, event_type="Player Reloaded"),
            TimelineEvent(event_id="e2", timestamp=1010.0, event_type="Player Dodged Left")
        ],
        battle_summary=BattleSummary(match_id="ep_milestone_1")
    )
    rows = builder.build_dataset_from_episode(ep)
    assert len(rows) == 1
    assert rows[0]["target_next_action"] == "Player Dodged Left"


def test_3_baseline_prediction():
    """Case 3: Baseline Prediction rule-based statistical inference."""
    predictor = BaselinePredictor()
    pred = predictor.predict(recent_actions=["Attack", "Attack", "Attack"], current_time=10.0)
    assert pred.action == "Reload"
    assert pred.confidence == 0.74


def test_4_prediction_evaluation():
    """Case 4: Prediction Evaluation metrics tracking."""
    evaluator = PredictionEvaluator()
    evaluator.record_outcome(predicted_action="Reload", actual_action="Reload")
    evaluator.record_outcome(predicted_action="Reload", actual_action="Dodge")

    metrics = evaluator.compute_metrics()
    assert metrics.total_samples == 2
    assert metrics.accuracy == 0.50


def test_5_pipeline_integration():
    """Case 5: Pipeline Integration (Semantic Memory -> Prediction Engine -> Goal Manager)."""
    engine = PredictionEngine()
    wm = WorldModel(timestamp=10.0)

    pred = engine.generate_prediction(world_model=wm, recent_actions=["Attack", "Attack", "Attack"])
    assert pred.action.upper() == "RELOAD"
    assert pred.confidence >= 0.70


def test_6_accuracy_tracking():
    """Case 6: Accuracy Tracking confusion matrix generation."""
    evaluator = PredictionEvaluator()
    for _ in range(5):
        evaluator.record_outcome("Reload", "Reload")

    metrics = evaluator.compute_metrics()
    assert metrics.accuracy == 1.0
    assert metrics.confusion_matrix["Reload"]["Reload"] == 5
