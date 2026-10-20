# Technology Origins

This page tracks where the major Agentic Web Stack technologies came from, who originally developed or stewarded them, and why they matter to agent-native systems.

Dates are practical architecture dates: first public announcement, first stable specification, or major public release. Some open-source projects evolve continuously, so treat these entries as orientation, not legal or archival provenance.

## How to Read This Page

The origin of a technology is not trivia. It helps estimate maturity, governance risk, interoperability expectations, and how quickly the interface may change.

- A standards-body technology such as OAuth2, OpenID Connect, RDF, SPARQL, or RFC-based well-known URIs usually has slower change but broader institutional adoption.
- A foundation-governed project such as A2A or OpenAPI usually signals an attempt to move beyond one company's implementation choices.
- A company-originated API or framework can move quickly, but may need extra abstraction if vendor neutrality is important.
- A university or research-originated runtime such as vLLM may be valuable because it encodes a specific systems idea, not only a product surface.
- A community-maintained open-source tool such as pgvector or llama.cpp may become infrastructure because it is simple to adopt and easy to run locally.

Use this page with the [Technology Stack](/architecture/technology-stack): the stack page explains where a technology belongs, while this page explains where it came from and who currently shapes it.

## Agent-Specific Protocols

Agent-specific protocols are the newest part of the stack. They should be evaluated with extra attention to versioning, governance, security model, SDK maturity, and implementation examples.

| Technology | First public milestone | Origin / steward | Why it matters |
| --- | --- | --- | --- |
| Agent2Agent (A2A) | Announced by Google in 2025; donated to the Linux Foundation in June 2025; v1.0 announced as the first stable version in 2026 | Originally developed by Google; now a Linux Foundation project with a technical steering committee | Provides an agent-to-agent interoperability layer for discovery, task delegation, messages, artifacts, streaming, and asynchronous work |
| Agent Card | Emerged with A2A discovery in 2025 and stabilized with the A2A specification | Defined by the A2A project | Gives agents a machine-readable self-description at `/.well-known/agent-card.json`, including identity, skills, endpoints, capabilities, and security requirements |
| Model Context Protocol (MCP) | Introduced by Anthropic in November 2024 | Originally developed by Anthropic; now broadly adopted across AI clients, tools, and servers | Standardizes how AI applications and agents connect to tools, resources, and prompt templates |

## Documentation Discovery

