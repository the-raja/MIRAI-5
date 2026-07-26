# MIRAI v2 — Post-Match Learning & Empirical Metrics (FROZEN SPECIFICATION)

> **Learning & Benchmarking Specification:**  
> "The boss never resets. The boss grows."  
> Learning in MIRAI is defined by precise, concrete post-match updates and quantitative benchmarks. If an improvement cannot be empirically measured, it cannot be claimed.

---

## 1. Concrete Post-Match Updates (Task 6)

When an encounter concludes, MIRAI executes a deterministic 7-step post-match learning pipeline.

```
       1. Update Player Profile (Bayesian Statistics & Style)
                                │
                                ▼
       2. Store Episodic Memory (512-dim Embedding Vector)
                                │
                                ▼
       3. Update Prediction Models (Incremental Retraining / Fine-Tuning)
                                │
                                ▼
       4. Adjust Utility Weights (Reward/Penalty Feedback)
                                │
                                ▼
       5. Record Successful Counter-Strategies (Counter Matrix)
                                │
                                ▼
       6. Update Model Confidence Values (Bayesian Belief Updates)
                                │
                                ▼
       7. Save Battle Summary & Telemetry Log (Persistence)
```

### Step 1: Update Player Profile
- **Bayesian Skill Updating:** Adjusts player reaction time estimates, aim accuracy, dodge direction bias, and reload interval distributions.
- **Combat Style Re-Classification:** Re-evaluates player archetype (e.g. `Aggressive_Counter_Fighter`, `Passive_Sniper`, `Panic_Dodger`).

### Step 2: Store Episodic Memory
- **Vector Embedding Generation:** Encodes match state trajectory into a 512-dimensional vector.
- **FAISS Index Write:** Inserts new vector with metadata (Match ID, Player ID, Outcome, Strategy Efficacy) into the HNSW graph index.

### Step 3: Update Prediction Models
- **Intent Classifier Update:** Appends match tabular state logs to training buffer and runs incremental gradient boosting step (XGBoost/LightGBM).
- **Movement Trajectory Fine-Tuning:** Evaluates spatial deviation and updates sequence model weights (LSTM/Transformer).

### Step 4: Adjust Utility Weights
- **Reinforcement Feedback Loop:** Increases utility weights for actions that yielded high damage/control ratios and penalizes actions that led to boss damage/whiffs.

### Step 5: Record Successful Counter-Strategies
- **Counter Matrix Entry:** Stores specific counter-actions that proved effective against detected player habits (e.g. `Dodge_Left_Bias` $\rightarrow$ `Right_Sweep_Attack`).

### Step 6: Update Model Confidence Values
- **Uncertainty Adjustment:** Increases model confidence ($[0.0 \to 1.0]$) for recognized player patterns; lowers confidence when player changes habits.

### Step 7: Save Battle Summary & Telemetry Log
- **Persistent Storage Write:** Writes detailed JSON battle summary and updates `.sqlite` database records and model checkpoint artifacts.

---

## 2. Measurable Success Metrics (Task 7)

To prove MIRAI is genuinely evolving rather than pretending to learn, every training phase is benchmarked against 7 quantitative metrics.

| Metric | Target / Benchmark Unit | Measurement Method |
| :--- | :--- | :--- |
| **1. Trajectory Prediction Accuracy** | **$\text{RMSE} < 0.15\text{m}$** at $t+0.5\text{s}$ | Euclidian spatial error between predicted trajectory and actual player position. |
| **2. Intent Prediction Accuracy** | **$> 85\%$ Accuracy** | Multiclass classification accuracy over player actions (`HEAL`, `RELOAD`, `PARRY`, etc.). |
| **3. Counter Success Rate** | **$> 75\%$ Effective Counters** | Percentage of executed counter-actions that successfully land or force player retreat. |
| **4. Average Decision Latency** | **$< 2.0\text{ms}$** per decision cycle | Execution time from Perception output to Utility AI action selection. |
| **5. Memory Retrieval Latency** | **$< 1.0\text{ms}$** FAISS HNSW query | Time taken to query 10,000+ historical memory vectors. |
| **6. Adaptation Speed** | **$\le 3$ Encounters** | Number of matches required to detect and counter a repeated player exploit/habit. |
| **7. Win/Loss Trend vs. Fixed Strategy** | **Steeper Defeat-to-Victory Curve** | Win-rate progression when a player uses the exact same attack pattern repeatedly. |

---

## 3. Empirical Verification Principle

> **Rule of Verification:**  
> No model update or learning code is declared successful unless it demonstrates a statistically significant improvement in at least one of the 7 core metrics above without regressing decision latency.
