import { spawnSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import net from 'node:net'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')

const defaultCommands = [
  ['node', '--version'],
  ['npm', '--version'],
  ['uv', '--version'],
  ['python3', '--version']
]

const defaultRequiredFiles = [
  'package.json',
  'services/api/pyproject.toml',
  'services/api/uv.lock',
  'services/api/src/agentic_web_demo/main.py',
  'services/api/data/corpus.json',
  'examples/literature-review/run_demo.py',
  'specs/demo/agent-card.json',
  'specs/demo/agent-registry.yaml',
  'specs/demo/openapi.yaml',
  'specs/demo/mcp-tools.json',
  'specs/demo/a2a-message-send.json'
]

function commandChecks() {
  const override = process.env.DEMO_DOCTOR_COMMANDS
  if (!override) return defaultCommands
  return override
    .split(',')
    .map((entry) => entry.trim().split(/\s+/).filter(Boolean))
    .filter((entry) => entry.length > 0)
}

function requiredFiles() {
  const override = process.env.DEMO_DOCTOR_REQUIRED_FILES
  if (!override) return defaultRequiredFiles
  return override.split(',').map((entry) => entry.trim()).filter(Boolean)
}

function checkCommand([command, ...args]) {
  const result = spawnSync(command, args, { encoding: 'utf8' })
  const output = `${result.stdout}${result.stderr}`.trim().split('\n')[0] ?? ''
  return {
    type: 'command',
    name: [command, ...args].join(' '),
    ok: result.status === 0,
    detail: output || (result.error ? result.error.message : '')
  }
}

function checkFile(relativePath) {
  return {
    type: 'file',
    name: relativePath,
    ok: existsSync(path.join(rootDir, relativePath)),
    detail: path.join(rootDir, relativePath)
  }
}

function checkPort(port) {
  return new Promise((resolve) => {
    const server = net.createServer()
    server.once('error', () => {
      resolve({
        type: 'port',
        name: `127.0.0.1:${port}`,
        ok: true,
        warning: true,
        detail: 'Port is already in use. api:dev may need another port, but demo:smoke uses a free port.'
      })
    })
    server.listen(port, '127.0.0.1', () => {
      server.close(() => {
        resolve({
          type: 'port',
          name: `127.0.0.1:${port}`,
          ok: true,
          detail: 'Port is available.'
        })
      })
    })
  })
}

function printResult(result) {
  const marker = result.ok ? (result.warning ? '[warn]' : '[ok]') : '[fail]'
  console.log(`${marker} ${result.type} ${result.name}: ${result.detail}`)
}

const results = [
  ...commandChecks().map(checkCommand),
  ...requiredFiles().map(checkFile),
  await checkPort(Number(process.env.DEMO_DOCTOR_PORT || 8000))
]

for (const result of results) {
  printResult(result)
}

const failed = results.filter((result) => !result.ok)
if (failed.length > 0) {
  console.error(`Demo doctor found ${failed.length} failing check(s).`)
  process.exit(1)
}

console.log('Demo doctor checks passed.')
