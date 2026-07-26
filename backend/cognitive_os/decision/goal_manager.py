"""GoalManager module.

Decides WHAT high-level goal MIRAI should pursue based on WorldModel, WorkingMemory, SemanticMemory, and Prediction:
Rules:
- Prediction (Player will Reload, conf >= 70%) -> PRESSURE
- Boss HP < 20% -> HEAL
- Player Low HP < 25% -> FINISH
- Player Reloading -> PRESSURE
- Player Hidden -> SEARCH

Contains NO ML—pure explainable rule-based goal selection.
"""

from typing import Optional, List, Dict, Any
from backend.cognitive_os.decision.goal import Goal
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class GoalManager:
    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.event_bus = event_bus
        self.active_goal: Goal = Goal(id="g_init", type="OBSERVE", priority=0.5, reason="Baseline observation")

        if self.event_bus:
            self.event_bus.subscribe("WORLD_MODEL_UPDATED", self._on_world_model_updated)

    def _on_world_model_updated(self, event: Event) -> None:
        if isinstance(event.payload, WorldModel):
            pass

    def evaluate_goal(
        self,
        world_model: WorldModel,
        memory_manager: Optional[MemoryManager] = None,
        semantic_manager: Optional[SemanticManager] = None,
        prediction: Optional[Prediction] = None
    ) -> Goal:
        """Evaluates inputs including predictions and returns the highest priority active Goal."""
        target_id = world_model.visible_entities[0] if world_model.visible_entities else "player_raja_01"
        time_since_reload = memory_manager.time_since_event("PlayerReloading", current_time=world_model.timestamp) if memory_manager else None

        wm_meta = getattr(world_model, "metadata", {}) or {}
        boss_hp_pct = wm_meta.get("boss_hp_pct", 1.0)
        player_hp_pct = wm_meta.get("player_hp_pct", 1.0)
        is_player_hidden = not world_model.visible_entities

        # 1. Rule: Prediction Engine predicts Player will Reload (conf >= 0.70) -> PRESSURE
        if prediction and prediction.action == "Reload" and prediction.confidence >= 0.70:
            goal = Goal(
                id=f"g_{int(world_model.timestamp*1000)}",
                type="PRESSURE",
                priority=94.0,
                reason=f"Prediction Engine ({prediction.source}): Player predicted to Reload ({int(prediction.confidence*100)}% conf).",
                created_at=world_model.timestamp
            )
        # 2. Rule: Boss HP < 20% -> HEAL
        elif boss_hp_pct < 0.20:
            goal = Goal(
                id=f"g_{int(world_model.timestamp*1000)}",
                type="HEAL",
                priority=95.0,
                reason="Boss health critical (<20%). Need recovery.",
                created_at=world_model.timestamp
            )
        # 3. Rule: Player Low HP (<25%) -> FINISH
        elif player_hp_pct < 0.25:
            goal = Goal(
                id=f"g_{int(world_model.timestamp*1000)}",
                type="FINISH",
                priority=93.0,
                reason="Player health low (<25%). Execute finish sequence.",
                created_at=world_model.timestamp
            )
        # 4. Rule: Player Reloading -> PRESSURE
        elif time_since_reload is not None and time_since_reload < 3.0:
            goal = Goal(
                id=f"g_{int(world_model.timestamp*1000)}",
                type="PRESSURE",
                priority=91.0,
                reason="Player reloading detected in Working Memory.",
                created_at=world_model.timestamp
            )
        # 5. Rule: Player Hidden -> SEARCH
        elif is_player_hidden:
            goal = Goal(
                id=f"g_{int(world_model.timestamp*1000)}",
                type="SEARCH",
                priority=85.0,
                reason="Player hidden / line of sight lost.",
                created_at=world_model.timestamp
            )
        # 6. Default -> ATTACK
        else:
            goal = Goal(
                id=f"g_{int(world_model.timestamp*1000)}",
                type="ATTACK",
                priority=70.0,
                reason="Standard tactical engage.",
                created_at=world_model.timestamp
            )

        self.active_goal = goal

        if self.event_bus:
            event = Event(
                event_type="GOAL_ACTIVATED",
                timestamp=world_model.timestamp,
                source="GoalManager",
                payload=goal
            )
            self.event_bus.publish(event)

        return goal