| Technology | First public milestone | Origin / steward | Why it matters |
| --- | --- | --- | --- |
| [llms.txt](/concepts/llms-txt) | Proposed 3 September 2024; v2 published August 2026 | Jeremy Howard; community proposal at [llmstxt.org](https://llmstxt.org/) | A Markdown entry point for documentation context in Layer 1; v2 clarifies path scope and discovery links. It is an evolving proposal, not a formal web standard. |

See the [v2 revision notes](https://llmstxt.org/changes.html) for changes to link discovery, Markdown page URLs, and consumption guidance.

## Web, API, and Identity Foundations

These are older web foundations. They are not agent-specific, but they are critical because agent systems still need ordinary service contracts, authentication, authorization, and metadata.

| Technology | First public milestone | Origin / steward | Why it matters |
| --- | --- | --- | --- |
| REST | Defined in Roy Fielding's 2000 doctoral dissertation at UC Irvine | Roy T. Fielding, University of California, Irvine | Architectural basis for much of the modern web API ecosystem |
| OAuth2 | RFC 6749 published by the IETF in October 2012 | IETF OAuth Working Group | Main authorization framework for delegated, scoped access to protected resources |
| OpenID Connect | Final OpenID Connect Core 1.0 specification published in 2014; errata set 2 incorporated in 2023 | OpenID Foundation | Adds interoperable identity and ID tokens on top of OAuth2 |
| OpenAPI | OpenAPI Initiative launched in 2015 after SmartBear donated the Swagger Specification to the Linux Foundation | SmartBear, OpenAPI Initiative, Linux Foundation | Makes HTTP APIs machine-readable for humans, agents, validators, SDK generators, and gateways |
| GraphQL | Developed at Facebook in 2012; open-sourced in 2015; moved under the GraphQL Foundation in 2018 | Facebook / Meta, GraphQL Foundation, Linux Foundation | Lets clients query precisely shaped data, useful when agents need flexible access to complex domains |
| JSON Schema | Draft 0 and Draft 1 published on 5 December 2009 | Early drafts by Kris Zyp and contributors; now community-maintained at json-schema.org | Common schema vocabulary for validating and documenting JSON payloads |

## Memory, Retrieval, and Knowledge

Memory technologies come from two different traditions: semantic web and graph systems on one side, and embedding/vector retrieval systems on the other. Practical agent systems often combine both.

| Technology | First public milestone | Origin / steward | Why it matters |
| --- | --- | --- | --- |
| RDF | W3C Recommendation in February 1999 | W3C, with early editors from Nokia Research Center and W3C | Foundation for semantic web data and graph-based knowledge representation |
| SPARQL | W3C Recommendation in January 2008; SPARQL 1.1 in 2013 | W3C SPARQL Working Group | Query language for RDF graphs and semantic knowledge stores |
| Neo4j | Prototype work began around 2000; first version in 2002; company and open-source release in 2007 | Neo4j founders Emil Eifrem, Johan Svensson, and Peter Neubauer | Mature native graph database for entity and relationship modeling |
| Chroma | Founded in 2022; public open-source project and cloud service followed | Chroma, co-founded by Jeff Huber and Anton Troynikov | Developer-friendly embedding and search infrastructure for AI applications |
| Qdrant | Founded in 2021 | André Zayarni and Andrey Vasnetsov | Rust-based vector search engine and database for semantic retrieval |
| Weaviate | Launched by SeMI Technologies in 2019; company renamed Weaviate in 2023 | SeMI Technologies / Weaviate | AI-native vector database with semantic and hybrid search features |
| pgvector | Early 2020s open-source PostgreSQL extension | Andrew Kane and contributors | Adds vector similarity search to PostgreSQL, useful when teams want embeddings inside an existing relational database |

## Models, Local Runtimes, and Gateways

Model infrastructure changes faster than the web standards layer. For production systems, provenance helps distinguish hosted model APIs, local runtime projects, serving engines, and gateway abstractions.

| Technology | First public milestone | Origin / steward | Why it matters |
| --- | --- | --- | --- |
| OpenAI API | API announced in 2020; OpenAI founded in 2015 | OpenAI | Popular hosted model API surface for text, multimodal, embeddings, tools, and agent workloads |
| Claude | Introduced by Anthropic in March 2023 | Anthropic | Hosted model family designed around helpfulness, reliability, and API access |
| Gemini | Gemini 1.0 announced by Google and Google DeepMind in December 2023 | Google / Google DeepMind | Hosted multimodal model family used across Google AI products and APIs |
| llama.cpp | Released in March 2023 | Georgi Gerganov and the ggml community | Made local LLM inference practical on consumer hardware using C/C++ and quantized model formats |
| Ollama | Public project activity and Docker support appeared in 2023 | Ollama | Simplifies running local models on macOS, Linux, and Windows |
| vLLM | Announced by UC Berkeley researchers in 2023 | Sky Computing Lab at UC Berkeley; LMSYS ecosystem | High-throughput LLM serving engine built around PagedAttention |
| LiteLLM | Public open-source AI gateway in the early LLM provider-fragmentation era | BerriAI / LiteLLM contributors | Provides a unified OpenAI-compatible interface, proxy, routing, logging, and budget control across many model providers |

## Agent Frameworks

Agent frameworks sit closest to application code. They are useful for orchestration and developer productivity, but they should not replace protocol-level interoperability contracts when systems need to cross vendor or organizational boundaries.

| Technology | First public milestone | Origin / steward | Why it matters |
| --- | --- | --- | --- |
| LangGraph | Launched by LangChain in early 2024 | LangChain | Stateful, graph-based orchestration for long-running and controllable agents |
| CrewAI | Emerged as a public multi-agent framework around 2023-2024 | Created by João Moura; CrewAI company and community | Role-based multi-agent workflows, crews, flows, memory, and observability |
| Semantic Kernel | Public Microsoft documentation and SDK work became visible in 2023; agent framework work matured later | Microsoft | Model-agnostic SDK and agent framework for .NET, Python, and Java ecosystems |
| Agent Development Kit (ADK) | Introduced by Google at Cloud Next 2025 | Google | Open-source framework for building, debugging, evaluating, and deploying agents and multi-agent systems |

## References

- [A2A Protocol](https://a2a-protocol.org/latest/) - Official A2A documentation home, including overview, specification, extensions, resources, and community links.
- [Google Cloud donates A2A to Linux Foundation](https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/) - Google announcement describing the transfer of A2A to the Linux Foundation.
- [Linux Foundation A2A project launch](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents) - Linux Foundation announcement for the Agent2Agent protocol project.
- [A2A v1.0 announcement](https://a2a-protocol.org/latest/announcing-1.0/) - A2A community announcement for the first stable production-ready specification.
- [A2A Agent Discovery](https://a2a-protocol.org/latest/topics/agent-discovery/) - Official page explaining Agent Cards, discovery strategies, security considerations, and caching.
- [Introducing Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) - Anthropic's November 2024 announcement for MCP.
- [MCP Specification](https://modelcontextprotocol.io/specification) - Current MCP specification and protocol reference.
- [Roy Fielding REST dissertation](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) - Original academic source defining REST as an architectural style.
- [RFC 6749: OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749) - Core IETF OAuth2 specification from October 2012.
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) - OpenID Foundation specification defining identity on top of OAuth2.
- [OpenAPI Initiative About](https://www.openapis.org/about) - OAI description of OpenAPI governance and its origin in the donated Swagger Specification.
- [Linux Foundation Open API Initiative launch](https://www.linuxfoundation.org/press/press-release/new-collaborative-project-to-extend-swagger-specification-for-building-connected-applications-and-services) - 2015 announcement of the Open API Initiative.
- [GraphQL at Facebook](https://engineering.fb.com/2015/09/14/core-infra/graphql-a-data-query-language/) - Meta engineering article describing GraphQL's origin and open-source release.
- [GraphQL Foundation](https://graphql.org/) - Current GraphQL documentation and governance entry point.
- [JSON Schema specification links](https://json-schema.org/specification-links) - Official list of JSON Schema draft versions and publication dates.
- [W3C RDF 1999 Recommendation](https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/) - First official RDF recommendation.
- [W3C SPARQL Query Language](https://www.w3.org/TR/rdf-sparql-query/) - 2008 W3C Recommendation for querying RDF.
- [Neo4j company history](https://neo4j.com/company/) - Neo4j timeline covering prototype, first version, company formation, and open-source release.
- [Qdrant About Us](https://qdrant.tech/about-us/) - Qdrant origin story and founding context.
- [Weaviate Google Cloud customer story](https://cloud.google.com/customers/semi-technologies) - Google Cloud profile noting SeMI Technologies and the 2019 launch of Weaviate.
- [pgvector GitHub repository](https://github.com/pgvector/pgvector) - Source repository for the PostgreSQL vector extension.
- [OpenAI API announcement](https://openai.com/index/openai-api/) - Original OpenAI API launch article.
- [Introducing Claude](https://www.anthropic.com/news/introducing-claude) - Anthropic's first Claude announcement from March 2023.
- [Introducing Gemini](https://blog.google/innovation-and-ai/technology/ai/google-gemini-ai/) - Google and Google DeepMind announcement for Gemini 1.0.
- [llama.cpp GitHub repository](https://github.com/ggml-org/llama.cpp) - Source repository and project overview for local LLM inference.
- [Ollama documentation](https://docs.ollama.com/) - Official documentation for running local models with Ollama.
- [vLLM blog announcement](https://vllm.ai/blog/2023-06-20-vllm) - UC Berkeley / LMSYS introduction to vLLM and PagedAttention.
- [vLLM documentation](https://docs.vllm.ai/) - Current documentation noting UC Berkeley Sky Computing Lab origins.
- [LiteLLM GitHub repository](https://github.com/BerriAI/litellm) - Source repository describing LiteLLM as an open-source AI gateway.
- [LangGraph launch note](https://changelog.langchain.com/?date=2024-01-01) - LangChain changelog entry announcing LangGraph in January 2024.
- [CrewAI documentation](https://docs.crewai.com/) - Current CrewAI documentation for agents, crews, flows, guardrails, memory, and observability.
- [Semantic Kernel overview](https://learn.microsoft.com/en-us/semantic-kernel/overview/) - Microsoft Learn overview of Semantic Kernel.
- [Google ADK announcement](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/) - Google announcement introducing Agent Development Kit at Cloud Next 2025.
