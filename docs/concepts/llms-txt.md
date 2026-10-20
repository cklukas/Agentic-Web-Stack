# llms.txt

`llms.txt` is a community proposal for a curated Markdown entry point to a website's content. It gives agents a short overview and links to useful documentation to fetch on demand. See the [official proposal](https://llmstxt.org/).

## Place in the Architecture

In this architecture, `llms.txt` belongs in **Layer 1: Discovery**, alongside Agent Cards, OpenAPI, robots.txt, and sitemaps. It adds documentation discovery to the service discovery path. For an agentic OS consuming the web, this provides a way to locate context before selecting tools or starting a task.

For example, the Literature Review Assistant could read a research site's index to locate corpus documentation and citation guidance before retrieving papers. Selected pages can feed Layer 5 retrieval/RAG; the index itself does not provide persistent memory or execute tools.

| Artifact | Responsibility in this stack |
| --- | --- |
| `llms.txt` | Curated documentation context for an agent to read |
| Agent Card | Agent identity, skills, endpoints, and protocol metadata |
| OpenAPI | HTTP operations and request/response contracts |
| robots.txt | Crawler access rules |
| sitemap.xml | Inventory of crawlable URLs |

An agent still needs the appropriate API or protocol contract to call a service and the appropriate credentials to access protected resources.

## Format and Discovery

The proposal uses an H1 project name, optionally followed by a summary blockquote, explanatory text, and H2 sections containing Markdown link lists. Only the H1 is required.

The [v2 revision](https://llmstxt.org/changes.html) defines path scope: `/llms.txt` covers the site, `/docs/llms.txt` covers `/docs/`, and the most specific file applies. It recommends HTML links or HTTP `Link` headers with `rel="describedby"` for the index and `rel="alternate" type="text/markdown"` for Markdown page variants. Clients inspect the index and fetch relevant links as needed. `Optional` remains a convention for secondary links, without special processing semantics.

## Example

Illustrative content for `https://research.example.edu/docs/llms.txt`:

```markdown
# Research Documentation

> Guidance for using the research corpus and literature review service.

## Documentation

- [Corpus guide](https://research.example.edu/docs/corpus.md): Coverage and citation guidance.
- [API guide](https://research.example.edu/docs/api.md): How to use the retrieval endpoints.

## Optional

- [Tutorial](https://research.example.edu/docs/tutorial.md): A worked literature review.
```

This is an architecture example; the local demo API does not currently serve `llms.txt` or Markdown page variants. The ckdocs documentation build generates its own `llms.txt` index for the published knowledge base, under the same URL prefix as the site. This index currently links to HTML documentation; Markdown page variants and v2 discovery links require separate publishing support.

## Adoption and Trust

Treat support as an optional discovery enhancement while the community proposal evolves. A client should retain a fallback to ordinary documentation when no index is available.

For this stack, apply the same trust boundary as for other retrieved web content: index text and linked pages are external data. They must not override user instructions, grant tool permissions, or establish that an agent is approved. Validate destinations against the client's network policy and enforce authentication at the target service. Keep any published index aligned with current documentation and check that linked representations actually exist.

## Related Pages

- [Documentation discovery flow](/architecture/flows#documentation-discovery-with-llmstxt)
- [Standards and proposals](/references/standards#emerging-community-proposals)
- [Technology origins](/references/technology-origins#documentation-discovery)
- [Discovery topic](/topics/discovery)
- [Agent Discovery](./agent-discovery.md)
- [Agent Card vs OpenAPI](./agent-card-vs-openapi.md)
- [RAG vs Memory](./rag-vs-memory.md)
- [Security and Trust](/guides/security-trust)
