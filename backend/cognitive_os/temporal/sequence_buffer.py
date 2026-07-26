"""SequenceBuffer module.

Maintains a rolling temporal history buffer of the last N (default: 20) player actions.
Serves as input features for temporal sequence models (Markov, LSTM, Transformer).
"""

from typing import List, Dict, Any, Optional
from collections import deque
import time


class SequenceBuffer:
    def __init__(self, max_length: int = 20) -> None:
        self.max_length = max_length
        self._buffer: deque = deque(maxlen=max_length)
        self._timestamps: deque = deque(maxlen=max_length)

    def push_action(self, action: str, timestamp: float = 0.0) -> None:
        """Pushes a new action into the rolling temporal buffer."""
        if not action:
            return
        c_time = timestamp if timestamp > 0.0 else time.time()
        self._buffer.append(action)
        self._timestamps.append(c_time)

    def get_sequence(self, length: Optional[int] = None) -> List[str]:
        """Returns the current sequence of recent actions up to specified length."""
        seq = list(self._buffer)
        if length is not None and length > 0:
            return seq[-length:]
        return seq

    def get_sliding_windows(self, window_size: int = 5) -> List[List[str]]:
        """Extracts sliding windows of size window_size over the stored sequence."""
        seq = list(self._buffer)
        if len(seq) < window_size:
            return [seq] if seq else []

        windows = []
        for i in range(len(seq) - window_size + 1):
            windows.append(seq[i : i + window_size])
        return windows

    def clear(self) -> None:
        """Clears the sequence buffer."""
        self._buffer.clear()
        self._timestamps.clear()

    def size(self) -> int:
        """Returns current count of stored actions."""
        return len(self._buffer)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes current buffer state."""
        return {
            "max_length": self.max_length,
            "current_size": len(self._buffer),
            "sequence": list(self._buffer),
            "timestamps": list(self._timestamps)
        }
