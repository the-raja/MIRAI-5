# MIRAI v2 — Cognitive OS Data Flow & Module Specifications

> **Master Brain Specification:**  
> This document defines the exact data contracts, inputs, outputs, operational frequencies, and concrete examples for every subsystem in the MIRAI Cognitive OS before any AI algorithms or code are written.

---

## 1. Master Data Flow Diagram

```
Player Input
      │
      ▼
Telemetry Collector
      │
      ▼
Perception Engine
      │
      ▼
Attention Engine
      │
      ▼
World Model
      │
      ▼
Memory System
      │
      ▼
Prediction Engine
      │
      ▼
Goal Manager
      │
      ▼
Utility AI
      │
      ▼
Planner
      │
      ▼
Motor Planner
      │
      ▼
Game Engine
      │
      ▼
Learning Engine
      │
      ▼
Persistent Memory
```

---

## 2. Complete Module Specifications

### 1. Player Input
* **Purpose:** Capture physical human or bot inputs at the hardware/virtual controller boundary.
* **Input:** Keyboard keys, mouse coordinates/deltas, controller buttons, joystick axes.
* **Output:** `RawInputSignal` (unprocessed input events).
* **Frequency:** Real-time / Event-driven (up to 1000 Hz).
* **Examples:** `Key_W_Down`, `Mouse_Move(+12, -4)`, `Right_Trigger_Pressed`, `Dodge_Button_Press`.

---

### 2. Telemetry Collector
* **Purpose:** Collect raw game events, entity transforms, and combat stats every frame.
* **Input:** `RawInputSignal`, Player position, NPC positions, Boss position, combat stats.
* **Output:** `TelemetryFrame` (timestamped snapshot of the raw combat environment).
* **Frequency:** 60 Hz.
* **Examples:**  
  - `player_pos: (12.4, 0.0, -4.2)`  
  - `player_hp: 85`  
  - `player_stamina: 40`  
  - `boss_pos: (2.1, 0.0, 1.0)`  
  - `active_weapon: Katana`  
  - `timestamp_ms: 1722000000123`

---

### 3. Perception Engine
* **Purpose:** Convert raw telemetry into normalized feature observations and state changes.
* **Input:** `TelemetryFrame` stream.
* **Output:** `ObservationSet` (normalized feature vectors and semantic observation flags).
* **Frequency:** 60 Hz.
* **Examples:**  
  - `Player_Visible: True`  
  - `Player_Sprinting: True`  
  - `Player_Attacking: False`  
  - `Player_Reloading: True`  
  - `Player_Entered_Cover: True`  
  - `Boss_Under_Attack: False`  
  - `Distance_To_Player: 4.8m`  
  - `Player_HP_Pct: 0.85`

---

### 4. Attention Engine
* **Purpose:** Filter cognitive noise, score event saliency, and isolate priority targets.
* **Input:** `ObservationSet`.
* **Output:** `SalientEvents` & `PriorityTargets` (focused list of urgent tactical items).
* **Frequency:** 60 Hz.
* **Examples:**  
  - `Urgent_Threat: Medic reviving teammate (Distance: 3.1m)`  
  - `Salient_Event: Player reloading behind low wall`  
  - `Ignored_Event: Sniper 50m away missing shots`

---

### 5. World Model
* **Purpose:** Build and maintain spatial graph topology, line-of-sight visibility, cover points, and dynamic hazard nodes.
* **Input:** `ObservationSet`, `SalientEvents`, static map geometry.
* **Output:** `WorldGraph` (node-edge spatial and visibility graph).
* **Frequency:** 30 Hz.
* **Examples:**  
  - `CoverNode_A: Connected to CoverNode_B (Distance: 6m, Flank Risk: LOW)`  
  - `Player_Node: Currently in CoverNode_A`  
  - `Line_Of_Sight: Boss → Player = BLOCKED`  
  - `Line_Of_Sight: Boss → Medic = CLEAR`

---

### 6. Memory System
* **Purpose:** Query vector database (FAISS + HNSW) to retrieve similar past encounters and effective counter-strategies.
* **Input:** Current `ObservationSet` feature embedding vector.
* **Output:** `RetrievedMemories` (Top-$K$ past fights, strategy confidence ratings, player behavior profiles).
* **Frequency:** 10 Hz / Event-driven.
* **Examples:**  
  - `Match_ID_4821: Similar player dodge-left pattern (Similarity: 0.94)`  
  - `Effective_Counter: Flank_Right (Success_Rate: 0.88)`  
  - `Player_Profile: Aggressive counter-fighter, panics at <30% HP`

---

