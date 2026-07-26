# MIRAI v2 — Execution Frequencies & Cognitive Rationale

> **Cognitive Frequency Specification:**  
> Biological cognitive systems operate at multi-tiered time scales. High-level reasoning does not occur at the same frequency as motor reflexes or sensor sampling. Running every module at 60 Hz wastes computational resources, creates chaotic oscillations, and produces robotic behavior. MIRAI uses a staggered multi-rate execution architecture to achieve human-like cognitive pacing.

---

## 1. Master Frequency Table

| Module | Update Frequency | Execution Type | Rationale / Cognitive Justification |
| :--- | :--- | :--- | :--- |
| **Telemetry Collector** | **60 Hz** | Synchronous | Collect raw physical game state every frame without missing state deltas. |
| **Perception Engine** | **60 Hz** | Synchronous | Immediately normalize features so motor reflexes and collision responses react quickly. |
| **Attention Engine** | **30 Hz** | Sub-sampled | Human cognitive focus does not reprioritize targets every single frame (prevents target jitter). |
| **World Model** | **30 Hz** | Sub-sampled | Arena spatial topology and cover status remain stable over micro-intervals. |
| **Prediction Engine** | **20 Hz** | Asynchronous | Future trajectory forecasting ($t+0.5\text{s}$) and intent models only need periodic updates. |
| **Utility AI** | **20 Hz** | Asynchronous | Action candidate scoring needs to evaluate choices smoothly without re-scoring 60 times/sec. |
| **Goal Manager** | **10 Hz** | Strategic Event | Macro objectives (e.g. `Eliminate_Medic`) persist across combat phases and change infrequently. |
| **HTN Planner** | **5 – 10 Hz** | Strategic Batch | Multi-step task decomposition executes over long time horizons. |
| **Dialogue Engine (LLM)**| **Event-Driven** | Asynchronous | Dialogue generation triggers only when meaningful events occur (taunts, phase shifts). |
| **Learning Engine** | **End of Encounter**| Async Batch | Model retraining and weight adjustments occur offline after combat terminates. |
| **Persistent Memory** | **Cross-Session** | Storage Write | FAISS index writes and database updates persist post-encounter. |

---

## 2. Multi-Rate Architecture Benefits

### 1. Elimination of Decision Oscillation ("Jitter")
If high-level Goal Selection and Utility Scoring ran at 60 Hz, minor frame-to-frame noise in player position could cause MIRAI to swap targets 60 times per second. By locking Goals to 10 Hz and Attention to 30 Hz, MIRAI exhibits purposeful, committed behavior.

### 2. Computational Efficiency & Real-Time Performance
Heavy ML inference (e.g. LSTM trajectory prediction, XGBoost intent classification, FAISS vector lookups) is decoupled from the 60 Hz render loop. Prediction runs asynchronously at 20 Hz, consuming <15% of the frame budget.

### 3. Human Cognitive Alignment
- **Reflexes (Perception & Motor):** 60 Hz (~16.6ms resolution).
- **Focus & Spatial Beliefs (Attention & World Model):** 30 Hz (~33.3ms resolution).
- **Evaluations & Intent (Utility & Prediction):** 20 Hz (~50ms resolution).
- **Macro Planning (Goals & HTN):** 5–10 Hz (~100–200ms resolution).
