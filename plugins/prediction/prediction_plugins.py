"""Prediction Plugin Ecosystem.

Swappable prediction implementations:
- XGBoostPlugin
- TransformerPlugin
- RuleBasedPlugin
"""

from typing import Dict, Any


class BasePredictionPlugin:
    def predict(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class XGBoostPlugin(BasePredictionPlugin):
    def predict(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        return {"action": "Reload", "confidence": 0.91, "plugin": "XGBoost"}


class TransformerPlugin(BasePredictionPlugin):
    def predict(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        return {"action": "Left Dodge", "confidence": 0.93, "plugin": "Transformer"}


class RuleBasedPlugin(BasePredictionPlugin):
    def predict(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        return {"action": "Block", "confidence": 0.74, "plugin": "RuleBased"}
