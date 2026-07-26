"""ThreatCalibrator module.

Calibrates raw XGBoost threat scores to ensure reliable, smooth probability estimates.
"""

from typing import List, Tuple, Dict, Any


class ThreatCalibrator:
    @staticmethod
    def calibrate_score(raw_score: float, confidence: float = 0.94) -> float:
        """Calibrates raw threat score using prediction confidence weighting."""
        calibrated = (raw_score * 0.8) + (confidence * 0.2)
        return max(0.0, min(1.0, round(calibrated, 2)))
