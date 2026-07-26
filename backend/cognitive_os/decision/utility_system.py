"""UtilitySystem module.

The heart of MIRAI decision-making. Calculates explainable utility scores for all action candidates:
Final Score = Base Score + Reload Bonus + Range Bonus + Goal Bonus + Boss HP Modifier + Cooldown Penalty

Contains NO ML—pure transparent, deterministic scoring.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.cognitive_os.decision.utility_action import UtilityAction
from backend.cognitive_os.decision.goal import Goal
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager


class ScoredUtilityAction(BaseModel):
    action: UtilityAction
    base_score: float
    context_score: float = 0.0
    reload_bonus: float = 0.0
    range_bonus: float = 0.0
    boss_low_hp_modifier: float = 0.0
    cooldown_penalty: float = 0.0
    final_score: float = 0.0
    rationale: str = ""


class UtilitySystem:
    def score_action(
        self,
        action: UtilityAction,
        active_goal: Goal,
        world_model: WorldModel,
        memory_manager: Optional[MemoryManager] = None,
        semantic_manager: Optional[SemanticManager] = None
    ) -> ScoredUtilityAction:
        """Scores a single candidate UtilityAction against goal, context, knowledge, and memory."""
        current_time = world_model.timestamp
        base = action.base_score * 100.0 if action.base_score <= 1.0 else action.base_score
        context_score = 0.0
        reload_bonus = 0.0
        range_bonus = 0.0
        boss_low_hp_modifier = 0.0
        cooldown_penalty = 0.0
        reasons: List[str] = []

        # 1. Cooldown Penalty
        if action.is_on_cooldown(current_time):
            cooldown_penalty = 200.0
            reasons.append("Action is on cooldown")

        # 2. Check Working Memory (Player Reloading)
        time_since_reload = memory_manager.time_since_event("PlayerReloading", current_time=current_time) if memory_manager else None
        is_player_reloading = time_since_reload is not None and time_since_reload < 3.0

        if is_player_reloading:
            if action.name in ("HeavyAttack", "LightAttack"):
                reload_bonus = 25.0
                reasons.append("Player Reloading (+25)")
            elif action.name == "Heal":
                reload_bonus = -15.0
                reasons.append("Player Reloading penalty for Heal (-15)")

        # 3. Check Range & Distance (Optimal Range / Enemy Far)
        player_pos = world_model.estimated_player_positions.get("player_raja_01")
        is_enemy_far = not player_pos or player_pos.x > 8.0
        if action.name in ("HeavyAttack", "LightAttack") and not is_enemy_far:
            range_bonus = 15.0
            reasons.append("Optimal Range (+15)")
        elif action.name == "Heal" and is_enemy_far:
            range_bonus = 20.0
            reasons.append("Enemy Far (+20)")

        # 4. Check Boss HP Modifier
        wm_meta = getattr(world_model, "metadata", {}) or {}
        boss_hp_pct = wm_meta.get("boss_hp_pct", 1.0)
        if boss_hp_pct < 0.20:
            if action.name == "Heal":
                boss_low_hp_modifier = 50.0
                reasons.append("Boss HP Low (+50)")
            elif action.name == "HeavyAttack":
                boss_low_hp_modifier = -30.0
                reasons.append("Low Boss HP penalty for Heavy Attack (-30)")

        # 5. Goal Alignment Bonus
        if active_goal.type in ("PRESSURE", "ATTACK", "FINISH") and action.name in ("HeavyAttack", "LightAttack"):
            context_score = 15.0
            reasons.append(f"Goal Alignment: {active_goal.type} (+15)")
        elif active_goal.type == "HEAL" and action.name == "Heal":
            context_score = 25.0
            reasons.append(f"Goal Alignment: {active_goal.type} (+25)")

        # Final Score Calculation
        final_score = base + context_score + reload_bonus + range_bonus + boss_low_hp_modifier - cooldown_penalty
        final_score = max(0.0, round(final_score, 1))

        rationale_str = " | ".join(reasons) if reasons else "Default base scoring"

        return ScoredUtilityAction(
            action=action,
            base_score=round(base, 1),
            context_score=context_score,
            reload_bonus=reload_bonus,
            range_bonus=range_bonus,
            boss_low_hp_modifier=boss_low_hp_modifier,
            cooldown_penalty=cooldown_penalty,
            final_score=final_score,
            rationale=rationale_str
        )

    def evaluate_all_actions(
        self,
        candidate_actions: List[UtilityAction],
        active_goal: Goal,
        world_model: WorldModel,
        memory_manager: Optional[MemoryManager] = None,
        semantic_manager: Optional[SemanticManager] = None
    ) -> List[ScoredUtilityAction]:
        """Evaluates all candidate actions and returns them sorted descending by final_score."""
        scored: List[ScoredUtilityAction] = []
        for action in candidate_actions:
            s = self.score_action(
                action=action,
                active_goal=active_goal,
                world_model=world_model,
                memory_manager=memory_manager,
                semantic_manager=semantic_manager
            )
            scored.append(s)

        scored.sort(key=lambda sa: sa.final_score, reverse=True)
        return scored
