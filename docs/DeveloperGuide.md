# MIRAI v2 — Developer Guide & Plugin Development

## 1. Quick Start & Installation

```bash
# 1. Clone repository
git clone https://github.com/the-raja/MIRAI-5.git
cd MIRAI-5

# 2. Setup python virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run test suite
pytest backend/
```

---

## 2. How to Add Custom ML Models

1. Inherit from `BaseModelInterface` in `backend/cognitive_os/ml/models/`.
2. Implement `train()`, `predict()`, `save()`, `load()`.
3. Register model name inside `ModelRegistry`.

---

## 3. How to Write a Custom Plugin

Implement the swappable plugin interface:

```python
from plugins.prediction.prediction_plugins import BasePredictionPlugin

class CustomTransformerPlugin(BasePredictionPlugin):
    def predict(self, situation):
        return {"action": "Counter", "confidence": 0.98, "plugin": "CustomTransformer"}
```

---

## 4. Contributing Guidelines
* Ensure 100% of unit tests pass (`pytest backend/`).
* Maintain docstrings and preserve API contracts.
* Include Mermaid diagrams in any new documentation files.
