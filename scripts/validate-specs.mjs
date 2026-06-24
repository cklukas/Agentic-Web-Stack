import { execFileSync } from 'node:child_process'
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import Ajv2020 from 'ajv/dist/2020.js'
import addFormats from 'ajv-formats'
import YAML from 'yaml'

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const demoDir = path.join(rootDir, 'specs', 'demo')
const schemasDir = path.join(rootDir, 'specs', 'schemas')
const docsDir = path.join(rootDir, 'docs')

const requiredDemoFiles = [
  'agent-card.json',
  'openapi.yaml',
  'oidc-client.example.json',
  'mcp-tools.json',
  'a2a-message-send.json',
  'agent-registry.yaml',
  'memory.yaml',
  'model-routing.yaml',
  'application-workflow.yaml',
  'evaluation-scenarios.yaml'
]

const schemaMap = {
  'agent-card.json': 'agent-card.schema.json',
  'oidc-client.example.json': 'oidc-client.schema.json',
  'mcp-tools.json': 'mcp-tools.schema.json',
  'a2a-message-send.json': 'a2a-message-send.schema.json',
  'agent-registry.yaml': 'agent-registry.schema.json',
  'memory.yaml': 'memory.schema.json',
  'model-routing.yaml': 'model-routing.schema.json',
  'application-workflow.yaml': 'application-workflow.schema.json',
  'evaluation-scenarios.yaml': 'evaluation-scenarios.schema.json'
}

const errors = []

function readText(filePath) {
  return readFileSync(filePath, 'utf8')
}

function parseSpec(filePath) {
  const raw = readText(filePath)
  if (filePath.endsWith('.json')) {
    return JSON.parse(raw)
  }
  if (filePath.endsWith('.yaml') || filePath.endsWith('.yml')) {
    return YAML.parse(raw)
  }
  throw new Error(`Unsupported spec extension: ${filePath}`)
}

function walkFiles(dir, predicate = () => true) {
  if (!existsSync(dir)) return []

  return readdirSync(dir)
    .flatMap((name) => {
      const filePath = path.join(dir, name)
      const stat = statSync(filePath)
      if (stat.isDirectory()) return walkFiles(filePath, predicate)
      return predicate(filePath) ? [filePath] : []
    })
    .sort()
}

function formatAjvErrors(ajv, validationErrors) {
  return ajv.errorsText(validationErrors, { separator: '\n  ' })
}

function validateRequiredFiles() {
  for (const fileName of requiredDemoFiles) {
    const filePath = path.join(demoDir, fileName)
    if (!existsSync(filePath)) {
      errors.push(`Missing required demo spec: specs/demo/${fileName}`)
    }
  }
}

function validateParseableSpecs() {
  const specFiles = walkFiles(demoDir, (filePath) => /\.(json|ya?ml)$/.test(filePath))
  for (const filePath of specFiles) {
    try {
      parseSpec(filePath)
    } catch (error) {
      errors.push(`Cannot parse ${path.relative(rootDir, filePath)}: ${error.message}`)
    }
  }
}

function validateSchemas() {
  const ajv = new Ajv2020({
    allErrors: true,
    strict: true,
    strictRequired: false,
    allowUnionTypes: true
  })
  addFormats(ajv)

  for (const schemaFile of walkFiles(schemasDir, (filePath) => filePath.endsWith('.json'))) {
    try {
      const schema = parseSpec(schemaFile)
      ajv.compile(schema)
    } catch (error) {
      errors.push(`Invalid schema ${path.relative(rootDir, schemaFile)}: ${error.message}`)
    }
  }

  for (const [demoFile, schemaFile] of Object.entries(schemaMap)) {
    const demoPath = path.join(demoDir, demoFile)
    const schemaPath = path.join(schemasDir, schemaFile)
    if (!existsSync(demoPath) || !existsSync(schemaPath)) continue

    try {
      const schema = parseSpec(schemaPath)
      const data = parseSpec(demoPath)
      const validate = ajv.getSchema(schema.$id) ?? ajv.compile(schema)
      if (!validate(data)) {
        errors.push(
          `Schema validation failed for specs/demo/${demoFile}:\n  ${formatAjvErrors(ajv, validate.errors)}`
        )
      }
    } catch (error) {
      errors.push(`Could not validate specs/demo/${demoFile}: ${error.message}`)
    }
  }

  validateNestedMcpToolSchemas(ajv)
}

function validateNestedMcpToolSchemas(ajv) {
  const mcpToolsPath = path.join(demoDir, 'mcp-tools.json')
  if (!existsSync(mcpToolsPath)) return

  try {
    const toolsList = parseSpec(mcpToolsPath)
    for (const tool of toolsList.result?.tools ?? []) {
      for (const schemaKey of ['inputSchema', 'outputSchema']) {
        if (!tool[schemaKey]) continue
        try {
          ajv.compile(tool[schemaKey])
        } catch (error) {
          errors.push(`Invalid ${schemaKey} for MCP tool "${tool.name}": ${error.message}`)
        }
      }
    }
  } catch (error) {
    errors.push(`Could not validate nested MCP tool schemas: ${error.message}`)
  }
}

function validateOpenApi() {
  const openapiPath = path.join(demoDir, 'openapi.yaml')
  if (!existsSync(openapiPath)) return

  const command = process.platform === 'win32' ? 'npx.cmd' : 'npx'
  try {
    execFileSync(command, ['redocly', 'lint', openapiPath], {
      cwd: rootDir,
      stdio: 'inherit'
    })
  } catch {
    errors.push('Redocly OpenAPI lint failed for specs/demo/openapi.yaml')
  }
}

function validateDocsSpecLinks() {
  const markdownFiles = walkFiles(docsDir, (filePath) => filePath.endsWith('.md'))
  const specLinkPattern = /\/specs\/demo\/[A-Za-z0-9._/-]+\.(?:json|ya?ml)/g

  for (const filePath of markdownFiles) {
    const text = readText(filePath)
    const links = text.match(specLinkPattern) ?? []
    for (const link of links) {
      const targetPath = path.join(rootDir, link.replace(/^\//, ''))
      if (!existsSync(targetPath)) {
        errors.push(`${path.relative(rootDir, filePath)} links to missing spec ${link}`)
      }
    }
  }
}

validateRequiredFiles()
validateParseableSpecs()
validateSchemas()
validateOpenApi()
validateDocsSpecLinks()

if (errors.length > 0) {
  console.error('\nSpec validation failed:')
  for (const error of errors) {
    console.error(`- ${error}`)
  }
  process.exit(1)
}

console.log('Spec validation passed.')
