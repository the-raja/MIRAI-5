# MIRAI v2 — Cognitive OS Data Schemas & Language Specification

> **Data Language Specification:**  
> This document defines the exact structural schemas for the primary data objects passed between modules in the MIRAI Cognitive OS. No code implementations are included—only formal field definitions, types, and value constraints.

---

## 1. PlayerState
Represents the complete instantaneous state of a human player or bot in the arena.

| Field | Type | Description / Constraints |
| :--- | :--- | :--- |
| `id` | `String` | Unique entity identifier (e.g., `"player_raja_01"`). |
| `position` | `Vector3` | Spatial coordinates `(x: Float, y: Float, z: Float)`. |
| `velocity` | `Vector3` | Directional velocity vector `(vx: Float, vy: Float, vz: Float)`. |
| `health` | `Float` | Current health points `[0.0, 100.0]`. |
| `stamina` | `Float` | Current stamina points `[0.0, 100.0]`. |
| `posture` | `Float` | Balance / guard break meter `[0.0, 100.0]`. |
| `weapon` | `String` | Currently equipped weapon identifier (e.g., `"Katana"`, `"Sniper"`). |
| `animation` | `String` | Active animation state (e.g., `"Heavy_Attack_Windup"`, `"Dodge_Left"`). |
| `current_action` | `String` | High-level action label (e.g., `"ATTACK"`, `"RELOAD"`, `"HEAL"`, `"IDLE"`). |
| `target` | `String / Null` | Entity ID currently targeted by this player. |
| `status_effects` | `List[String]` | Active buffs/debuffs (e.g., `["Stunned", "Shielded"]`). |
| `team` | `String` | Team assignment (e.g., `"PLAYERS"`, `"BOSS"`). |
| `alive` | `Boolean` | Life status (`True` if active, `False` if eliminated). |

---

## 2. WorldState
Represents the global spatial, topological, and environmental snapshot of the arena.

| Field | Type | Description / Constraints |
| :--- | :--- | :--- |
| `timestamp_ms` | `Integer` | Epoch timestamp in milliseconds. |
| `frame_id` | `Integer` | Sequential frame counter. |
| `combatants` | `Map[String, PlayerState]` | Map of entity IDs to their `PlayerState`. |
| `boss_state` | `PlayerState` | Instantaneous state of the boss agent. |
| `cover_nodes` | `List[CoverNode]` | Cover points with position, height, and occupation status. |
| `visibility_matrix` | `Map[Pair[String, String], Boolean]` | Line-of-sight status between all entity pairs. |
| `line_of_fire_matrix`| `Map[Pair[String, String], Boolean]` | Clear firing line status between all entity pairs. |
| `hazard_zones` | `List[HazardArea]` | Active environmental danger areas. |

---

## 3. Observation
Normalized, feature-engineered observation matrix produced by the Perception Engine.

| Field | Type | Description / Constraints |
| :--- | :--- | :--- |
| `timestamp_ms` | `Integer` | Timestamp of perceived observation. |
| `distances` | `Map[String, Float]` | Euclidian distance from Boss to every combatant. |
| `health_percentages`| `Map[String, Float]` | Health ratios `[0.0, 1.0]` for all combatants. |
| `is_player_visible` | `Boolean` | Flag indicating line-of-sight to primary target. |
| `is_player_sprinting`| `Boolean` | Flag indicating player velocity exceeds sprint threshold. |
| `is_player_reloading`| `Boolean` | Flag indicating active reload animation. |
| `is_player_in_cover` | `Boolean` | Flag indicating player position coincides with cover node. |
| `is_boss_under_attack`| `Boolean` | Flag indicating incoming projectiles or hitboxes. |
| `feature_vector` | `List[Float]` | Flat 1D normalized float array for ML model input. |

---

## 4. Goal
High-level strategic objective formulated by the Goal Manager.

