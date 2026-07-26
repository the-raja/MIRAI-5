"""MemoryManager module.

Manages Working Memory operations: insertion, expiration removal, importance updates,
cognitive queries, and cognitive score decay prioritization.
Contains NO ML — pure working memory query engine.
"""

from typing import List, Optional, Dict, Any
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.memory.memory_buffer import MemoryBuffer
from backend.cognitive_os.attention.salience import AttentionState
from backend.cognitive_os.perception.observation import ObservationSet
from backend.cognitive_os.telemetry.telemetry_frame import Vector3Data
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class MemoryManager:
    def __init__(self, max_items: int = 100, max_retention_seconds: float = 10.0, event_bus: Optional[EventBus] = None) -> None:
        self.buffer = MemoryBuffer(max_items=max_items, max_retention_seconds=max_retention_seconds)
        self.event_bus = event_bus

        if self.event_bus:
            self.event_bus.subscribe("OBSERVATION_SET", self._on_observation_set)
            self.event_bus.subscribe("ATTENTION_STATE", self._on_attention_state)

    def _on_observation_set(self, event: Event) -> None:
        """Automatically converts every observation in ObservationSet into a Working Memory item."""
        if isinstance(event.payload, ObservationSet):
            obs_set: ObservationSet = event.payload
            for obs in obs_set.observations:
                item = MemoryItem(
                    id=f"mem_obs_{obs.type}_{int(obs.timestamp*1000)}",
                    timestamp=obs.timestamp,
                    event_type=obs.type,
                    confidence=obs.confidence,
                    importance=50.0,
                    related_entity=obs.source,
                    metadata=obs.metadata
                )
                self.buffer.add_item(item)

            for flag_name, is_active in obs_set.flags.items():
                if is_active:
                    flag_item = MemoryItem(
                        id=f"mem_flag_{flag_name}_{int(obs_set.timestamp*1000)}",
                        timestamp=obs_set.timestamp,
                        event_type=flag_name,
                        importance=60.0,
                        metadata={"flag": flag_name}
                    )
                    self.buffer.add_item(flag_item)

            if self.event_bus:
                self._publish_memory_update(obs_set.timestamp)

    def _on_attention_state(self, event: Event) -> None:
        """Updates working memory importance scores based on Attention Engine saliency prioritization."""
        if isinstance(event.payload, AttentionState):
            att: AttentionState = event.payload
            for ev in att.salient_events:
                clean_type = ev.event_id.replace("evt_", "")
                matched = False
                for item in self.buffer.get_items():
                    if item.event_type == clean_type:
                        item.importance = max(item.importance, ev.saliency_score)
                        matched = True

                if not matched:
                    item = MemoryItem(
                        id=f"mem_att_{clean_type}_{int(ev.timestamp*1000)}",
                        timestamp=ev.timestamp,
                        event_type=clean_type,
                        importance=ev.saliency_score,
                        related_entity=att.primary_target_id,
                        metadata=ev.metadata
                    )
                    self.buffer.add_item(item)

            if self.event_bus:
                self._publish_memory_update(att.timestamp)

    def insert_memory(self, item: MemoryItem) -> None:
        """Insert a new MemoryItem into Working Memory."""
        self.buffer.add_item(item)
        if self.event_bus:
            self._publish_memory_update(item.timestamp)

    def remove_expired(self, current_time: float) -> int:
        """Remove memories older than the retention window or whose decayed score drops below threshold."""
        evicted = self.buffer.evict_expired(current_time=current_time)
        if evicted > 0 and self.event_bus:
            self._publish_memory_update(current_time)
        return evicted

    def update_importance(self, memory_id: str, new_importance: float) -> bool:
        """Update the importance score of an existing memory item by ID."""
        for item in self.buffer.get_items():
            if item.id == memory_id:
                item.importance = new_importance
                return True
        return False

    def retrieve_recent(self, time_window_seconds: float = 10.0, current_time: Optional[float] = None) -> List[MemoryItem]:
        """Retrieve memories within the last N seconds."""
        return self.buffer.get_recent_memories(time_window_seconds=time_window_seconds, current_time=current_time)

    def retrieve_highest_priority(self, top_k: int = 5, current_time: Optional[float] = None) -> List[MemoryItem]:
        """Retrieve top-K memories sorted descending by current decayed importance score."""
        items = self.buffer.get_items()
        if not items:
            return []

        ref_time = current_time if current_time is not None else items[-1].timestamp
        sorted_items = sorted(items, key=lambda m: m.get_decayed_score(ref_time), reverse=True)
        return sorted_items[:top_k]

    def query_memories_by_type(self, event_type: str) -> List[MemoryItem]:
        """Filter working memories by event_type label."""
        return [m for m in self.buffer.get_items() if m.event_type == event_type]

    # --- Cognitive Queries for Prediction Engine ---

    def time_since_event(self, event_type: str, current_time: float) -> Optional[float]:
        """Returns seconds elapsed since the last occurrence of event_type, or None if not found."""
        last_event = self.get_last_event(event_type)
        if last_event:
            return round(current_time - last_event.timestamp, 3)
        return None

    def get_last_event(self, event_type: str) -> Optional[MemoryItem]:
        """Returns the most recent MemoryItem matching event_type."""
        for item in reversed(self.buffer.get_items()):
            if item.event_type == event_type:
                return item
        return None

    def last_seen_position(self, entity_id: str) -> Optional[Vector3Data]:
        """Returns the last recorded spatial position for entity_id in working memory."""
        for item in reversed(self.buffer.get_items()):
            if item.related_entity == entity_id and item.position is not None:
                return item.position
        return None

    def count_events_in_window(self, event_type: str, time_window_seconds: float = 5.0, current_time: Optional[float] = None) -> int:
        """Returns the count of matching event_type occurrences within the specified time window."""
        recent_items = self.retrieve_recent(time_window_seconds=time_window_seconds, current_time=current_time)
        return sum(1 for item in recent_items if item.event_type == event_type)

    def _publish_memory_update(self, timestamp: float) -> None:
        if self.event_bus:
            event = Event(
                event_type="WORKING_MEMORY_UPDATED",
                timestamp=timestamp,
                source="MemoryManager",
                payload=self.buffer.get_items()
            )
            self.event_bus.publish(event)
