"""MIRAI Python SDK.

Stable SDK interface encapsulating MIRAI Cognitive OS into a clean 3-step loop:
    runtime = MiraiSDK()
    runtime.observe(game_state)
    action = runtime.tick()
    runtime.learn(match_result)
"""

from typing import Dict, Any, Optional
from backend.runtime.runtime import MiraiRuntime


class MiraiSDK:
    def __init__(self, session_id: str = "default_sdk_session") -> None:
        self._runtime = MiraiRuntime(session_id=session_id)

    def observe(self, game_state: Dict[str, Any]) -> None:
        """Ingests raw game engine state observation."""
        self._runtime.observe(game_state)

    def tick(self, frame: Optional[Dict[str, Any]] = None) -> str:
        """Executes single-function cognitive tick returning chosen combat action."""
        return self._runtime.tick(frame)

    def learn(self, match_result: Dict[str, Any]) -> Dict[str, Any]:
        """Ingests match outcome results for online learning."""
        return self._runtime.learn(match_result)
