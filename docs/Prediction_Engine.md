# MIRAI v2 — Prediction Engine Specification

> **Phase 7 Specification & Deliverable Documentation**  
> "Machine Learning should answer one question only: What will probably happen next? Not what should I do. Decision-making is solved by the Decision Cortex. Now we improve it with Prediction."

---

## 1. Purpose & Core Vision
The **Prediction Engine** is MIRAI's first ML module. It forecasts future player actions (`Reload`, `Dodge`, `Heal`, `Attack`, `Retreat`, `Block`) before they occur. By establishing a statistical non-ML `BaselinePredictor` (Markov transition frequencies & sequence rules), MIRAI sets a rigorous benchmark for evaluating future XGBoost, LightGBM, and PyTorch DL models.

---

## 2. System Architecture Diagram

```mermaid
graph LR
    SEM[Semantic Memory] --> FE[Feature Extractor]
    FE --> FV[Feature Vector]
    FV --> BP[Baseline Predictor]
    BP --> PRED[Prediction]
    PRED --> GM[Goal Manager]
    GM --> GOAL[Active Goal]
    GOAL --> US[Utility System]
    US --> DEC[Decision]
    PRED --> PE[Prediction Evaluator]
```

---

## 3. Class Diagram & Relationship Hierarchy

```mermaid
classDiagram
    class Prediction {
        +String prediction_id
        +Float timestamp
        +String action
        +Float confidence
        +Float time_horizon
        +String reason
        +String source
        +Dict metadata
    }

    class IPredictor {
        <<interface>>
        +predict(List~String~, MemoryManager, SemanticManager) Prediction
    }

    class BaselinePredictor {
        +Dict transition_table
        +predict(List~String~, MemoryManager, SemanticManager) Prediction
    }

    class FeatureVector {
        +Float distance
        +Float player_hp
        +Float boss_hp
        +String weapon
        +Float stamina
        +Dict cooldowns
        +String current_action
        +List~String~ last_5_actions
        +Float aggression_score
        +Int reload_count
        +String preferred_dodge
        +String preferred_weapon
        +Float time_since_last_heal
        +to_dict() Dict
        +to_numpy_array() ndarray
    }

    class FeatureExtractor {
        +extract_features(TelemetryFrame, WorldModel, MemoryManager, SemanticManager) FeatureVector
    }

    class DatasetBuilder {
        +build_dataset_from_episode(Episode) List~Dict~
        +save_dataset_to_csv(List~Dict~, String) String
        +load_dataset_from_csv(String) List~Dict~
    }

    class EvaluationMetrics {
        +Int total_samples
        +Int correct_predictions
        +Float accuracy
        +Dict precision
        +Dict recall
        +Dict confusion_matrix
    }

    class PredictionEvaluator {
        +record_outcome(String, String)
        +compute_metrics() EvaluationMetrics
        +format_report() String
    }

    IPredictor <|.. BaselinePredictor
    BaselinePredictor .. Prediction
    FeatureExtractor .. FeatureVector
    PredictionEvaluator .. EvaluationMetrics
```

---

## 4. 13 ML Features Specification & Dataset Generation

`FeatureExtractor` converts active Game State into structured tabular feature vectors for ML training:

| Feature Column | Type | Example |
| :--- | :--- | :--- |
| `distance` | `float` | `10.0m` |
| `player_hp` | `float` | `85.0` |
| `boss_hp` | `float` | `75.0` |
| `weapon` | `str` | `"Shotgun"` |
| `stamina` | `float` | `90.0` |
| `cooldowns` | `Dict` | `{"HeavyAttack": 0.0}` |
| `current_action` | `str` | `"RELOAD"` |
| `last_5_actions` | `List[str]` | `["Attack", "Attack", "Attack", "Reload"]` |
| `aggression_score` | `float` | `0.85` |
| `reload_count` | `int` | `15` |
| `preferred_dodge` | `str` | `"Left"` |
| `preferred_weapon` | `str` | `"Shotgun"` |
| `time_since_last_heal` | `float` | `42.5s` |

`DatasetBuilder` generates supervised learning CSV datasets inside `backend/data/datasets/training_dataset.csv` with target labels (`y = target_next_action`).

---

## 5. ML Evaluation Report Format

```text
=============================================
PREDICTION ENGINE ML EVALUATION REPORT
=============================================
Total Samples Tested: 10
Overall Accuracy:     80.0%

Per-Action Precision & Recall
-----------------------------
Dodge          | Precision:  80.0% | Recall:  80.0%
Reload         | Precision:  80.0% | Recall:  80.0%

Confusion Matrix (Rows: Actual, Cols: Predicted)
------------------------------------------------
Actual Reload     -> [Reload:4, Dodge:1]
Actual Dodge      -> [Reload:1, Dodge:4]
=============================================
```

---

## 6. Updated System Roadmap

- **Phase 1** ✅ Cognitive Kernel (`v0.1-cognitive-kernel`)
- **Phase 2** ✅ Working Memory (`v0.2-working-memory`)
- **Phase 3** ✅ Episodic Memory (`v0.3-episodic-memory`)
- **Phase 4** ✅ Semantic Memory (`v0.4-semantic-memory`)
- **Phase 5** ✅ Decision Cortex (`v0.5-decision-cortex`)
- **Phase 6** ✅ Prediction Engine (`v0.6-prediction-engine`)
- **Phase 7** 🔄 Continuous Learning & Retraining (XGBoost / PyTorch)
- **Phase 8** 🔄 Vector Memory (FAISS + HNSW)
- **Phase 9** 🔄 LLM Cognitive Layer
- **Phase 10** 🔄 Team Intelligence
- **Phase 11** 🔄 Full Game Integration
