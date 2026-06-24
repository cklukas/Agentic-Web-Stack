# RAG vs Memory

RAG and memory are related, but they are not the same layer.

| Question | RAG | Memory |
| --- | --- | --- |
| Meaning | Retrieval-Augmented Generation | Persistent and retrievable context layer |
| Scope | Retrieve context for a model call | Store, retrieve, relate, filter, and govern context |
| Typical data | Documents and passages | Documents, embeddings, graph entities, task state, preferences |
| Risk | Retrieved text may be untrusted | Stored context may become stale, sensitive, or over-broad |
| Demo artifact | Retrieval behavior in [memory.yaml](/specs/demo/memory.yaml) | Full memory configuration in [memory.yaml](/specs/demo/memory.yaml) |

## Decision Rule

Use RAG as a generation pattern. Design memory as an architecture layer with visibility, provenance, retrieval, evaluation, and governance.

## Related Pages

- [Agent Memory](./memory.md)
- [Memory topic](/topics/memory)
- [Evaluation](./evaluation.md)
