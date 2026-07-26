"""Tick rate utilities for frequency-to-interval conversion."""

from typing import Optional
from pydantic import BaseModel


class TaskSchedule(BaseModel):
    name: str
    target_hz: float
    interval_seconds: float
    last_executed_time: Optional[float] = None
    execution_count: int = 0

    @classmethod
    def create(cls, name: str, target_hz: float) -> "TaskSchedule":
        interval = 1.0 / target_hz if target_hz > 0 else 0.0
        return cls(name=name, target_hz=target_hz, interval_seconds=interval)
