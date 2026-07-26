"""Additional unit tests for EmbeddingProvider and swappable embedding providers."""

import pytest
from backend.cognitive_os.embedding.embedding_model import (
    SentenceTransformerEmbeddingProvider,
    CustomCombatEmbeddingProvider
)


def test_sentence_transformer_provider_encoding():
    provider = SentenceTransformerEmbeddingProvider(vector_dim=16)
    vec1 = provider.encode("Aggressive player reloading below 30% HP")
    vec2 = provider.encode("Defensive player dodging left")

    assert len(vec1) == 16
    assert len(vec2) == 16
    assert vec1 != vec2


def test_custom_combat_provider_encoding():
    provider = CustomCombatEmbeddingProvider(vector_dim=16)
    vec1 = provider.encode("Heavy attack combo interrupt")
    vec2 = provider.encode("Retreat and heal")

    assert len(vec1) == 16
    assert len(vec2) == 16
    assert vec1 != vec2


def test_provider_interchangeability():
    p1 = SentenceTransformerEmbeddingProvider(vector_dim=16)
    p2 = CustomCombatEmbeddingProvider(vector_dim=16)

    v1 = p1.encode("Combat Event")
    v2 = p2.encode("Combat Event")

    assert len(v1) == len(v2) == 16
