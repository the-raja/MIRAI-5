"""MemoryBuffer module.

Implements a bounded sliding window memory buffer (max 100 items, max 10 seconds retention)
with cognitive importance decay eviction.
"""

from typing import List, Optional
from collections import deque
from backend.cognitive_os.memory.memory_item import MemoryItem


class MemoryBuffer:
    def __init__(self, max_items: int = 100, max_retention_seconds: float = 10.0, min_score_threshold: float = 5.0) -> None:
        self.max_items = max_items
        self.max_retention_seconds = max_retention_seconds
        self.min_score_threshold = min_score_threshold
        self._buffer: deque[MemoryItem] = deque()

    def add_item(self, item: MemoryItem) -> None:
        """Add a new MemoryItem to the buffer. Evicts oldest item if max_items capacity is reached."""
        self._buffer.append(item)
        while len(self._buffer) > self.max_items:
            self._buffer.popleft()
        self.evict_expired(current_time=item.timestamp)

    def evict_expired(self, current_time: float) -> int:
        """Evict all memories older than max_retention_seconds OR whose decayed score drops below threshold."""
        evicted_count = 0
        cutoff_time = current_time - self.max_retention_seconds
        remaining: deque[MemoryItem] = deque()

        for item in self._buffer:
            decayed_score = item.get_decayed_score(current_time)
            is_time_expired = item.timestamp < cutoff_time
            is_score_expired = decayed_score <= self.min_score_threshold

            if is_time_expired or is_score_expired:
                evicted_count += 1
            else:
                remaining.append(item)

        self._buffer = remaining
        return evicted_count

    def get_recent_memories(self, time_window_seconds: Optional[float] = None, current_time: Optional[float] = None) -> List[MemoryItem]:
        """Return memories within the specified time_window_seconds relative to current_time."""
        if not self._buffer:
            return []

        ref_time = current_time if current_time is not None else self._buffer[-1].timestamp
        if time_window_seconds is None:
            return list(self._buffer)

        cutoff = ref_time - time_window_seconds
        return [item for item in self._buffer if item.timestamp >= cutoff]

    def get_items(self) -> List[MemoryItem]:
        """Return all active memory items in the buffer."""
        return list(self._buffer)

    def count(self) -> int:
        """Return total active items in buffer."""
        return len(self._buffer)

    def clear(self) -> None:
        """Clear all active items."""
        self._buffer.clear()
