"""Phase 3 Working Memory Milestone Unit Tests.

Explicitly verifies the 5 core working memory contracts:
1. Insert memory
2. Retrieve memory
3. Expire memory after timeout
4. Importance decays over time
5. Highest-priority memory is returned correctly
"""

import pytest
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.memory.memory_buffer import MemoryBuffer
from backend.cognitive_os.memory.memory_manager import MemoryManager


def test_1_insert_memory():
    """Case 1: Insert memory into Working Memory."""
    manager = MemoryManager(max_items=100)
    item = MemoryItem(id="m_insert_1", timestamp=10.0, event_type="PlayerReloading", importance=90.0)

    manager.insert_memory(item)
    memories = manager.retrieve_recent(current_time=10.0)

    assert len(memories) == 1
    assert memories[0].id == "m_insert_1"
    assert memories[0].event_type == "PlayerReloading"


def test_2_retrieve_memory():
    """Case 2: Retrieve memory by event type and recent time window."""
    manager = MemoryManager()
    manager.insert_memory(MemoryItem(id="m1", timestamp=10.0, event_type="PlayerReloading"))
    manager.insert_memory(MemoryItem(id="m2", timestamp=12.0, event_type="BossHit"))

    retrieved = manager.query_memories_by_type("PlayerReloading")
    assert len(retrieved) == 1
    assert retrieved[0].id == "m1"

    last_event = manager.get_last_event("BossHit")
    assert last_event is not None
    assert last_event.id == "m2"


def test_3_expire_memory_after_timeout():
    """Case 3: Expire memory after retention timeout (10 seconds)."""
    buffer = MemoryBuffer(max_items=100, max_retention_seconds=10.0)

    buffer.add_item(MemoryItem(id="m_old", timestamp=1.0, event_type="OldEvent"))
    buffer.add_item(MemoryItem(id="m_recent", timestamp=9.0, event_type="RecentEvent"))

    # At t=11.5 -> cutoff is 11.5 - 10.0 = 1.5. m_old (t=1.0) must expire.
    evicted = buffer.evict_expired(current_time=11.5)
    assert evicted == 1
    remaining = [m.id for m in buffer.get_items()]
    assert "m_old" not in remaining
    assert "m_recent" in remaining


def test_4_importance_decays_over_time():
    """Case 4: Importance decays over time based on initial importance."""
    item_high = MemoryItem(id="m_high", timestamp=10.0, event_type="BossDamaged", importance=100.0)
    item_mid = MemoryItem(id="m_mid", timestamp=10.0, event_type="PlayerReloading", importance=90.0)
    item_low = MemoryItem(id="m_low", timestamp=10.0, event_type="PlayerRunning", importance=30.0)

    # Initial scores at t=10.0
    assert item_high.get_decayed_score(10.0) == 100.0
    assert item_mid.get_decayed_score(10.0) == 90.0
    assert item_low.get_decayed_score(10.0) == 30.0

    # Decayed scores at t=13.0 (3 seconds later)
    high_score = item_high.get_decayed_score(13.0)
    mid_score = item_mid.get_decayed_score(13.0)
    low_score = item_low.get_decayed_score(13.0)

    # High importance decays slowly; low importance decays rapidly
    assert high_score > mid_score
    assert mid_score > low_score
    assert low_score < 20.0


def test_5_highest_priority_memory_returned_correctly():
    """Case 5: Highest-priority memory is returned correctly accounting for decay."""
    manager = MemoryManager()

    # m_recent_mid (t=10.0, importance 80.0) vs m_old_low (t=5.0, importance 40.0) vs m_top (t=10.0, importance 95.0)
    manager.insert_memory(MemoryItem(id="m_low", timestamp=5.0, event_type="PlayerRunning", importance=40.0))
    manager.insert_memory(MemoryItem(id="m_mid", timestamp=10.0, event_type="BossDamaged", importance=80.0))
    manager.insert_memory(MemoryItem(id="m_top", timestamp=10.0, event_type="PlayerReloading", importance=95.0))

    top_items = manager.retrieve_highest_priority(top_k=2, current_time=10.0)
    assert len(top_items) == 2
    assert top_items[0].id == "m_top"
    assert top_items[1].id == "m_mid"
