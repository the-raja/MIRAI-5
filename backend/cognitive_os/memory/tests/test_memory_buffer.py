"""Unit tests for MemoryBuffer capacity and expiration eviction."""

import pytest
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.memory.memory_buffer import MemoryBuffer


def test_memory_buffer_capacity_eviction():
    buffer = MemoryBuffer(max_items=3, max_retention_seconds=10.0)

    for i in range(5):
        buffer.add_item(MemoryItem(id=f"m_{i}", timestamp=1.0, event_type="TEST"))

    # Should cap at 3 items: m_2, m_3, m_4
    assert buffer.count() == 3
    items = buffer.get_items()
    assert items[0].id == "m_2"
    assert items[-1].id == "m_4"


def test_memory_buffer_time_expiration_eviction():
    buffer = MemoryBuffer(max_items=100, max_retention_seconds=5.0)

    buffer.add_item(MemoryItem(id="m_old", timestamp=1.0, event_type="OLD_EVENT"))
    buffer.add_item(MemoryItem(id="m_mid", timestamp=4.0, event_type="MID_EVENT"))
    
    # Add item at t=7.0 -> cutoff is 7.0 - 5.0 = 2.0. m_old (t=1.0) should be evicted.
    buffer.add_item(MemoryItem(id="m_new", timestamp=7.0, event_type="NEW_EVENT"))

    assert buffer.count() == 2
    items = buffer.get_items()
    assert [i.id for i in items] == ["m_mid", "m_new"]


def test_memory_buffer_get_recent_memories():
    buffer = MemoryBuffer(max_items=100, max_retention_seconds=10.0)

    buffer.add_item(MemoryItem(id="m1", timestamp=1.0, event_type="EVENT_1"))
    buffer.add_item(MemoryItem(id="m2", timestamp=5.0, event_type="EVENT_2"))
    buffer.add_item(MemoryItem(id="m3", timestamp=6.0, event_type="EVENT_3"))

    # Get memories in last 2 seconds relative to t=6.0 -> m2 (5.0) and m3 (6.0)
    recent = buffer.get_recent_memories(time_window_seconds=2.0, current_time=6.0)
    assert len(recent) == 2
    assert [i.id for i in recent] == ["m2", "m3"]
