"""Unit tests for MemoryManager cognitive queries:

time_since_event, last_seen_position, count_events_in_window, get_last_event
"""

import pytest
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.telemetry.telemetry_frame import Vector3Data


def test_memory_queries_time_since_event():
    manager = MemoryManager()
    manager.insert_memory(MemoryItem(id="m1", timestamp=10.0, event_type="PlayerReloading"))
    manager.insert_memory(MemoryItem(id="m2", timestamp=11.5, event_type="BossHit"))

    # Query time since PlayerReloading at t=14.7 -> 14.7 - 10.0 = 4.7s
    elapsed = manager.time_since_event("PlayerReloading", current_time=14.7)
    assert elapsed == 4.7

    # Query time since BossHit at t=14.7 -> 14.7 - 11.5 = 3.2s
    elapsed_hit = manager.time_since_event("BossHit", current_time=14.7)
    assert elapsed_hit == 3.2

    # Query non-existent event -> None
    assert manager.time_since_event("NonExistent", current_time=14.7) is None


def test_memory_queries_last_seen_position():
    manager = MemoryManager()
    pos1 = Vector3Data(x=12.3, y=0.0, z=6.1)
    pos2 = Vector3Data(x=14.0, y=0.0, z=8.0)

    manager.insert_memory(MemoryItem(id="m1", timestamp=1.0, event_type="PlayerSeen", related_entity="player_raja", position=pos1))
    manager.insert_memory(MemoryItem(id="m2", timestamp=3.0, event_type="PlayerSeen", related_entity="player_raja", position=pos2))

    last_pos = manager.last_seen_position("player_raja")
    assert last_pos is not None
    assert last_pos.x == 14.0
    assert last_pos.z == 8.0


def test_memory_queries_count_events_in_window():
    manager = MemoryManager()

    # Insert 4 attack events within t=5.0 to t=9.0
    manager.insert_memory(MemoryItem(id="m1", timestamp=1.0, event_type="PlayerAttacking")) # outside 5s window at t=10.0
    manager.insert_memory(MemoryItem(id="m2", timestamp=6.0, event_type="PlayerAttacking"))
    manager.insert_memory(MemoryItem(id="m3", timestamp=7.0, event_type="PlayerAttacking"))
    manager.insert_memory(MemoryItem(id="m4", timestamp=8.0, event_type="PlayerAttacking"))
    manager.insert_memory(MemoryItem(id="m5", timestamp=9.0, event_type="PlayerAttacking"))

    # Count attacks in last 5 seconds at t=10.0 -> window cutoff is 5.0 -> m2, m3, m4, m5 = 4 attacks
    count = manager.count_events_in_window("PlayerAttacking", time_window_seconds=5.0, current_time=10.0)
    assert count == 4