### 7. Prediction Engine
* **Purpose:** Forecast player future trajectories, short-term action intents, and multi-agent squad threat levels.
* **Input:** Sequence of `ObservationSet` history frames, `WorldGraph`, `RetrievedMemories`.
* **Output:** `PredictionBundle` (movement path predictions, action probabilities, target threat rankings).
* **Frequency:** 20 Hz (Movement) / 10 Hz (Intent & Threat).
* **Examples:**  
  - `Movement_Prediction: Player will be at (14.2, 0.0, -3.1) in t+0.5s (Confidence: 0.89)`  
  - `Intent_Prediction: P(Heal)=0.78, P(Attack)=0.12, P(Retreat)=0.10`  
  - `Threat_Ranking: Medic (0.92) > Player (0.75) > Guardian (0.31)`

---

### 8. Goal Manager
* **Purpose:** Select high-level strategic objectives based on tactical priorities, world topology, and predictions.
* **Input:** `PredictionBundle`, `WorldGraph`, `SalientEvents`.
* **Output:** `StrategicGoal` (active high-level cognitive objective).
* **Frequency:** 5 Hz / Event-driven.
* **Examples:**  
  - `ActiveGoal: Eliminate_Medic`  
  - `ActiveGoal: Retreat_To_Cover`  
  - `ActiveGoal: Pressure_Low_HP_Player`  
  - `ActiveGoal: Bait_Parry`

---

### 9. Utility AI
* **Purpose:** Evaluate and score candidate action options against goal constraints, memory weights, and utility curves to select the optimal tactical action.
* **Input:** `StrategicGoal`, `PredictionBundle`, `WorldGraph`, `RetrievedMemories`.
* **Output:** `ScoredActionPlan` + `ExplainabilityAudit`.
* **Frequency:** 10 Hz.
* **Examples:**  
  - `Selected_Action: Heavy_Flank_Attack`  
  - `Utility_Scores: [Heavy_Flank: 0.87, Direct_Rush: 0.42, Retreat: 0.15]`  
  - `Audit_Rationale: "Target Medic low HP (28%), line-of-sight clear via CoverNode_B, high historical success"`

---

### 10. Planner
* **Purpose:** Decompose high-level action plan into long-term task sequences (HTN) and tick-by-tick combat execution nodes (Behavior Tree).
* **Input:** `ScoredActionPlan`.
* **Output:** `ExecutableTaskSequence` (ordered sub-task execution list).
* **Frequency:** 30 Hz.
* **Examples:**  
  - `SubTask_1: MoveToPosition(10.5, 0.0, -2.1)`  
  - `SubTask_2: FaceTarget(Medic_01)`  
  - `SubTask_3: ExecuteSkill(Shield_Dash)`

---

### 11. Motor Planner
* **Purpose:** Convert abstract sub-tasks into physical kinematic steering vectors, rotation angles, attack timings, and button trigger outputs.
* **Input:** `ExecutableTaskSequence`, current boss kinematic transform.
* **Output:** `MotorCommand` (low-level steering vector, target lock angle, trigger activation signals).
* **Frequency:** 60 Hz.
* **Examples:**  
  - `Steering_Vector: (+0.8, 0.0, -0.6)`  
  - `Turn_Rate: 4.2 rad/s`  
  - `Trigger_Skill_Slot_1: True`  
  - `Animation_Cue: Dash_Start`

---

### 12. Game Engine
* **Purpose:** Execute motor commands within the game simulation, resolve physics/collisions, calculate hitboxes, and update game world state.
* **Input:** `MotorCommand`.
* **Output:** Updated match simulation state, hit registrations, environment deltas.
* **Frequency:** 60 Hz.
* **Examples:**  
  - `Boss_Position_Updated: (3.2, 0.0, 0.5)`  
  - `Hitbox_Collision: True (Damage Applied: 45 to Medic_01)`  
  - `Particle_Effect_Spawned: Dash_Trail`

---

### 13. Learning Engine
* **Purpose:** Evaluate post-match performance, compute prediction loss metrics (RMSE, Accuracy), and update internal model parameters.
* **Input:** Complete match telemetry history, prediction logs, final match outcome (win/loss).
* **Output:** Model weight deltas, updated feature importance matrices, versioned model checkpoints.
* **Frequency:** Post-Match (Async Batch).
* **Examples:**  
  - `Movement_Loss_RMSE: 0.12m`  
  - `Intent_Accuracy: 84.5%`  
  - `Updated_Feature_Weight: Player_Panic_Threshold adjusted from 30% to 25%`  
  - `New_Checkpoint: xgboost_intent_v1.0.4.joblib`

---

### 14. Persistent Memory
* **Purpose:** Permanently store player profiles, Bayesian skill estimates, historical vector embeddings, and strategy confidence matrices across sessions.
* **Input:** Post-match learning evaluation and updated player embeddings.
* **Output:** Updated persistent storage files (`.faiss`, `.sqlite`, `.joblib`).
* **Frequency:** Post-Match / Cross-Session.
* **Examples:**  
  - `Player_Raja_Profile_Saved: Katana user, 218ms reaction avg, left-dodge bias (0.82)`  
  - `FAISS_Vector_Added: 512-dim embedding for Match #142`  
  - `DB_Record_Updated: Player combat encounters total = 14`
