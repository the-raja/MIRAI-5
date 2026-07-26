# MIRAI v2 — Execution & Planning Engine

## 1. Hybrid Planning Architecture
- **Hierarchical Task Network (HTN):** Decomposes complex strategic objectives (e.g. `Execute_Flank_And_Isolate`) into ordered sub-tasks.
- **Behavior Tree (BT):** Handles real-time, tick-by-tick combat execution, state checks, and interrupt handling.

## 2. Motor Planning & Interface
Translates high-level planned sub-tasks into physical boss movements, rotation angles, attack triggers, and defensive maneuvers.
