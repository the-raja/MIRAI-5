"""Unit tests for KnowledgeGraph NetworkX relationship modeling."""

import pytest
from backend.cognitive_os.memory.semantic.knowledge import Knowledge
from backend.cognitive_os.memory.semantic.knowledge_graph import KnowledgeGraph


def test_knowledge_graph_relationship_building():
    kg = KnowledgeGraph()

    k_weapon = Knowledge(
        id="k1",
        type="PreferredWeapon",
        confidence=0.87,
        evidence_count=15,
        description="Player prefers Shotgun",
        metadata={"preferred_weapon": "Shotgun"}
    )
    kg.ingest_knowledge(k_weapon)

    # Query relations from "Player" -> USES -> Shotgun
    rel_player = kg.query_relations_from("Player")
    assert len(rel_player) >= 1
    assert rel_player[0]["relation"] == "USES"
    assert rel_player[0]["target"] == "Shotgun"

    # Query path from "Player" to "Reload After 3 Attacks"
    path = kg.query_path("Player", "Reload After 3 Attacks")
    assert len(path) == 4
    assert path == ["Player", "Shotgun", "Medium Range", "Reload After 3 Attacks"]


def test_knowledge_graph_summary():
    kg = KnowledgeGraph()
    kg.add_relation("Player", "PREFERS_DODGE", "Dodge Left", confidence=0.94)

    summary = kg.get_summary()
    assert summary["total_nodes"] == 2
    assert summary["total_edges"] == 1
    assert "Player --[PREFERS_DODGE]--> Dodge Left" in summary["edges"][0]
