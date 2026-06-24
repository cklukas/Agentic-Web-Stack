# Agent Memory

Agent memory is persistent or retrievable context used beyond a single model call. It can include documents, embeddings, graph relationships, task state, user preferences, and audit-safe history.

Memory is not the same as RAG. RAG is one use of retrieval; memory is the broader layer that manages what context can survive, be searched, and be reused.

## Memory Responsibilities

- Retrieve relevant context for a task.
- Preserve provenance and visibility rules.
- Combine vector search with graph or metadata filters.
- Prevent untrusted retrieved text from overriding system policy.
- Support evaluation by making retrieval behavior inspectable.

## Demo Mapping

The demo memory configuration is [memory.yaml](/specs/demo/memory.yaml). It models:

- document chunking
- embeddings
- vector search
- knowledge graph expansion
- visibility filters

## Related Pages

- [RAG vs Memory](./rag-vs-memory.md)
- [Memory topic](/topics/memory)
- [Operations and Evaluation](/guides/operations-evaluation)
