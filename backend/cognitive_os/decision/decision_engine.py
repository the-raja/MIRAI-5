"""DecisionEngine module.

Coordinates GoalManager, PredictionEngine, and UtilitySystem to make explainable, 100% deterministic decisions.
Cascade:
Semantic Memory -> Prediction Engine -> Goal Manager -> Utility AI -> Decision
Publishes DECISION_MADE events onto the EventBus.
"""

from typing import List, Optional, Dict, Any
from backend.cognitive_os.decision.decision import Decision
from backend.cognitive_os.decision.goal import Goal
from backend.cognitive_os.decision.goal_manager import GoalManager
from backend.cognitive_os.decision.utility_action import UtilityAction, create_standard_action_set
from backend.cognitive_os.decision.utility_system import UtilitySystem, ScoredUtilityAction
from backend.cognitive_os.decision.reasoning_trace import ReasoningTraceModel
from backend.cognitive_os.prediction.prediction_engine import PredictionEngine
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class DecisionEngine:
    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.goal_manager = GoalManager(event_bus=event_bus)
        self.utility_system = UtilitySystem()
        self.prediction_engine = PredictionEngine(event_bus=event_bus)
        self.candidate_actions: List[UtilityAction] = create_standard_action_set()
        self.event_bus = event_bus

        if self.event_bus:
            self.event_bus.subscribe("WORLD_MODEL_UPDATED", self._on_world_model_updated)

    def _on_world_model_updated(self, event: Event) -> None:
        if isinstance(event.payload, WorldModel):
            pass

    def make_decision(
        self,
        world_model: WorldModel,
        memory_manager: Optional[MemoryManager] = None,
        semantic_manager: Optional[SemanticManager] = None,
        recent_actions: Optional[List[str]] = None
    ) -> Decision:
        """Processes Prediction Engine, Goal, World Model, Working Memory, and Semantic Memory to select optimal Action."""
        
        # 1. Generate Prediction via PredictionEngine
        prediction: Prediction = self.prediction_engine.generate_prediction(
            world_model=world_model,
            memory_manager=memory_manager,
            semantic_manager=semantic_manager,
            recent_actions=recent_actions
        )

        # 2. Determine active Goal (passing prediction)
        active_goal = self.goal_manager.evaluate_goal(
            world_model=world_model,
            memory_manager=memory_manager,
            semantic_manager=semantic_manager,
            prediction=prediction
        )

        # 3. Evaluate and score all candidate actions
        scored_actions = self.utility_system.evaluate_all_actions(
            candidate_actions=self.candidate_actions,
            active_goal=active_goal,
            world_model=world_model,
            memory_manager=memory_manager,
            semantic_manager=semantic_manager
        )

        # 4. Deterministic Sorting: Primary by final_score (descending), Secondary by action name (alphabetical)
        scored_actions.sort(key=lambda sa: (-sa.final_score, sa.action.name.lower()))

        # 5. Select winning action
        winning_scored = scored_actions[0] if scored_actions else ScoredUtilityAction(
            action=self.candidate_actions[-1], base_score=20.0, final_score=20.0
        )

        winning_action = winning_scored.action
        winning_action.last_used_timestamp = world_model.timestamp
        winning_action.target_entity_id = active_goal.id

        score_val = round(winning_scored.final_score, 1)
        conf_val = round(min(0.98, max(0.60, winning_scored.final_score / 100.0 * 0.90 if winning_scored.final_score > 1.0 else winning_scored.final_score * 0.90)), 2)

        # Build ReasoningTraceModel
        scores_map = {sa.action.name: round(sa.final_score, 1) for sa in scored_actions}
        reasons_list = [
            f"Prediction: Player will {prediction.action} ({int(prediction.confidence*100)}% conf from {prediction.source})",
            f"Goal Driver: {active_goal.reason}"
        ]
        if winning_scored.rationale:
            reasons_list.extend(winning_scored.rationale.split(" | "))

        trace = ReasoningTraceModel(
            goal=active_goal.type,
            candidate_actions=[sa.action.name for sa in scored_actions],
            scores=scores_map,
            winner=winning_action.name,
            reason_list=reasons_list,
            confidence=conf_val
        )

        decision = Decision(
            decision_id=f"dec_{int(world_model.timestamp*1000)}",
            timestamp=world_model.timestamp,
            goal=active_goal,
            chosen_action=winning_action,
            utility_score=score_val,
            confidence=conf_val,
            reasoning_trace=trace
        )

        if self.event_bus:
            event = Event(
                event_type="DECISION_MADE",
                timestamp=world_model.timestamp,
                source="DecisionEngine",
                payload=decision
            )
            self.event_bus.publish(event)

        return decision
