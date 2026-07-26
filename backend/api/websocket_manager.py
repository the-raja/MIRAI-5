"""WebSocketManager module.

Phase 0 Step 0.2: Real-time WebSocket event broadcaster streaming:
- Current HP
- Boss Action / Player Action
- Threat Update
- Prediction Update
- Emotion Update
- Memory Trigger
- Planner Change
"""

from typing import List, Dict, Any
import json
import asyncio


class WebSocketManager:
    def __init__(self) -> None:
        self.active_connections: List[Any] = []

    async def connect(self, websocket: Any) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: Any) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Broadcasts real-time JSON payload to all connected clients."""
        payload = json.dumps({"event_type": event_type, "data": data})
        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except Exception:
                pass

    def create_telemetry_event(
        self,
        player_hp: float,
        boss_hp: float,
        boss_action: str,
        player_action: str,
        threat_update: Dict[str, float],
        prediction_update: Dict[str, Any],
        emotion_update: str,
        memory_trigger: str,
        planner_change: str
    ) -> Dict[str, Any]:
        """Formats the canonical Step 0.2 WebSocket telemetry payload."""
        return {
            "player_hp": player_hp,
            "boss_hp": boss_hp,
            "boss_action": boss_action,
            "player_action": player_action,
            "threat_update": threat_update,
            "prediction_update": prediction_update,
            "emotion_update": emotion_update,
            "memory_trigger": memory_trigger,
            "planner_change": planner_change
        }
