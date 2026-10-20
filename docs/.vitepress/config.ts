import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, statSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import type { Plugin } from 'vite'
import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

const repository = 'https://github.com/cklukas/Agentic-Web-Stack'
const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..')
const specsDir = path.join(rootDir, 'specs')

function copyDirectory(sourceDir: string, targetDir: string) {
  if (!existsSync(sourceDir)) return

  mkdirSync(targetDir, { recursive: true })

  for (const entry of readdirSync(sourceDir)) {
    const sourcePath = path.join(sourceDir, entry)
    const targetPath = path.join(targetDir, entry)
    const stat = statSync(sourcePath)

    if (stat.isDirectory()) {
      copyDirectory(sourcePath, targetPath)
    } else if (stat.isFile()) {
      copyFileSync(sourcePath, targetPath)
    }
  }
}

function contentTypeFor(filePath: string) {
  if (filePath.endsWith('.json')) return 'application/json; charset=utf-8'
  if (filePath.endsWith('.yaml') || filePath.endsWith('.yml')) return 'application/yaml; charset=utf-8'
  return 'text/plain; charset=utf-8'
}

function specsStaticPlugin(): Plugin {
  return {
    name: 'agentic-web-stack-specs-static',
    configureServer(server) {
      server.middlewares.use('/specs/', (request, response, next) => {
        if (!request.url) {
          next()
          return
        }

        const url = new URL(request.url, 'http://localhost')
        let relativePath = decodeURIComponent(url.pathname).replace(/^\/+/, '')
        if (relativePath.startsWith('specs/')) {
          relativePath = relativePath.slice('specs/'.length)
        }
        const requestedPath = path.resolve(specsDir, relativePath)

        if (!requestedPath.startsWith(`${specsDir}${path.sep}`)) {
          response.statusCode = 400
          response.end('Bad request')
          return
        }

        if (!existsSync(requestedPath) || !statSync(requestedPath).isFile()) {
          next()
          return
        }

        response.setHeader('Content-Type', contentTypeFor(requestedPath))
        response.end(readFileSync(requestedPath))
      })
    },
    closeBundle() {
      copyDirectory(specsDir, path.join(rootDir, 'docs', '.vitepress', 'dist', 'specs'))
    }
  }
}

