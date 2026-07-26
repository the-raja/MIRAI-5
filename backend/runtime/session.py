"""RuntimeSession module.

Manages active game sessions using MiraiRuntime.
"""

from typing import Dict, Any, Optional
from backend.runtime.runtime import MiraiRuntime


class RuntimeSession:
    def __init__(self, session_id: str = "sess_001") -> None:
        self.session_id = session_id
        self.runtime = MiraiRuntime(session_id=session_id)

    def observe(self, frame: Dict[str, Any]) -> None:
        self.runtime.observe(frame)

    def tick(self) -> str:
        return self.runtime.tick()

    def learn(self, result: Dict[str, Any]) -> Dict[str, Any]:
        return self.runtime.learn(result)
