# Memory

## Topic Summary

The memory layer gives agents durable access to semantic context, structured knowledge, historical state, and retrievable domain information.

## Stack Level

Memory is Layer 5 of the Agentic Web Stack. It decides what context survives beyond one prompt, how information is retrieved, and how structured or semantic knowledge becomes available to agents.

## Goals

- Compare vector databases, knowledge graphs, and hybrid memory patterns.
- Document how memory supports RAG, semantic search, and reasoning over relationships.
- Keep storage choices modular and replaceable.

## Common Tech Stack

| Technology | Role in memory |
| --- | --- |
| Vector databases | Store embeddings and run similarity search for semantic retrieval |
| Chroma, Qdrant, Weaviate | Common dedicated vector database options |
| pgvector | Vector search inside PostgreSQL for teams already using relational data |
| Embedding models | Convert text or multimodal content into searchable vectors |
| RAG pipelines | Retrieve relevant context before model generation |
| Knowledge graphs | Store explicit entities, relationships, and paths for reasoning |
| Neo4j, RDF, SPARQL | Common graph database and semantic web technologies |
| Object storage | Store source documents, files, artifacts, and large binary content |

## Reference Scenario

The Literature Review Assistant uses semantic retrieval for relevant passages and a graph model for explicit paper-author-topic relationships. The combination supports both similarity search and relationship-aware context expansion.

## Related Materials

- [Memory Store Selection Decision](/decisions/memory-store-selection)
- [End-to-End Demo](/guides/end-to-end-demo)
- [Specifications](/specifications/)

## Standards and Protocols

- Vector search APIs
- RDF and SPARQL for graph-oriented knowledge
- Property graph patterns
- Embedding and retrieval pipelines

## Example Use Case

A research agent needs to answer questions about a collection of technical papers. It stores chunks and embeddings in a vector database, keeps paper-author-topic relationships in a graph, and retrieves both semantic matches and explicit relationships before generating an answer.

## Example Memory Specification Sketch

```yaml
corpus:
  name: agentic-web-papers
  sourceStorage: s3://example-research-corpus/papers/
chunking:
  strategy: markdown-section
  maxTokens: 700
  overlapTokens: 100
embeddings:
  model: text-embedding-example
  dimensions: 1536
vectorIndex:
  engine: qdrant
  collection: agentic_web_chunks
  distance: cosine
  payloadFields:
    - documentId
    - title
    - section
    - sourceUrl
knowledgeGraph:
  engine: neo4j
  nodes:
    - Paper
    - Author
    - Topic
  relationships:
    - WRITTEN_BY
    - CITES
    - DISCUSSES
retrieval:
  topK: 8
  filters:
    visibility: public
  graphExpansion:
    enabled: true
    maxHops: 2
```

Example artifact: [memory.yaml](/specs/demo/memory.yaml).

## Reference Links and Papers

- [Technology Origins](/references/technology-origins) - Local reference page with historical context for RDF, SPARQL, Neo4j, vector databases, and embedding infrastructure.
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) - Foundational RAG paper describing retrieval over external knowledge for generation.
- [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/) - W3C recommendation defining the RDF graph data model.
- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/) - W3C recommendation for querying RDF graphs.
- [Chroma documentation](https://docs.trychroma.com/) - Documentation for Chroma embedding storage and retrieval.
- [Qdrant documentation](https://qdrant.tech/documentation/) - Documentation for Qdrant vector search, filtering, and deployment.
- [Weaviate documentation](https://weaviate.io/developers/weaviate) - Documentation for Weaviate vector, hybrid, and semantic search features.
- [pgvector repository](https://github.com/pgvector/pgvector) - PostgreSQL extension repository for vector similarity search.
- [Neo4j documentation](https://neo4j.com/docs/) - Documentation for Neo4j graph database modeling, querying, and operations.

## Design Considerations

- Keep source documents separate from vector and graph indexes.
- Store source IDs in every retrieved chunk so answers can cite evidence.
- Combine semantic retrieval with metadata filters and policy checks.
- Define retention, privacy, and deletion expectations before storing user data.
