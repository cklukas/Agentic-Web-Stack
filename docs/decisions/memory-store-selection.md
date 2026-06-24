# Memory Store Selection

## Recommended Starting Point

Use a **Qdrant-style vector index** for semantic retrieval and a **Neo4j-style graph model** for explicit relationships in the demo architecture. This keeps vector retrieval and graph reasoning separate enough to teach clearly.

## Tradeoffs

| Choice | Best fit | Strength | Cost |
| --- | --- | --- | --- |
| Chroma | Local development and simple prototypes | Low-friction embedding workflows | Less emphasis on production operations |
| Qdrant | Vector search service | Strong filtering and deployment story | Separate service to operate |
| Weaviate | Hybrid semantic/search workloads | Rich AI-native database features | More platform surface area |
| pgvector | PostgreSQL-first teams | Keeps vectors near relational data | Scaling and tuning stay tied to Postgres |
| Neo4j | Explicit entity relationships | Mature graph modeling and traversal | Separate graph database to operate |
| RDF/SPARQL | Standards-based semantic data | Interoperable semantic web model | Higher modeling complexity |

## Architecture Guidance

- Use vector search for semantic similarity and RAG.
- Use a graph when relationships are first-class data, not only metadata.
- Keep document source storage separate from indexes.
- Store document IDs in both vector payloads and graph nodes so results can be joined.

## Example Artifact

- [memory.yaml](/specs/demo/memory.yaml)
