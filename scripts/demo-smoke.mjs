import { spawn, spawnSync } from 'node:child_process'
import net from 'node:net'

function freePort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer()
    server.once('error', reject)
    server.listen(0, '127.0.0.1', () => {
      const address = server.address()
      const port = typeof address === 'object' && address ? address.port : undefined
      server.close(() => {
        if (!port) reject(new Error('Could not allocate a local port.'))
        else resolve(port)
      })
    })
  })
}

async function waitForHealth(baseUrl, processRef, timeoutMs) {
  const startedAt = Date.now()
  while (Date.now() - startedAt < timeoutMs) {
    if (processRef.exitCode !== null) {
      throw new Error(`API process exited before /health became ready with code ${processRef.exitCode}.`)
    }

    try {
      const response = await fetch(`${baseUrl}/health`, { signal: AbortSignal.timeout(500) })
      if (response.ok) return
    } catch {
      // Retry until timeout.
    }

    await new Promise((resolve) => setTimeout(resolve, 200))
  }

  throw new Error(`Timed out waiting for ${baseUrl}/health.`)
}

function collectOutput(processRef) {
  let output = ''
  processRef.stdout?.on('data', (chunk) => {
    output += chunk.toString()
  })
  processRef.stderr?.on('data', (chunk) => {
    output += chunk.toString()
  })
  return () => output.trim()
}

function runWorkflow(baseUrl) {
  const result = spawnSync(
    'uv',
    [
      'run',
      '--project',
      'services/api',
      '--locked',
      'python',
      'examples/literature-review/run_demo.py',
      '--base-url',
      baseUrl,
      '--json'
    ],
    {
      encoding: 'utf8'
    }
  )

  if (result.status !== 0) {
    throw new Error(`Workflow failed:\n${result.stdout}\n${result.stderr}`.trim())
  }

  const summary = JSON.parse(result.stdout)
  if (summary.a2aTaskState !== 'completed') {
    throw new Error(`Expected A2A task to complete, got: ${summary.a2aTaskState}`)
  }
  if (!summary.draftId || !summary.reviewUrl) {
    throw new Error('Workflow did not create a draft.')
  }
  if (!Array.isArray(summary.mcpTools) || !summary.mcpTools.includes('search_documents')) {
    throw new Error('Workflow did not list the expected MCP tools.')
  }
  if (!summary.traceId) {
    throw new Error('Workflow did not report a trace ID.')
  }

  return summary
}

function shutdown(processRef) {
  return new Promise((resolve) => {
    if (processRef.exitCode !== null) {
      resolve()
      return
    }

    const timeout = setTimeout(() => {
      if (processRef.exitCode === null) processRef.kill('SIGKILL')
    }, 5000)

    processRef.once('exit', () => {
      clearTimeout(timeout)
      resolve()
    })
    processRef.kill('SIGTERM')
  })
}

const port = Number(process.env.DEMO_SMOKE_PORT || await freePort())
const baseUrl = `http://127.0.0.1:${port}`
const timeoutMs = Number(process.env.DEMO_SMOKE_TIMEOUT_MS || 15000)
const appTarget = process.env.DEMO_SMOKE_APP || 'agentic_web_demo.main:app'

const api = spawn(
  'uv',
  [
    'run',
    '--project',
    'services/api',
    '--locked',
    'uvicorn',
    '--app-dir',
    'services/api/src',
    appTarget,
    '--host',
    '127.0.0.1',
    '--port',
    String(port)
  ],
  {
    stdio: ['ignore', 'pipe', 'pipe']
  }
)
const apiOutput = collectOutput(api)

try {
  await waitForHealth(baseUrl, api, timeoutMs)
  const summary = runWorkflow(baseUrl)
  console.log(JSON.stringify({
    status: 'ok',
    baseUrl,
    traceId: summary.traceId,
    resultCount: summary.resultCount,
    draftId: summary.draftId
  }, null, 2))
  console.log('Demo smoke check passed.')
} catch (error) {
  console.error(error.message)
  const output = apiOutput()
  if (output) console.error(output)
  process.exitCode = 1
} finally {
  await shutdown(api)
}
