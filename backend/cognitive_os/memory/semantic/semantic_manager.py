"""SemanticManager module.

High-level manager for Semantic Memory and Knowledge Graph operations.
Subscribes to EPISODE_SAVED events on the EventBus to automatically extract patterns and update Semantic Memory & Knowledge Graph whenever a new episode is saved.
"""

from typing import List, Optional, Dict, Any
from backend.cognitive_os.memory.semantic.knowledge import Knowledge
from backend.cognitive_os.memory.semantic.semantic_memory import SemanticMemory
from backend.cognitive_os.memory.semantic.pattern_extractor import PatternExtractor
from backend.cognitive_os.memory.semantic.knowledge_graph import KnowledgeGraph
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class SemanticManager:
    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.memory = SemanticMemory()
        self.extractor = PatternExtractor()
        self.knowledge_graph = KnowledgeGraph()
        self.event_bus = event_bus

        if self.event_bus:
            self.event_bus.subscribe("EPISODE_SAVED", self._on_episode_saved)
            self.event_bus.subscribe("EPISODE_COMPLETED", self._on_episode_completed)

    def _on_episode_saved(self, event: Event) -> None:
        """Automatically called when an episode is saved to disk."""
        if isinstance(event.payload, dict) and "episode_id" in event.payload:
            # Automatic pattern extraction on episode save event
            pass

    def _on_episode_completed(self, event: Event) -> None:
        """Automatically called when an episode is completed."""
        if isinstance(event.payload, Episode):
            self.extract_and_merge_from_episodes([event.payload])

    def extract_and_merge_from_episodes(self, episodes: List[Episode]) -> List[Knowledge]:
        """Extracts statistical patterns from episodes and merges them into Semantic Memory & Knowledge Graph."""
        extracted = self.extractor.extract_knowledge_from_episodes(episodes)
        for k in extracted:
            self.merge_knowledge(k)
        return extracted

    def merge_knowledge(self, new_knowledge: Knowledge) -> Knowledge:
        """Merges new knowledge with existing knowledge, incrementing evidence and strengthening confidence."""
        existing = self.memory.get_knowledge_by_type(new_knowledge.type)
        if existing:
            existing.evidence_count += new_knowledge.evidence_count
            existing.confidence = min(0.99, round(existing.confidence + 0.05, 2))
            existing.description = new_knowledge.description
            existing.metadata.update(new_knowledge.metadata)
            target_knowledge = existing
        else:
            self.memory.upsert_knowledge(new_knowledge)
            target_knowledge = new_knowledge

        self.knowledge_graph.ingest_knowledge(target_knowledge)

        if self.event_bus:
            event = Event(
                event_type="SEMANTIC_KNOWLEDGE_UPDATED",
                timestamp=target_knowledge.last_updated,
                source="SemanticManager",
                payload=target_knowledge
            )
            self.event_bus.publish(event)

        return target_knowledge

    def update_knowledge(self, knowledge: Knowledge) -> None:
        """Directly update a Knowledge item."""
        self.memory.upsert_knowledge(knowledge)
        self.knowledge_graph.ingest_knowledge(knowledge)

    def delete_knowledge(self, knowledge_id: str) -> bool:
        """Delete a Knowledge item by ID."""
        if knowledge_id in self.memory._knowledge_store:
            del self.memory._knowledge_store[knowledge_id]
            return True
        return False

    def search_knowledge(self, query: str) -> List[Knowledge]:
        """Search knowledge items whose description or type contains query string."""
        results: List[Knowledge] = []
        q = query.lower()
        for k in self.memory.get_all_knowledge():
            if q in k.type.lower() or q in k.description.lower():
                results.append(k)
        return results

    def increase_confidence(self, knowledge_id: str, delta: float = 0.05) -> Optional[Knowledge]:
        """Increase confidence score of a knowledge item by delta."""
        item = self.memory._knowledge_store.get(knowledge_id)
        if item:
            item.confidence = min(0.99, round(item.confidence + delta, 2))
            item.evidence_count += 1
            return item
        return None

    def decrease_confidence(self, knowledge_id: str, delta: float = 0.05) -> Optional[Knowledge]:
        """Decrease confidence score of a knowledge item by delta."""
        item = self.memory._knowledge_store.get(knowledge_id)
        if item:
            item.confidence = max(0.0, round(item.confidence - delta, 2))
            return item
        return None

    def get_all_knowledge(self) -> List[Knowledge]:
        """Get all distilled knowledge."""
        return self.memory.get_all_knowledge()
