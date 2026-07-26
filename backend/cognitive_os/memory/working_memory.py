"""WorkingMemory state container module."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from backend.cognitive_os.memory.memory_item import MemoryItem


class WorkingMemoryState(BaseModel):
    timestamp: float = 0.0
    active_items: List[MemoryItem] = Field(default_factory=list)
    top_priority_item: Optional[MemoryItem] = None
    capacity_used: int = 0
    max_capacity: int = 100
