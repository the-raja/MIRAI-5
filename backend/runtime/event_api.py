"""EventAPI module.

Game engines emit high-level combat events (PlayerMoved, PlayerAttacked, PlayerReloaded, BossDamaged).
MIRAI automatically listens and reacts without manual component calls.
"""

from typing import Dict, Any, Optional
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class EventAPI:
    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.event_bus = event_bus or EventBus()
        self._setup_event_listeners()

    def _setup_event_listeners(self) -> None:
        """Subscribes internal handlers to game engine events."""
        self.event_bus.subscribe("PlayerMoved", lambda evt: None)
        self.event_bus.subscribe("PlayerAttacked", lambda evt: None)
        self.event_bus.subscribe("PlayerReloaded", lambda evt: None)
        self.event_bus.subscribe("BossDamaged", lambda evt: None)

    def emit_event(self, event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        """Emits a game event to which MIRAI's Cognitive OS automatically reacts."""
        data = payload or {}
        event = Event(event_type=event_type, data=data)
        self.event_bus.publish(event)
        self.event_bus.dispatch()
