"""Intent Prediction Configuration & Canonical Feature Schema Specification.

Frozen feature schema v1.0.0 for tabular XGBoost intent classification.
Strict versioning: Do NOT add features without incrementing FEATURE_SCHEMA_VERSION.
"""

from typing import List, Dict, Any

FEATURE_SCHEMA_VERSION: str = "v1.0.0"

CANONICAL_FEATURE_LIST: List[str] = [
    "distance",
    "player_hp",
    "boss_hp",
    "stamina",
    "weapon",
    "current_action",
    "last_action",
    "last_5_action_histogram",
    "aggression_score",
    "reload_frequency",
    "preferred_dodge",
    "preferred_weapon",
    "time_since_reload",
    "time_since_heal",
    "time_since_damage",
    "boss_cooldown",
    "player_cooldown"
]

INTENT_CLASSES: List[str] = [
    "ATTACK",
    "HEAVY_ATTACK",
    "BLOCK",
    "DODGE_LEFT",
    "DODGE_RIGHT",
    "HEAL",
    "RELOAD",
    "RETREAT",
    "IDLE"
]

# Numerical feature columns used for XGBoost matrix construction
NUMERICAL_FEATURE_KEYS: List[str] = [
    "distance",
    "player_hp",
    "boss_hp",
    "stamina",
    "aggression_score",
    "reload_frequency",
    "time_since_reload",
    "time_since_heal",
    "time_since_damage",
    "boss_cooldown",
    "player_cooldown"
]

# Categorical feature columns needing LabelEncoder / OneHot
CATEGORICAL_FEATURE_KEYS: List[str] = [
    "weapon",
    "current_action",
    "last_action",
    "preferred_dodge",
    "preferred_weapon"
]

# XGBoost Model Hyperparameters
DEFAULT_XGB_HYPERPARAMETERS: Dict[str, Any] = {
    "n_estimators": 100,
    "max_depth": 5,
    "learning_rate": 0.08,
    "objective": "multi:softprob",
    "num_class": len(INTENT_CLASSES),
    "random_state": 42,
    "subsample": 0.8,
    "colsample_bytree": 0.8
}
