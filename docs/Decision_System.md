# MIRAI v2 — Decision System & Utility AI

## 1. Decision Pipeline
1. **Goal Manager (Symbolic AI):** Maintains high-level strategic goals (e.g. `Eliminate_Medic`, `Retreat_To_Cover`, `Pressure_Ranger`).
2. **Utility AI Scoring:** Scores every candidate action based on current state, memory context, and threat levels.
3. **Explainability Engine:** Logs precise weightings, parameters, and decision criteria for every chosen action.

## 2. Explainability Schema
Every decision outputs structured diagnostic telemetry:
```json
{
  "timestamp": "2026-07-26T16:24:00Z",
  "chosen_action": "Target_Medic_Flank",
  "utility_score": 0.89,
  "rationale": {
    "target": "Medic_Bot_01",
    "medic_hp_pct": 0.35,
    "team_survivability_impact": "CRITICAL",
    "distance": 8.5
  }
}
```
