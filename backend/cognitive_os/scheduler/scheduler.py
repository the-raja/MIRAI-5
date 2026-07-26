"""Cognitive OS multi-rate scheduler.

Manages multi-frequency task registration (e.g. 60Hz, 30Hz, 20Hz, 10Hz) and triggers task callbacks when due based on elapsed time deltas.
"""

from typing import Dict, Callable, List
from backend.cognitive_os.scheduler.tick_rate import TaskSchedule


class CognitiveScheduler:
    def __init__(self) -> None:
        self._schedules: Dict[str, TaskSchedule] = {}
        self._callbacks: Dict[str, Callable[[], None]] = {}

    def register_task(self, name: str, target_hz: float, callback: Callable[[], None]) -> None:
        """Register a named task to run at target_hz frequency."""
        schedule = TaskSchedule.create(name=name, target_hz=target_hz)
        self._schedules[name] = schedule
        self._callbacks[name] = callback

    def unregister_task(self, name: str) -> None:
        """Unregister a task by name."""
        self._schedules.pop(name, None)
        self._callbacks.pop(name, None)

    def tick(self, current_time: float) -> List[str]:
        """Evaluate registered tasks against current_time and execute those due.
        
        Returns a list of task names executed during this tick.
        """
        executed_tasks: List[str] = []

        for name, schedule in self._schedules.items():
            if schedule.last_executed_time is None:
                is_due = True
            else:
                elapsed = current_time - schedule.last_executed_time
                is_due = elapsed >= schedule.interval_seconds - 1e-6  # small epsilon for float precision

            if is_due:
                callback = self._callbacks.get(name)
                if callback:
                    callback()
                    schedule.last_executed_time = current_time
                    schedule.execution_count += 1
                    executed_tasks.append(name)

        return executed_tasks
