"""Unit tests for CognitiveScheduler multi-frequency task scheduling."""

import pytest
from backend.cognitive_os.scheduler.scheduler import CognitiveScheduler


def test_scheduler_register_and_tick():
    scheduler = CognitiveScheduler()
    executed = []

    def task_60hz():
        executed.append("telemetry")

    def task_30hz():
        executed.append("attention")

    scheduler.register_task("telemetry", 60.0, task_60hz)   # interval: 1/60 ~ 0.01667s
    scheduler.register_task("attention", 30.0, task_30hz)   # interval: 1/30 ~ 0.03333s

    # T0: Initial tick at t=0.0
    ran = scheduler.tick(0.0)
    assert "telemetry" in ran
    assert "attention" in ran

    # T1: Tick at t=0.02 (20ms) -> only 60Hz task (telemetry) should run
    ran_t1 = scheduler.tick(0.02)
    assert "telemetry" in ran_t1
    assert "attention" not in ran_t1

    # T2: Tick at t=0.04 (40ms) -> both 60Hz and 30Hz tasks due
    ran_t2 = scheduler.tick(0.04)
    assert "telemetry" in ran_t2
    assert "attention" in ran_t2


def test_scheduler_unregister():
    scheduler = CognitiveScheduler()
    count = [0]

    def task():
        count[0] += 1

    scheduler.register_task("test_task", 10.0, task)
    scheduler.tick(0.0)
    assert count[0] == 1

    scheduler.unregister_task("test_task")
    scheduler.tick(1.0)
    assert count[0] == 1  # No further executions
