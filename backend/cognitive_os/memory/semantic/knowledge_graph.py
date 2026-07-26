"""KnowledgeGraph module.

Uses NetworkX directed graph structure to represent relationships between players, habits, weapons, dodge directions, and combat behaviors.
"""

from typing import List, Dict, Any, Optional
import networkx as nx
from backend.cognitive_os.memory.semantic.knowledge import Knowledge


class KnowledgeGraph:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_concept(self, name: str, node_type: str = "Concept", attributes: Optional[Dict[str, Any]] = None) -> None:
        """Add a concept node to the knowledge graph."""
        attrs = attributes if attributes is not None else {}
        attrs["node_type"] = node_type
        self.graph.add_node(name, **attrs)

    def add_relation(self, source: str, relation: str, target: str, confidence: float = 1.0) -> None:
        """Add a directed relation edge between two concepts (e.g. Player -> Uses -> Shotgun)."""
        if not self.graph.has_node(source):
            self.add_concept(source, node_type="Entity")
        if not self.graph.has_node(target):
            self.add_concept(target, node_type="Attribute")

        self.graph.add_edge(source, target, relation=relation, confidence=confidence)

    def ingest_knowledge(self, knowledge: Knowledge) -> None:
        """Ingest a Knowledge object into graph relationships."""
        player_node = "Player"

        if knowledge.type == "PreferredWeapon":
            wep = knowledge.metadata.get("preferred_weapon", "Shotgun")
            self.add_relation(player_node, "USES", wep, confidence=knowledge.confidence)

            # Link weapon to typical range
            self.add_relation(wep, "USUALLY", "Medium Range", confidence=knowledge.confidence)
            self.add_relation("Medium Range", "FREQUENTLY", "Reload After 3 Attacks", confidence=knowledge.confidence)

        elif knowledge.type == "PreferredDodge":
            dodge = knowledge.metadata.get("preferred_dodge", "Left")
            self.add_relation(player_node, "PREFERS_DODGE", f"Dodge {dodge}", confidence=knowledge.confidence)

        elif knowledge.type == "PlayerReloadHabit":
            avg_reloads = knowledge.metadata.get("avg_reloads_per_battle", 15)
            self.add_relation(player_node, "HABITUALLY_RELOADS", f"Reloads ({avg_reloads}/battle)", confidence=knowledge.confidence)

        elif knowledge.type == "EngagementRange":
            avg_dist = knowledge.metadata.get("avg_distance_meters", 6.0)
            self.add_relation(player_node, "MAINTAINS_DISTANCE", f"{avg_dist}m Range", confidence=knowledge.confidence)

    def query_relations_from(self, source: str) -> List[Dict[str, Any]]:
        """Find all outgoing relationship edges from source concept."""
        if not self.graph.has_node(source):
            return []

        results: List[Dict[str, Any]] = []
        for target in self.graph.successors(source):
            edge_data = self.graph.get_edge_data(source, target)
            results.append({
                "source": source,
                "relation": edge_data.get("relation", "CONNECTED_TO"),
                "target": target,
                "confidence": edge_data.get("confidence", 1.0)
            })
        return results

    def query_path(self, source: str, target: str) -> List[str]:
        """Find shortest relationship path between source and target concepts."""
        if not self.graph.has_node(source) or not self.graph.has_node(target):
            return []
        try:
            return nx.shortest_path(self.graph, source=source, target=target)
        except nx.NetworkXNoPath:
            return []

    def get_summary(self) -> Dict[str, Any]:
        """Returns node count, edge count, and list of edges."""
        edges = []
        for u, v, d in self.graph.edges(data=True):
            edges.append(f"{u} --[{d.get('relation', 'REL')}]--> {v} (conf: {d.get('confidence', 1.0)})")

        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "edges": edges
        }
