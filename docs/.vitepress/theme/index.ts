import DefaultTheme from 'vitepress/theme'
import { nextTick, watch } from 'vue'
import { inBrowser, useRoute } from 'vitepress'
import './custom.css'

const WRAPPER_CLASS = 'mermaid-expandable'
const BUTTON_CLASS = 'mermaid-expand-button'
const OVERLAY_CLASS = 'mermaid-fullscreen'

function diagramLabel(diagram: Element) {
  const heading = diagram
    .closest('.vp-doc')
    ?.querySelector('h1, h2, h3')
    ?.textContent
    ?.trim()

  return heading ? `Expand diagram: ${heading}` : 'Expand diagram'
}

function normalizeFullscreenSvg(diagram: HTMLElement) {
  const svg = diagram.matches('svg') ? diagram : diagram.querySelector('svg')
  const viewBox = svg?.getAttribute('viewBox')

  if (!svg || !viewBox) return

  const [, , width, height] = viewBox.split(/\s+/).map(Number)

  if (Number.isFinite(width) && Number.isFinite(height)) {
    svg.setAttribute('width', String(Math.ceil(width)))
    svg.setAttribute('height', String(Math.ceil(height)))
    svg.style.maxWidth = '100%'
    svg.style.maxHeight = '100%'
  }
}

function fitFullscreenSvg(content: HTMLElement) {
  const svg = content.querySelector('svg')
  const viewBox = svg?.getAttribute('viewBox')
  if (!svg || !viewBox) return

  const [, , width, height] = viewBox.split(/\s+/).map(Number)
  const contentRect = content.getBoundingClientRect()
  if (!Number.isFinite(width) || !Number.isFinite(height) || !contentRect.width || !contentRect.height) {
    return
  }

  const svgRatio = width / height
  const contentRatio = contentRect.width / contentRect.height
  svg.style.maxWidth = '100%'
  svg.style.maxHeight = '100%'

  if (svgRatio > contentRatio) {
    svg.style.width = `${Math.floor(contentRect.width)}px`
    svg.style.height = 'auto'
  } else {
    svg.style.width = 'auto'
    svg.style.height = `${Math.floor(contentRect.height)}px`
  }
}

function openFullscreen(diagram: Element) {
  const existingOverlay = document.querySelector(`.${OVERLAY_CLASS}`)
  existingOverlay?.remove()

  const overlay = document.createElement('div')
  overlay.className = OVERLAY_CLASS
  overlay.setAttribute('role', 'dialog')
  overlay.setAttribute('aria-modal', 'true')
  overlay.setAttribute('aria-label', 'Expanded Mermaid diagram')

  const toolbar = document.createElement('div')
  toolbar.className = 'mermaid-fullscreen-toolbar'

  const closeButton = document.createElement('button')
  closeButton.className = 'mermaid-fullscreen-close'
  closeButton.type = 'button'
  closeButton.setAttribute('aria-label', 'Close expanded diagram')
  closeButton.textContent = 'Close'

  const content = document.createElement('div')
  content.className = 'mermaid-fullscreen-content'

  const clone = diagram.cloneNode(true) as HTMLElement
  normalizeFullscreenSvg(clone)
  content.append(clone)

  const close = () => {
    document.removeEventListener('keydown', handleKeyDown)
    window.removeEventListener('resize', handleResize)
    document.body.classList.remove('has-mermaid-fullscreen')
    overlay.remove()
  }

  const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'Escape') close()
  }

  const handleResize = () => fitFullscreenSvg(content)

  closeButton.addEventListener('click', close)
  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) close()
  })
  document.addEventListener('keydown', handleKeyDown)

  toolbar.append(closeButton)
  overlay.append(toolbar, content)
  document.body.append(overlay)
  document.body.classList.add('has-mermaid-fullscreen')
  window.addEventListener('resize', handleResize)
  window.requestAnimationFrame(() => fitFullscreenSvg(content))
  closeButton.focus()
}

function mermaidDiagrams() {
  const diagrams = new Set<Element>()

  document.querySelectorAll('.vp-doc .mermaid').forEach((element) => {
    diagrams.add(element)
  })

  document.querySelectorAll('.vp-doc svg[id^="mermaid-"]').forEach((element) => {
    diagrams.add(element.closest('.mermaid') ?? element)
  })

  return [...diagrams]
}

function enhanceMermaidDiagrams() {
  if (!inBrowser) return

  mermaidDiagrams().forEach((diagram) => {
    if (diagram.closest(`.${WRAPPER_CLASS}`)) return

    const wrapper = document.createElement('div')
    wrapper.className = WRAPPER_CLASS

    const button = document.createElement('button')
    button.className = BUTTON_CLASS
    button.type = 'button'
    button.setAttribute('aria-label', diagramLabel(diagram))
    button.title = 'Expand diagram'
    button.textContent = 'Expand'
    button.addEventListener('click', () => openFullscreen(diagram))

    diagram.before(wrapper)
    wrapper.append(diagram, button)
  })
}

function scheduleMermaidEnhancement() {
  nextTick(() => {
    window.setTimeout(enhanceMermaidDiagrams, 250)
    window.setTimeout(enhanceMermaidDiagrams, 1000)
  })
}

export default {
  extends: DefaultTheme,
  setup() {
    const route = useRoute()

    if (inBrowser) {
      scheduleMermaidEnhancement()
      watch(() => route.path, scheduleMermaidEnhancement)

      if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(() => enhanceMermaidDiagrams())
        nextTick(() => {
          const content = document.querySelector('.VPContent')
          if (content) {
            observer.observe(content, { childList: true, subtree: true })
          }
        })
      }
    }

    return { route }
  }
}
