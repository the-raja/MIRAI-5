"""PredictionFusionEngine module.

Researched Prediction Fusion component combining single-state XGBoost intent predictions with multi-step LSTM temporal predictions.

Example Agreement:
XGBoost: Reload (91%) | LSTM: Reload (88%) -> Final Prediction: Reload (94%)

Example Disagreement:
XGBoost: Heal (72%) | LSTM: Retreat (84%) -> Fusion Decision: Retreat (Reason: Temporal model confidence higher.)
"""

from typing import Optional, Dict, Any
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.ml.fusion.confidence_calibrator import ConfidenceCalibrator


class PredictionFusionEngine:
    def __init__(self) -> None:
        self.calibrator = ConfidenceCalibrator()

    def fuse_predictions(self, xgb_pred: Prediction, lstm_pred: Prediction) -> Prediction:
        """Fuses single-state XGBoost and multi-step LSTM predictions with explainable audit traces."""
        c_time = max(xgb_pred.timestamp, lstm_pred.timestamp)
        agree = (xgb_pred.action.upper() == lstm_pred.action.upper())

        fused_conf = self.calibrator.calibrate_confidence(xgb_pred.confidence, lstm_pred.confidence, agree)

        if agree:
            fused_action = xgb_pred.action
            reason = f"Dual Prediction Fusion (Agreement): Both XGBoost ({xgb_pred.action}) & LSTM sequence match ({int(fused_conf*100)}% conf)."
        else:
            if lstm_pred.confidence > xgb_pred.confidence:
                fused_action = lstm_pred.action
                reason = f"Temporal model confidence higher ({int(lstm_pred.confidence*100)}% vs {int(xgb_pred.confidence*100)}%)."
            else:
                fused_action = xgb_pred.action
                reason = f"Single-state tabular model confidence higher ({int(xgb_pred.confidence*100)}% vs {int(lstm_pred.confidence*100)}%)."

        return Prediction(
            prediction_id=f"pred_fused_{int(c_time*1000)}",
            timestamp=c_time,
            action=fused_action,
            confidence=fused_conf,
            time_horizon=2.0,
            reason=reason,
            source="Dual Prediction Fusion (XGBoost + LSTM)",
            metadata={
                "xgb_action": xgb_pred.action,
                "xgb_confidence": xgb_pred.confidence,
                "lstm_action": lstm_pred.action,
                "lstm_confidence": lstm_pred.confidence,
                "agreement": agree
            }
        )
