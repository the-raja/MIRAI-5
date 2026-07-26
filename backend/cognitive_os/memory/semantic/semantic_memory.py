"""SemanticMemory module.

Stores distilled domain Knowledge items (habits, profiles, preference rules).
Contains NO raw memories or frame clutter—only high-confidence distilled knowledge.
"""

from typing import Dict, List, Optional
from backend.cognitive_os.memory.semantic.knowledge import Knowledge


class SemanticMemory:
    def __init__(self) -> None:
        self._knowledge_store: Dict[str, Knowledge] = {}

    def upsert_knowledge(self, knowledge: Knowledge) -> None:
        """Adds or updates distilled knowledge in Semantic Memory."""
        existing = self._knowledge_store.get(knowledge.id)
        if existing:
            # Increment evidence count and update confidence
            knowledge.evidence_count = max(knowledge.evidence_count, existing.evidence_count + 1)
            knowledge.confidence = min(0.99, round(max(existing.confidence, knowledge.confidence) + 0.02, 2))
        self._knowledge_store[knowledge.id] = knowledge

    def get_knowledge_by_type(self, type_name: str) -> Optional[Knowledge]:
        """Returns Knowledge matching type_name or None if not found."""
        for item in self._knowledge_store.values():
            if item.type == type_name:
                return item
        return None

    def get_high_confidence_knowledge(self, min_confidence: float = 0.80) -> List[Knowledge]:
        """Returns all knowledge items meeting or exceeding min_confidence threshold."""
        return [k for k in self._knowledge_store.values() if k.confidence >= min_confidence]

    def get_all_knowledge(self) -> List[Knowledge]:
        """Returns all distilled knowledge items currently stored."""
        return list(self._knowledge_store.values())

    def count(self) -> int:
        """Returns count of stored knowledge items."""
        return len(self._knowledge_store)