export default withMermaid(defineConfig({
  title: 'Agentic Web Stack',
  description:
    'Reference architectures, protocols, standards, and technologies for the emerging Agentic Web.',
  base: process.env.VITEPRESS_BASE ?? '/',
  lastUpdated: true,
  mermaid: {
    securityLevel: 'strict',
    theme: 'default'
  },
  vite: {
    build: {
      chunkSizeWarningLimit: 1200
    },
    plugins: [specsStaticPlugin()]
  },
  themeConfig: {
    nav: [
      { text: 'Start', link: '/' },
      { text: 'Architecture', link: '/architecture/' },
      {
        text: 'Learn',
        items: [
          { text: 'Concepts', link: '/concepts/' },
          { text: 'Topics', link: '/topics/' },
          { text: 'Glossary', link: '/glossary' }
        ]
      },
      {
        text: 'Build',
        items: [
          { text: 'Guides', link: '/guides/' },
          { text: 'Specifications', link: '/specifications/' },
          { text: 'Decisions', link: '/decisions/' }
        ]
      },
      {
        text: 'References',
        items: [
          { text: 'Reference Index', link: '/references/' },
          { text: 'Glossary', link: '/glossary' },
          { text: 'Timeline', link: '/references/timeline' },
          { text: 'Technology Origins', link: '/references/technology-origins' },
          { text: 'Standards', link: '/references/standards' },
          { text: 'Protocols', link: '/references/protocols' },
          { text: 'Papers', link: '/references/papers' },
          { text: 'Tools', link: '/references/tools' }
        ]
      }
    ],
    sidebar: {
      '/architecture/': [
        {
          text: 'Architecture',
          items: [
            { text: 'Architecture Index', link: '/architecture/' },
            { text: 'Layer Model', link: '/architecture/layers' },
            { text: 'Technology Stack', link: '/architecture/technology-stack' },
            { text: 'Architecture Flows', link: '/architecture/flows' },
            { text: 'Architecture Variants', link: '/architecture/variants' }
          ]
        }
      ],
      '/guides/': [
        {
          text: 'Guides',
          items: [
            { text: 'Guide Index', link: '/guides/' },
            { text: 'End-to-End Demo', link: '/guides/end-to-end-demo' },
            { text: 'Run Local Demo', link: '/guides/run-local-demo' },
            { text: 'Security and Trust', link: '/guides/security-trust' },
            { text: 'Operations and Evaluation', link: '/guides/operations-evaluation' }
          ]
        }
      ],
      '/specifications/': [
        {
          text: 'Specifications',
          items: [{ text: 'Specification Index', link: '/specifications/' }]
        }
      ],
      '/decisions/': [
        {
          text: 'Decisions',
          items: [
            { text: 'Decision Index', link: '/decisions/' },
            { text: 'Protocol Selection', link: '/decisions/protocol-selection' },
            { text: 'API Style', link: '/decisions/api-style' },
            { text: 'Memory Store Selection', link: '/decisions/memory-store-selection' },
            { text: 'Model Deployment', link: '/decisions/model-deployment' },
            { text: 'Agent Framework Selection', link: '/decisions/agent-framework-selection' }
          ]
        }
      ],
      '/concepts/': [
        {
          text: 'Core Concepts',
          items: [
            { text: 'Concept Index', link: '/concepts/' },
            { text: 'Agent Card', link: '/concepts/agent-card' },
            { text: 'Agent2Agent', link: '/concepts/a2a' },
            { text: 'Model Context Protocol', link: '/concepts/mcp' },
            { text: 'Agent Discovery', link: '/concepts/agent-discovery' },
            { text: 'llms.txt', link: '/concepts/llms-txt' },
            { text: 'Identity Delegation', link: '/concepts/identity-delegation' },
            { text: 'Trust Model', link: '/concepts/trust-model' },
            { text: 'Agent Registry', link: '/concepts/agent-registry' },
            { text: 'Tool Use', link: '/concepts/tool-use' },
            { text: 'Agent Memory', link: '/concepts/memory' },
            { text: 'Evaluation', link: '/concepts/evaluation' },
            { text: 'Versioning and Governance', link: '/concepts/versioning-governance' }
          ]
        },
        {
          text: 'Comparisons',
          items: [
            { text: 'MCP vs A2A', link: '/concepts/mcp-vs-a2a' },
            { text: 'Agent Card vs OpenAPI', link: '/concepts/agent-card-vs-openapi' },
            { text: 'RAG vs Memory', link: '/concepts/rag-vs-memory' },
            { text: 'Framework vs Protocol', link: '/concepts/framework-vs-protocol' }
          ]
        }
      ],
      '/topics/': [
        {
          text: 'Topic Guides',
          items: [{ text: 'Topic Index', link: '/topics/' }]
        },
        {
          text: 'Web Foundations',
          items: [
            { text: 'Discovery', link: '/topics/discovery' },
            { text: 'Identity', link: '/topics/identity' },
            { text: 'APIs', link: '/topics/apis' }
          ]
        },
        {
          text: 'Agent Runtime',
          items: [
            { text: 'Agent Protocols', link: '/topics/agent-protocols' },
            { text: 'Memory', link: '/topics/memory' },
            { text: 'Models', link: '/topics/models' }
          ]
        },
        {
          text: 'Application Layer',
          items: [
            { text: 'Applications', link: '/topics/applications' }
          ]
        }
      ],
      '/references/': [
        {
          text: 'References',
          items: [
            { text: 'Reference Index', link: '/references/' },
            { text: 'Standards', link: '/references/standards' },
            { text: 'Protocols', link: '/references/protocols' },
            { text: 'Timeline', link: '/references/timeline' },
            { text: 'Technology Origins', link: '/references/technology-origins' },
            { text: 'Papers', link: '/references/papers' },
            { text: 'Tools', link: '/references/tools' }
          ]
        }
      ],
      '/': [
        {
          text: 'Start',
          items: [
            { text: 'Overview', link: '/' },
            { text: 'Glossary', link: '/glossary' }
          ]
        },
        {
          text: 'Reference',
          items: [
            { text: 'References', link: '/references/' },
            { text: 'Technology Stack', link: '/architecture/technology-stack' },
            { text: 'Topic Guides', link: '/topics/' }
          ]
        }
      ]
    },
    search: {
      provider: 'local'
    },
    outline: {
      level: [2, 3]
    },
    editLink: {
      pattern: `${repository}/edit/main/docs/:path`,
      text: 'Edit this page on GitHub'
    },
    socialLinks: [{ icon: 'github', link: repository }],
    footer: {
      message: 'Page created by Dr. C. Klukas'
    }
  }
}))
