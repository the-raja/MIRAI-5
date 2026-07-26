# MIRAI v2 — Prediction System Specification

## 1. Subsystem Scope
- **Movement Predictor:** Standard interface `IMovementPredictor`. Predicts future player spatial coordinates (e.g. t+0.5s) using sequential models (LSTM / Temporal Transformer).
- **Intent Predictor:** Standard interface `IIntentPredictor`. Predicts immediate player actions (Reload, Heal, Attack, Parry, Retreat) using tabular classifiers (XGBoost / LightGBM).
- **Threat Ranking Engine:** Ranks multi-agent team targets by strategic value.

## 2. Abstraction Contract
Models are strictly decoupled via interface wrappers allowing modular backend replacement without changing consuming logic.