| Field | Type | Description / Constraints |
| :--- | :--- | :--- |
| `goal_id` | `String` | Unique goal identifier (e.g., `"GOAL_ELIMINATE_MEDIC"`). |
| `type` | `String` | Goal category (`"ELIMINATE"`, `"RETREAT"`, `"FLANK"`, `"DEFEND"`). |
| `target_entity_id` | `String / Null` | Target entity of the objective. |
| `priority_weight` | `Float` | Strategic importance score `[0.0, 1.0]`. |
| `creation_timestamp`| `Integer` | Frame timestamp when goal was activated. |
| `expiry_conditions` | `List[String]` | Conditions under which goal terminates (e.g., `"TARGET_DIED"`). |

---

## 5. Prediction
Forecast bundle produced by the Prediction Engine.

| Field | Type | Description / Constraints |
| :--- | :--- | :--- |
| `predicted_trajectory`| `List[Vector3]` | Spatial path sequence for primary target over next $N$ frames ($t+0.5\text{s}$). |
| `trajectory_confidence`| `Float` | Model confidence score `[0.0, 1.0]`. |
| `intent_probabilities`| `Map[String, Float]` | Probabilities over player actions (`HEAL`, `RELOAD`, `PARRY`, etc.). |
| `top_predicted_intent` | `String` | Highest probability intent label. |
| `threat_rankings` | `List[ThreatScore]` | Ranked list of entities with threat scores and rationale. |

---

## 6. Memory
Episodic memory structure retrieved from FAISS + HNSW storage.

| Field | Type | Description / Constraints |
| :--- | :--- | :--- |
| `memory_id` | `String` | Unique memory record UUID. |
| `similarity_score` | `Float` | Vector cosine/L2 similarity metric `[0.0, 1.0]`. |
| `historical_embedding`| `List[Float]` | 512-dim embedding vector of past encounter. |
| `recorded_player_style`| `String` | Behavior classification (e.g., `"Aggressive_Counter_Fighter"`). |
| `successful_counter` | `String` | Counter-action that proved effective in that fight. |
| `outcome` | `String` | Historic match result (`"BOSS_VICTORY"`, `"BOSS_DEFEAT"`). |

---

## 7. UtilityAction
Evaluated candidate action with utility scoring breakdown.

| Field | Type | Description / Constraints |
| :--- | :--- | :--- |
| `action_id` | `String` | Candidate action identifier (e.g., `"HEAVY_FLANK_ATTACK"`). |
| `base_score` | `Float` | Unweighted utility score `[0.0, 1.0]`. |
| `goal_alignment_score`| `Float` | Alignment multiplier based on active `Goal`. |
| `memory_bias_score` | `Float` | Modifier based on retrieved historical memory confidence. |
| `risk_penalty` | `Float` | Risk deduction score based on positioning and danger. |
| `final_utility` | `Float` | Net weighted utility score (`(base * goal * memory) - risk`). |

---

## 8. Decision
The explainable decision packet selected by Utility AI and sent to Planner.

| Field | Type | Description / Constraints |
| :--- | :--- | :--- |
| `decision_id` | `String` | Unique decision instance UUID. |
| `chosen_action` | `UtilityAction` | Winning candidate action with highest utility. |
| `evaluated_candidates`| `List[UtilityAction]`| Complete list of candidate actions considered and their scores. |
| `explainability_audit`| `AuditLog` | Structured key-value object containing the explicit *why* rationale. |
| `timestamp_ms` | `Integer` | Decision timestamp. |

---

## 9. LearningRecord
Post-match evaluation log processed by the Learning Engine.

| Field | Type | Description / Constraints |
| :--- | :--- | :--- |
| `match_id` | `String` | Unique match session identifier. |
| `total_frames` | `Integer` | Total frames recorded during match. |
| `movement_rmse` | `Float` | Root Mean Squared Error of movement trajectory predictions. |
| `intent_accuracy` | `Float` | Classification accuracy percentage for intent model. |
| `strategy_win_rate` | `Float` | Updated win rate metric for applied counter-strategy. |
| `bayesian_skill_delta`| `Float` | Updated skill rating increment/decrement for player profile. |
| `new_checkpoint_path`| `String / Null` | Path to newly saved model artifact (if retrained). |
