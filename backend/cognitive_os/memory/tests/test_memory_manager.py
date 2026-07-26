"""Unit tests for MemoryManager operations."""

import pytest
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


def test_memory_manager_insert_and_retrieve_highest_priority():
    manager = MemoryManager(max_items=100, max_retention_seconds=10.0)

    manager.insert_memory(MemoryItem(id="m1", timestamp=1.0, event_type="PlayerRunning", importance=20.0))
    manager.insert_memory(MemoryItem(id="m2", timestamp=1.1, event_type="PlayerReloading", importance=90.0))
    manager.insert_memory(MemoryItem(id="m3", timestamp=1.2, event_type="BossHit", importance=80.0))

    top_items = manager.retrieve_highest_priority(top_k=2)
    assert len(top_items) == 2
    assert top_items[0].event_type == "PlayerReloading"
    assert top_items[1].event_type == "BossHit"


def test_memory_manager_update_importance():
    manager = MemoryManager()
    manager.insert_memory(MemoryItem(id="m1", timestamp=1.0, event_type="PlayerRunning", importance=20.0))

    updated = manager.update_importance("m1", 95.0)
    assert updated is True

    top = manager.retrieve_highest_priority(top_k=1)
    assert top[0].importance == 95.0


def test_memory_manager_event_bus_integration():
    bus = EventBus()
    manager = MemoryManager(event_bus=bus)
    updates = []

    def on_memory_updated(event: Event):
        updates.append(event.payload)

    bus.subscribe("WORKING_MEMORY_UPDATED", on_memory_updated)

    manager.insert_memory(MemoryItem(id="m1", timestamp=1.0, event_type="TEST", importance=50.0))
    bus.dispatch()

    assert len(updates) == 1
    assert len(updates[0]) == 1
    assert updates[0][0].id == "m1"
