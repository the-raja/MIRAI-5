"""Pygame Integration Plugin for MIRAI."""

from typing import Dict, Any
from sdk.python.mirai_sdk import MiraiSDK


class PygameMiraiController:
    def __init__(self) -> None:
        self.sdk = MiraiSDK(session_id="pygame_boss_session")

    def update_frame(self, pygame_player_pos: tuple, player_hp: float) -> str:
        frame = {
            "visible_entities": ["player_01"],
            "metadata": {
                "player_hp": player_hp,
                "distance": float(pygame_player_pos[0]) / 10.0
            }
        }
        self.sdk.observe(frame)
        return self.sdk.tick()
