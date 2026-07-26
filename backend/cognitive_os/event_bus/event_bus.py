"""Event Bus module acting as the central nervous system of the Cognitive OS.

Decouples all modules by allowing publish-subscribe event queuing and dispatching with fault isolation.
"""

from typing import Dict, List, Callable, Any
from collections import deque
import logging
from backend.cognitive_os.event_bus.events import Event

logger = logging.getLogger("EventBus")


class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}
        self._event_queue: deque[Event] = deque()

    def subscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """Subscribe a callback function to a specific event_type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """Unsubscribe a callback function from a specific event_type."""
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)

    def publish(self, event: Event) -> None:
        """Publish an event onto the event queue for dispatching."""
        self._event_queue.append(event)

    def dispatch(self) -> int:
        """Dispatch all queued events to their respective subscribers.
        
        Fault isolation: If any subscriber raises an exception, it is caught
        and logged without breaking execution for remaining subscribers.
        
        Returns the total number of events dispatched in this call.
        """
        dispatched_count = 0
        while self._event_queue:
            event = self._event_queue.popleft()
            dispatched_count += 1
            callbacks = list(self._subscribers.get(event.event_type, []))
            for callback in callbacks:
                try:
                    callback(event)
                except Exception as err:
                    logger.error(f"Error in subscriber callback for '{event.event_type}': {err}")
        return dispatched_count
