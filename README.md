<p align="center">
  <img src="docs/assets/social-preview.png" alt="VizReport — Rich Interactive Reports. One File. Zero Dependencies." width="100%">
</p>

<h1 align="center">VizReport</h1>

<p align="center">
  <strong>Rich interactive reports for everyone. One file. Zero dependencies.</strong>
</p>

<p align="center">
  <sub><a href="README.zh-CN.md">中文文档</a> · <a href="https://magicalyu.github.io/vizreport">Live Demo</a></sub>
</p>

---

## What is VizReport?

VizReport is a Claude Code / agent skill that transforms any research, analysis, or project data into a **self-contained interactive HTML report**. No build tools, no CDN dependencies, no server required — just one `.html` file that opens in any modern browser.

**The report IS the demo.** [Click here to experience it live →](https://magicalyu.github.io/vizreport)

## Why VizReport?

| Feature | VizReport | share-html | html-report-skill |
|---------|-----------|------------|-------------------|
| Layout templates | 2 (report + cardwall) | 5 styles | 1 |
| Content block types | 13 (charts, timeline, flow, mindmap...) | Static paragraphs | Static paragraphs |
| Charts (pure SVG, zero-dep) | ✅ bar / hbar / line / donut | ❌ | ❌ |
| Sortable & filterable tables | ✅ 3-state sort + row filter + column filter | ❌ | ❌ |
| TOC navigation | ✅ Sticky tree + collapsible + draggable | ❌ | ❌ |
| Theme | ✅ Light/dark toggle + width slider | Fixed | Fixed |
| Offline (no CDN) | ✅ | ✅ | ❌ |
| QA automation | ✅ Playwright 50+ assertions + impeccable | ❌ | ❌ |

## Quick Start

### Install as Claude Code Skill

```bash
npx skills add MagicalYuYu/vizreport
```

### Generate a Report

Just tell Claude:

> "Turn this research into a visual report"

Or use any agent that supports the skills standard. The agent will:
1. Pick the right layout (narrative → `report`, list → `cardwall`)
2. Generate the data island (JSON)
3. Inject it into a template
4. Run QA gates (optional but recommended)

### Manual Use (No Agent Required)

1. Download `templates/report.template.html`
2. Open it in any text editor
3. Find `<script id="aos-data">` and replace the JSON with your content
4. Save and open in a browser

## Content Blocks

| Block | Use Case |
|-------|----------|
| `h` (level 1/2) | Section headings (auto TOC) |
| `p` | Paragraphs with **bold**, `code`, [links](https://example.com) |
| `ul` | Bullet lists |
| `stats` | KPI cards with numbers |
| `chart` | bar / hbar / line / donut (pure SVG, hover tooltips) |
| `cards` | Mini card grids |
| `table` | Sortable + filterable comparison tables |
| `callout` | Highlighted notes (info / warning / danger / success) |
| `quote` | Block quotes with attribution |
| `img` | Images (local or remote, with fallback) |
| `timeline` | Roadmap / milestone timelines |
| `flow` | Process flows (horizontal ≤4 steps, vertical >4) |
| `mindmap` | Concept maps (HTML/CSS, auto text wrapping) |

## Interactive Features

- **🔍 Search** across titles, tags, and content
- **📊 Sort** tables by clicking headers (3-state: asc → desc → original)
- **📋 Filter** by row keywords or per-column values (Excel-style)
- **📈 Chart hover** shows detailed tooltips with percentages
- **🌲 Collapsible sections** — click any heading to fold/unfold
- **🎨 Theme toggle** — light/dark with persistent preference
- **📏 Width slider** — pixel-precise content width (600–1800px)
- **字号 A+/A−** — 5-step font size with memory
- **🗺️ Draggable TOC** — reposition the sidebar anywhere
- **🖨️ Print-ready** — auto switches to light theme, expands all sections

## Browser Compatibility

| Browser | Support |
|---------|---------|
| Chrome / Edge (2018+) | ✅ Full |
| Firefox (2018+) | ✅ Full |
| Safari (macOS/iOS) | ✅ Full |
| Mobile browsers | ✅ Responsive |
| Offline / air-gapped | ✅ Zero network requests |
| IE 11 | ❌ Not supported |

## Architecture

```
┌─────────────────────────────────────────────┐
│              Single HTML File               │
├─────────────────────────────────────────────┤
│  <script id="aos-data">                     │
│    { meta, blocks: [...] }   ← Your data   │
│  </script>                                  │
│  <style> CSS tokens + themes </style>      │
│  <script> Renderer (vanilla JS) </script>  │
└─────────────────────────────────────────────┘
         No build step · No CDN · No server
```

## Report Index

Generate a searchable index of all your reports:

```bash
python scripts/build_index.py
```

Creates `showcase-index.html` with card/list/detail views, search, pin/hide, and iframe preview.

## License

MIT

---

<p align="center">
  <sub>Built with <a href="https://github.com/MagicalYuYu/vizreport">VizReport</a> itself. The <a href="https://magicalyu.github.io/vizreport">live demo</a> is a VizReport report.</sub>
</p>
