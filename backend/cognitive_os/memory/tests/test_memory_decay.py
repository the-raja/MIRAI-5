"""Unit tests for MemoryItem time decay calculation and cognitive forgetting."""

import pytest
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.memory.memory_buffer import MemoryBuffer
from backend.cognitive_os.memory.memory_manager import MemoryManager


def test_memory_decay_high_vs_low_importance():
    # Reload event (Importance 90) vs Low-priority event (Importance 30)
    high_imp = MemoryItem(id="m_high", timestamp=10.0, event_type="Reload", importance=90.0)
    low_imp = MemoryItem(id="m_low", timestamp=10.0, event_type="PlayerRunning", importance=30.0)

    # At t=10.0 (elapsed = 0s)
    assert high_imp.get_decayed_score(10.0) == 90.0
    assert low_imp.get_decayed_score(10.0) == 30.0

    # At t=13.0 (elapsed = 3s)
    # High importance decays slowly (e.g. ~86.0), Low importance decays faster (e.g. ~14.0)
    high_score_t3 = high_imp.get_decayed_score(13.0)
    low_score_t3 = low_imp.get_decayed_score(13.0)

    assert high_score_t3 > 80.0
    assert low_score_t3 < 20.0
    assert high_score_t3 > low_score_t3


def test_memory_buffer_decay_eviction():
    buffer = MemoryBuffer(max_items=100, max_retention_seconds=10.0, min_score_threshold=10.0)

    # Add low importance item (Importance 15) at t=10.0
    buffer.add_item(MemoryItem(id="m_weak", timestamp=10.0, event_type="LowSalience", importance=15.0))
    buffer.add_item(MemoryItem(id="m_strong", timestamp=10.0, event_type="BossHit", importance=95.0))

    # At t=14.0 (4 seconds later), m_weak decayed score drops below 10.0 -> evicted
    evicted = buffer.evict_expired(current_time=14.0)
    assert evicted >= 1
    remaining = [i.id for i in buffer.get_items()]
    assert "m_strong" in remaining
    assert "m_weak" not in remaining
