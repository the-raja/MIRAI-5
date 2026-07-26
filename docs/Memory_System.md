# MIRAI v2 — Episodic Memory & Vector Search

## 1. Memory Architecture
- **Feature Vector Embeddings:** Encodes player tactical state, gear, movement habits, and team composition into high-dimensional embedding vectors.
- **FAISS Indexing:** Fast vector indexing using HNSW (Hierarchical Navigable Small World) for sub-millisecond similarity retrieval.

## 2. Memory Retrieval Flow
1. Construct query vector from current combat state.
2. Query HNSW index for Top-K nearest historical encounters.
3. Extract successful counter-actions and weight decision scores in Utility AI.
