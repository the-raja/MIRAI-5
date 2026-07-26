"""ConfidenceCalibrator module.

Calibrates confidence scores when fusing single-state tabular XGBoost predictions with multi-step temporal LSTM predictions.
"""

from typing import Tuple, Dict, Any


class ConfidenceCalibrator:
    @staticmethod
    def calibrate_confidence(xgb_conf: float, lstm_conf: float, agree: bool) -> float:
        """Calibrates confidence based on model agreement and individual confidence bounds."""
        if agree:
            # Boost confidence when models reinforce each other
            boosted = max(xgb_conf, lstm_conf) + 0.03
            return round(min(0.99, boosted), 4)

        # Non-agreement: return winning model's calibrated confidence
        winning_conf = max(xgb_conf, lstm_conf)
        return round(winning_conf, 4)
