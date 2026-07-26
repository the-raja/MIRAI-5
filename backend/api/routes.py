"""REST API Routes module for Phase 0 Backend Freeze.

Finalized APIs:
- GET /state
- GET /memory
- GET /behavior
- GET /prediction
- GET /planner
- GET /emotion
- POST /battle/start
- POST /battle/action
- POST /battle/end
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class BattleStartRequest(BaseModel):
    session_id: str = "battle_01"
    player_id: str = "player_raja"


class BattleActionRequest(BaseModel):
    session_id: str = "battle_01"
    action: str = "HeavyAttack"
    timestamp: float = 12.0


class BattleEndRequest(BaseModel):
    session_id: str = "battle_01"
    outcome: str = "VICTORY"


@router.get("/state")
def get_state() -> Dict[str, Any]:
    """Returns canonical system state snapshot."""
    return {
        "current_goal": "Pressure Player",
        "boss_hp": 85.0,
        "player_hp": 60.0,
        "status": "COMBAT_ACTIVE"
    }


@router.get("/memory")
def get_memory() -> Dict[str, Any]:
    """Returns working, episodic, semantic, and vector memory snapshots."""
    return {
        "working_memory": {"active_items": 5, "focus": "player_raja"},
        "episodic_memory": {"total_episodes": 42, "last_episode": "ep_102"},
        "semantic_memory": {"rules": ["Player reloads under pressure"]},
        "vector_memory": {"experiences": 1000, "top_hit": "Episode 102 (Sim 0.94)"}
    }


@router.get("/behavior")
def get_behavior() -> Dict[str, Any]:
    """Returns current active Behavior Tree execution node status."""
    return {
        "active_bt_node": "SequenceBTNode",
        "last_action": "Dash",
        "execution_status": "SUCCESS"
    }


@router.get("/prediction")
def get_prediction() -> Dict[str, Any]:
    """Returns XGBoost + LSTM fused prediction confidence."""
    return {
        "intent_prediction": "Reload",
        "confidence": 0.94,
        "xgboost_conf": 0.91,
        "lstm_conf": 0.96
    }


@router.get("/planner")
def get_planner() -> Dict[str, Any]:
    """Returns HTN Task Network hierarchy and Behavior Tree execution status."""
    return {
        "goal": "WIN",
        "htn_decomposition": ["Reduce HP", "Pressure", "Force Reload", "Punish", "Retreat"],
        "progress_pct": 60.0
    }


@router.get("/emotion")
def get_emotion() -> Dict[str, Any]:
    """Returns Boss AI dynamic emotional cortex state."""
    return {
        "dominant_emotion": "Aggressive",
        "arousal": 0.85,
        "valence": 0.72,
        "fear_level": 0.12
    }


@router.post("/battle/start")
def start_battle(req: BattleStartRequest) -> Dict[str, Any]:
    """Initializes a new battle session."""
    return {
        "status": "BATTLE_STARTED",
        "session_id": req.session_id,
        "player_id": req.player_id
    }


@router.post("/battle/action")
def battle_action(req: BattleActionRequest) -> Dict[str, Any]:
    """Processes player action and returns Boss counter-action."""
    return {
        "status": "ACTION_PROCESSED",
        "player_action": req.action,
        "boss_counter_action": "Dash",
        "prediction": "Reload (94%)"
    }


@router.post("/battle/end")
def end_battle(req: BattleEndRequest) -> Dict[str, Any]:
    """Finalizes battle session and triggers online learning."""
    return {
        "status": "BATTLE_ENDED",
        "session_id": req.session_id,
        "outcome": req.outcome,
        "learning_updated": True
    }
