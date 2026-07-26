# MIRAI v2 — Research & Experimentation Log

## Project Roadmap & Coding Milestones

---

### [Phase 0] Architecture & Repository Initialization
- **Date:** 2026-07-26
- **Status:** Complete
- **Milestones:**
  - Repository structure created (`backend/`, `frontend/`, `docs/`, `research/`, `configs/`, `benchmarks/`).
  - Git initialized with strict `.gitignore` rules.
  - Virtual environment `.venv` initialized with specified ML/DL/API dependencies.
  - Core thesis documentation initialized under `docs/`.
  - Cognitive OS 14-stage pipeline architecture frozen.
  - Formal Module Specifications (Purpose, Input, Output, Frequency) established for all 14 modules.

---

### [Milestone 1] The First Breath — Sensing & Perception Pipeline
- **Status:** Pending Architectural Definition Completion
- **Scope:**
  $$\text{Telemetry} \longrightarrow \text{Perception} \longrightarrow \text{Attention} \longrightarrow \text{World Model}$$
- **Objective:**
  Build and verify the first executable sub-pipeline of the Cognitive OS.
  1. Ingest raw game telemetry frames (`TelemetryFrame`).
  2. Compute normalized observation states and feature deltas (`ObservationState`).
  3. Filter cognitive noise and isolate high-salience tactical events (`SalientEvents` & `PriorityTargets`).
  4. Construct real-time spatial connectivity and line-of-sight graphs (`WorldGraph`).
- **Non-Goals:**
  - NO monolithic `main.py`, `app.py`, `game.py`, or `boss.py` scripts.
  - NO decision, planning, or movement execution until Milestone 1 is 100% verified with unit tests.
