# MIRAI v2 — Cognitive OS Architecture (FROZEN SPECIFICATION)

> **Architectural Freeze Notice:**  
> The 14-stage cognitive pipeline documented herein is **FROZEN**. All future development, modular implementations, abstractions, and tests MUST strictly adhere to this exact control flow.

---

## 1. Frozen 14-Stage Cognitive Pipeline

```
                       ┌─────────────────────────┐
                       │         PLAYER          │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │        TELEMETRY        │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │       PERCEPTION        │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │        ATTENTION        │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │       WORLD MODEL       │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │         MEMORY          │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │       PREDICTION        │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │      GOAL MANAGER       │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │       UTILITY AI        │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │         PLANNER         │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │      MOTOR PLANNER      │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │       GAME ENGINE       │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │        LEARNING         │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │    PERSISTENT MEMORY    │
                       └─────────────────────────┘
```

---

## 2. Formal Module Specifications

### Module 1: Player
- **Purpose:** Provide external real-time combat actions, inputs, and behavior patterns.
- **Input:** Human inputs (mouse, keyboard, controller) or Bot AI decision cycles.
- **Output:** Raw character state (movement commands, attack triggers, item usage).
- **Frequency:** Continuous / Event-driven.

---

### Module 2: Telemetry
- **Purpose:** Ingest, record, and timestamp raw combat state streams from the game session.
- **Input:** Raw game state (positions $(x, y, z)$, velocity vectors, HP, stamina, ammo, equipped gear, combat events).
- **Output:** Timestamped Raw Telemetry Frames (`TelemetryFrame`).
- **Frequency:** 60 Hz.

---

### Module 3: Perception
- **Purpose:** Observe world state and transform raw telemetry into normalized feature vectors.
- **Input:** `TelemetryFrame` stream.
- **Output:** Cleaned `ObservationState` (normalized spatial distances, movement deltas, health percentages, reload counters, stance).
- **Frequency:** 60 Hz.

---

### Module 4: Attention
- **Purpose:** Prioritize observations, isolate critical tactical triggers, and filter cognitive noise.
- **Input:** `ObservationState`.
- **Output:** `SalientEvents` & `PriorityTargets` (highlighted high-threat actors, critical low-HP allies/enemies, impending attacks).
- **Frequency:** 60 Hz (or event-triggered on state changes).

---

### Module 5: World Model
- **Purpose:** Maintain spatial, topological, and visibility graph relationships of the battle arena.
- **Input:** `ObservationState`, `SalientEvents`, and spatial map grid.
- **Output:** `WorldGraph` (nodes: cover locations, combatants, choke points; edges: line-of-sight, distance, accessibility, threat zones).
- **Frequency:** 30 Hz.

---

### Module 6: Memory (Episodic Retrieval)
- **Purpose:** Query historical encounter database to retrieve relevant past experiences and successful counter-strategies.
- **Input:** Current `ObservationState` embedding vector.
- **Output:** `RetrievedMemories` (Top-$K$ similar historical encounters, strategy confidence scores, past player failure/success logs).
- **Frequency:** 10 Hz / Event-driven (triggered on engagement or tactical phase changes).

---

### Module 7: Prediction
- **Purpose:** Forecast short-term player movements, immediate actions/intents, and multi-agent squad threat rankings.
- **Input:** Sequence of `ObservationState` (history buffer), `WorldGraph`, and `RetrievedMemories`.
- **Output:** `PredictionBundle`:
  - **Movement:** Trajectory sequence $(x_{t+1}, y_{t+1}, \dots, x_{t+n}, y_{t+n})$.
  - **Intent:** Probabilities over actions (`Reload`, `Heal`, `Attack`, `Parry`, `Retreat`).
  - **Threat Ranking:** Ranked list of target entities with threat weights.
- **Frequency:** 20 Hz (Movement) / 10 Hz (Intent & Threat).

---

### Module 8: Goal Manager
- **Purpose:** Select high-level strategic objectives based on tactical priorities, world topology, and predictions.
- **Input:** `PredictionBundle`, `WorldGraph`, `SalientEvents`.
- **Output:** Active `StrategicGoal` (e.g., `Eliminate_Medic`, `Retreat_To_Cover`, `Flank_Ranger`, `Observe_Pattern`, `Defend_Position`).
- **Frequency:** 5 Hz / Event-triggered on major combat shifts.

---

### Module 9: Utility AI
- **Purpose:** Evaluate and score candidate action options against goal constraints, memory weights, and utility curves to pick the optimal tactical action.
- **Input:** Active `StrategicGoal`, `PredictionBundle`, `WorldGraph`, `RetrievedMemories`.
- **Output:** `ScoredActionPlan` + `ExplainabilityAudit` (chosen action, score array, feature weightings, exact rationale).
- **Frequency:** 10 Hz.

---

### Module 10: Planner
- **Purpose:** Decompose chosen action plan into long-term task sequences (HTN) and tick-by-tick state execution trees (Behavior Tree).
- **Input:** `ScoredActionPlan`.
- **Output:** `ExecutableTaskSequence` (ordered sub-tasks: `ApproachCover` $\rightarrow$ `CastShield` $\rightarrow$ `FireBurst`).
- **Frequency:** 30 Hz.

---

### Module 11: Motor Planner
- **Purpose:** Convert abstract tactical sub-tasks into precise kinematic movement vectors, rotation angles, attack timing, and input triggers.
- **Input:** `ExecutableTaskSequence`, current boss kinematic state.
- **Output:** `MotorCommand` (steering vector, target rotation, trigger commands, animation cues).
- **Frequency:** 60 Hz.

---

### Module 12: Game Engine
- **Purpose:** Simulate or execute boss motor commands in the game environment, resolve physics/collisions, and generate updated combat state.
- **Input:** `MotorCommand`.
- **Output:** Updated match simulation state, hit registrations, environment deltas.
- **Frequency:** 60 Hz (Game loop).

---

### Module 13: Learning
- **Purpose:** Evaluate post-match performance, compute prediction loss metrics (RMSE, Accuracy), and update internal model parameters.
- **Input:** Complete match telemetry log, prediction logs, victory/defeat outcome.
- **Output:** Model parameter updates, model version checkpoints, feature importance updates.
- **Frequency:** Post-Match (Async Batch).

---

### Module 14: Persistent Memory
- **Purpose:** Permanently store player profiles, Bayesian skill estimates, historical vector embeddings, and strategy confidence matrices across sessions.
- **Input:** Post-match learning evaluation and updated player embeddings.
- **Output:** Updated persistent storage state (FAISS indexes, SQLite/DB player records, model weights).
- **Frequency:** Post-Match / Cross-Session.
