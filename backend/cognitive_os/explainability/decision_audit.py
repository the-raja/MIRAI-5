"""DecisionAuditEngine module.

Stores and indexes frame-by-frame ReasoningTraces for post-match audit inspection.
"""

from typing import List, Dict, Any, Optional
from backend.cognitive_os.explainability.reasoning_trace import ReasoningTrace


class DecisionAuditEngine:
    def __init__(self) -> None:
        self._audit_log: List[ReasoningTrace] = []

    def record_trace(self, trace: ReasoningTrace) -> None:
        """Stores frame reasoning trace into chronological audit log."""
        self._audit_log.append(trace)

    def get_trace_at_frame(self, frame_index: int) -> Optional[ReasoningTrace]:
        """Retrieves exact reasoning trace at target frame index."""
        for trace in self._audit_log:
            if trace.frame_index == frame_index:
                return trace
        return self._audit_log[-1] if self._audit_log else None

    def get_all_traces(self) -> List[ReasoningTrace]:
        return self._audit_log
