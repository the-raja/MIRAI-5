# MIRAI v2 — Cognitive Memory Architecture (Four Pillars)

> **Memory System Specification:**  
> Human cognition relies on distinct memory stores operating across different temporal and functional boundaries. MIRAI incorporates four specialized memory systems to separate transient real-time combat context from long-term domain knowledge, episodic history, and motor execution.

---

## 1. Working Memory (Short-Term / Transient Context)

### Definition
The active, short-term cognitive buffer that holds real-time combat information required for immediate decision-making during the current frame/tick.

### Characteristics
- **Lifetime:** Transient (cleared or continuously overwritten during combat).
- **Scope:** Current combat scene.
- **Speed:** Instantaneous ($<0.1\text{ms}$ in-memory read/write).

### Contains
- **Current Active Target:** Entity ID of targeted opponent (`Medic_01`).
- **Current Active Goal:** Active objective (`Eliminate_Medic`).
- **Recent Observations:** Last observed reload timestamp, last dodge direction.
- **Active Danger Zones:** Immediate projectile trajectories, active area-of-effect hazards.
- **Temporary Hypotheses:** "Player is out of stamina" or "Medic is attempting a revive".

---

## 2. Episodic Memory (Experience & History Store)

### Definition
The long-term storage of specific past combat encounters, historical battles, critical events, and counter-strategy outcomes.

### Characteristics
- **Lifetime:** Permanent across sessions.
- **Scope:** Cross-match history.
- **Speed:** Fast vector similarity lookup ($<1\text{ms}$).

### Contains
- **Past Fight Records:** High-dimensional embedding vectors of historical encounters.
- **Strategy Outcomes:** Records of which counter-strategies succeeded or failed against specific player combat styles.
- **Player Encounters Log:** Historic performance profiles against specific players over days, weeks, or months.

---

## 3. Semantic Memory (Domain Knowledge & Rules)

### Definition
The static and semi-static structured knowledge base defining domain rules, game mechanics, weapon stats, map layout attributes, and ability cooldowns.

### Characteristics
- **Lifetime:** Static / Declarative (updated via patch notes or game configuration).
- **Scope:** Global game universe.
- **Speed:** Instantaneous lookup (dictionary / graph query).

### Contains
- **Weapons Data:** Damage stats, attack range, magazine sizes, reload durations.
- **Abilities & Cooldowns:** Ability cast times, cooldown timers, mana/stamina costs.
- **Map Geometry:** Static cover node positions, choke point coordinates, spawn locations.
- **Game Rules:** Damage multiplier formulas, status effect durations, line-of-sight obstruction rules.

---

## 4. Procedural Memory (Motor & Sequence Execution)

### Definition
The learned motor routines, combo execution sequences, and low-level physical combat behaviors.

### Characteristics
- **Lifetime:** Long-term / Evolving.
- **Scope:** Kinematic execution.
- **Speed:** Deterministic tick execution.

### Contains
- **Combat Combo Chains:** Pre-learned physical attack combinations (e.g. `Light_Slash` $\rightarrow$ `Heavy_Strike` $\rightarrow$ `Backdash`).
- **Kinematic Steering Sequences:** Motor maneuvering routines for dodging, flanking, and taking cover.
- **Animation Timing Windows:** Exact frame alignments for parry windows, invincibility frames, and recovery states.
