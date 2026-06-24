# Models

## Topic Summary

The model layer describes how hosted and local language models can be integrated behind a common architecture without committing the whole stack to one provider.

## Stack Level

Models are Layer 6 of the Agentic Web Stack. They provide reasoning, generation, extraction, planning, tool-selection, embeddings, and multimodal interpretation. The layer should be swappable because model capabilities, prices, latency, and deployment constraints change quickly.

## Goals

- Keep model access provider-neutral.
- Support hosted models and local inference options.
- Document model selection, capability differences, and operational tradeoffs.

## Common Tech Stack

| Technology | Role in models |
| --- | --- |
| Hosted model APIs | Managed reasoning, generation, vision, speech, embeddings, and tool calling |
| OpenAI, Gemini, Claude | Common hosted model providers |
| Local runtimes | Self-hosted inference for privacy, cost, latency, or offline requirements |
| Ollama, llama.cpp, vLLM | Common local or self-hosted model runtimes |
| Model gateways | Centralized routing, logging, fallback, rate limiting, and policy enforcement |
| Embedding models | Semantic representation for search and RAG |
| Evaluation tools | Regression testing for quality, safety, latency, and cost |

## Reference Scenario

The Literature Review Assistant uses different model routes for reasoning, summarization, private classification, and embeddings. A gateway-style abstraction keeps application logic from depending directly on one provider.

## Related Materials

- [Model Deployment Decision](/decisions/model-deployment)
- [Operations and Evaluation](/guides/operations-evaluation)
- [Specifications](/specifications/)

## Standards and Protocols

- Provider API conventions
- Streaming responses
- Tool calling and structured outputs where supported
- Local model server APIs

## Example Use Case

An agent platform uses a hosted reasoning model for complex planning, a cheaper model for summarization, a local model for private classification, and a dedicated embedding model for retrieval. A gateway keeps the application code from depending directly on every provider API.

## Example Model Routing Specification

```yaml
modelGateway:
  defaultPolicy: balanced
  logging:
    capturePrompts: false
    captureUsage: true
  routes:
    reasoning:
      primary:
        provider: openai
        model: gpt-example-reasoning
      fallback:
        provider: anthropic
        model: claude-example
    summarization:
      primary:
        provider: gemini
        model: gemini-example-flash
      maxLatencyMs: 2500
    privateClassification:
      primary:
        provider: local
        runtime: ollama
        model: local-classifier
      dataPolicy: no_external_network
    embeddings:
      primary:
        provider: openai
        model: text-embedding-example
        dimensions: 1536
budgets:
  dailyUsd: 25
  perRequestUsd: 0.25
```

Example artifact: [model-routing.yaml](/specs/demo/model-routing.yaml).

## Reference Links and Papers

- [Technology Origins](/references/technology-origins) - Local reference page with origin and stewardship context for hosted model APIs, local runtimes, serving engines, and gateways.
- [OpenAI API documentation](https://platform.openai.com/docs) - Current API documentation for OpenAI models, tools, embeddings, multimodal inputs, and platform features.
- [Gemini API documentation](https://ai.google.dev/gemini-api/docs) - Google documentation for Gemini models, generation, multimodal inputs, and developer APIs.
- [Anthropic Claude documentation](https://docs.anthropic.com/) - Anthropic documentation for Claude models, messages, tools, and platform APIs.
- [Ollama documentation](https://ollama.com/docs) - Documentation for running local models with Ollama.
- [llama.cpp repository](https://github.com/ggml-org/llama.cpp) - Source repository for local LLM inference with C/C++ and quantized model formats.
- [vLLM documentation](https://docs.vllm.ai/) - Documentation for high-throughput model serving and the vLLM runtime.
- [LiteLLM documentation](https://docs.litellm.ai/) - Documentation for provider abstraction, routing, logging, budgets, and gateway operation.

## Design Considerations

- Route by task type rather than by provider name in application code.
- Keep provider-specific capabilities visible without making them hard dependencies.
- Separate local inference concerns from hosted provider concerns.
- Track cost, latency, privacy, and deployment constraints for every model route.
