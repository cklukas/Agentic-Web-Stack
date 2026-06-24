# Foundation Roadmap

## Summary

The foundation milestone establishes Agentic Web Stack as a documentation-first reference architecture. It provides a VitePress documentation site, a clear project structure, and a publishing path for GitHub Pages.

## What It Provides

- VitePress documentation site under `docs/`.
- Topic pages for each Agentic Web Stack layer.
- Reference pages for standards, protocols, papers, and tools.
- Skeleton implementation folders with `.gitkeep` placeholders.
- npm scripts for local documentation development and static builds.
- GitHub Actions workflow for documentation build and GitHub Pages deployment.

## Directory Structure

```text
.
├── .github/
│   └── workflows/
│       └── docs.yml
├── agents/
│   └── .gitkeep
├── docs/
│   ├── .vitepress/
│   │   └── config.ts
│   ├── architecture/
│   ├── references/
│   ├── topics/
│   └── index.md
├── examples/
│   └── .gitkeep
├── infra/
│   └── .gitkeep
├── services/
│   └── .gitkeep
├── specs/
│   └── .gitkeep
├── package.json
└── README.md
```

## Quality Checks

- `npm run docs:build` completes successfully.
- Documentation navigation links to architecture, topics, and references.
- GitHub Actions builds docs for repository changes.
- GitHub Pages deployment runs only for pushes to `main`.
- Implementation folders contain placeholders only, with no per-folder README files.

## Next Milestones

- [Documentation Package](./phase-2.md) adds validated specs, diagrams, security guidance, operations guidance, and decision guides.
- [Runnable Demo](./phase-3.md) adds the first backend, Agent Card endpoint, MCP server, A2A service, and memory demonstration.
