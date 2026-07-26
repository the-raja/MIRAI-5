# MIRAI v2 — Screen Design Specification (Screens 1 - 10)

> **UI/UX Screen Blueprint Document**  
> "Defines exact visual content, wireframes, and interactive components for all 10 screens."

---

## Screen 1: Splash Screen
```text
████████████████████████████████████
              MIRAI
        "I've been waiting."

            [ ENTER ]
████████████████████████████████████
```
* **Content:** Glowing 3D brain icon, title heading, tagline, and `ENTER` button.
* **Component:** `SplashScreen.tsx`

---

## Screen 2: Identity Setup
```text
====================================
         IDENTIFY YOURSELF
  Enter your Combat Designation

  ______________________________

           [ CONTINUE ]
====================================
```
* **Content:** Operator name input field, designation validator, and proceed action button.
* **Component:** `NameEntryScreen.tsx`

---

## Screen 3: Command Center (Home Base)
```text
====================================
         COMMAND CENTER
  Operator: Raja

  [ PLAY BATTLE ]        [ BRAIN ARCHIVE ]
  [ REPLAY VIEWER ]      [ STATISTICS ]
====================================
```
* **Content:** 4 primary command cards launching combat, cognitive graph, replay debugger, and empirical benchmarks.
* **Component:** `HomeScreen.tsx`

---

## Screen 4: Agent Selection
```text
====================================
         AGENT SELECTION
  [3D Hero Viewer]  | Abilities
                    | Voice: Tactical
  Cyber Knight      | Ultimate: Overload
  Shadow Ninja      | Description
====================================
```
* **Content:** Hero selector, 3D model viewer, ability metrics, voice profile, and team lock button.
* **Component:** `HeroSelectScreen.tsx`

---

## Screen 5: Strategy Planning
```text
====================================
        STRATEGY PLANNING
  Configure Tactical Directive

  ⚡ Aggression     🛡️ Protect
  🏹 Kiting         🎯 Focus
====================================
```
* **Content:** Tactical stance options with detailed descriptions of how MIRAI will counter each stance.
* **Component:** `StrategyScreen.tsx`

---

## Screen 6: MIRAI Analysis
```text
====================================
         MIRAI ANALYSIS
  🔍 Scanning Team...
  🧠 Processing Intent Prediction...
  💾 Loading Vector Memory (Ep 102)...
====================================
```
* **Content:** Dynamic radar scanning animation, vector memory lookup log, and counter plan building progress bar.
* **Component:** `AnalysisScreen.tsx`

---

## Screen 7: Battle Arena
```text
====================================
           3D COMBAT ARENA
  [Boss HP: 85]      [Player HP: 60]
  ----------------------------------
  [ 3D R3F Canvas ]  | Live AI Panel
                     | 🔮 Pred: Reload
                     | 📜 Plan: Dash
====================================
```
* **Content:** 3D React Three Fiber arena canvas, dual health bars, and real-time "Watch AI Think" reasoning panel.
* **Component:** `BattleScreen.tsx`

---

## Screen 8: Brain View
```text
====================================
     BRAIN ARCHIVE & GRAPH
  [Perception] ➔ [Memory] ➔ [Prediction]
  [Threat]     ➔ [Planner] ➔ [Decision]
====================================
```
* **Content:** Interactive subsystem flow graph with live latency and state telemetry. Activatable globally via `TAB` key overlay (`BrainOverlay.tsx`).
* **Component:** `BrainViewScreen.tsx` & `BrainOverlay.tsx`

---

## Screen 9: Replay Viewer
```text
====================================
     REPLAY VIEWER & DEBUGGER
  Scrubber: [======|=======] Frame 130
  Memory: Ep 102 | Threat: 0.91
====================================
```
* **Content:** Match timeline slider restoring timestamped cognitive states at any frame index.
* **Component:** `ReplayScreen.tsx`

---

## Screen 10: Learning Screen
```text
====================================
     CONTINUOUS ONLINE LEARNING
  ✓ Battle Finished
  ✓ Episode Saved to Vector Storage
  ✓ Planner Task Network Adjusted
  ✓ Brain Checkpoint Saved (v3.2)
====================================
```
* **Content:** 6-stage post-match online learning sequence and empirical benchmark metrics.
* **Component:** `LearningScreen.tsx`
