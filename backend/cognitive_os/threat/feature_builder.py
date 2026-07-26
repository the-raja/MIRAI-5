"""ThreatFeatureBuilder module.

Constructs 17 canonical input features for Threat Ranking:
- Player HP, Boss HP, Distance, Weapon, Ammo, Healing Items, Ultimate Charge, Movement Speed,
  Recent Aggression, Accuracy, Hit Streak, Reload State, Cooldowns, Current Goal,
  Prediction Confidence, Temporal Pattern
"""

from typing import Dict, Any, List
import numpy as np


class ThreatFeatureBuilder:
    @staticmethod
    def build_threat_feature_vector(world_context: Dict[str, Any]) -> List[float]:
        """Extracts 17 normalized numerical features for XGBoost Threat Ranking Model."""
        p_hp = float(world_context.get("player_hp", 80.0)) / 100.0
        b_hp = float(world_context.get("boss_hp", 100.0)) / 100.0
        dist = float(world_context.get("distance", 5.0)) / 30.0
        wep_val = 0.8 if "Sword" in str(world_context.get("weapon", "Sword")) else 0.5
        ammo = float(world_context.get("ammo", 10)) / 30.0
        heals = float(world_context.get("healing_items", 2)) / 5.0
        ult = float(world_context.get("ultimate_charge", 0.75))
        spd = float(world_context.get("movement_speed", 6.0)) / 10.0
        aggr = float(world_context.get("recent_aggression", 0.85))
        acc = float(world_context.get("accuracy", 0.78))
        streak = float(world_context.get("hit_streak", 4)) / 10.0
        reload_st = 1.0 if world_context.get("is_reloading", False) else 0.0
        cd_st = float(world_context.get("cooldown_remaining", 0.0)) / 5.0
        goal_val = 0.9 if "Pressure" in str(world_context.get("current_goal", "Pressure Player")) else 0.5
        pred_conf = float(world_context.get("prediction_confidence", 0.94))
        temp_patt = 0.86

        return [
            p_hp, b_hp, dist, wep_val, ammo, heals, ult, spd,
            aggr, acc, streak, reload_st, cd_st, goal_val, pred_conf, temp_patt, 0.5
        ]
