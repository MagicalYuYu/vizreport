---
name: vizreport
description: "[Feature] Transform research, analysis, or project data into rich interactive HTML reports. Trigger: user says 'make a visual report', 'create a dashboard', 'turn this into a showcase', or delivers list-type research results (6+ items), or complains that Markdown isn't visual enough. Includes template routing, 3-step generation, and QA gates."
---

# VizReport

> v2.0.0 | Transform any content into a self-contained interactive HTML report. One file. Zero dependencies. Works offline in any modern browser.

## Layout Routing (pick a template first)

| Content Type | Template | Asset |
|---|---|---|
| **Narrative report / research** | `report` (sticky TOC + 13 block types) | `assets/report.template.html` |
| **List / catalog / inventory** | `cardwall` (card grid + search/filter/sort) | `assets/cardwall.template.html` |
| Mixed (report + resource list) | `report` with `cards`/`table` blocks | same as report |
| Comparison / evaluation | `report` with `table` + `callout` blocks | same as report |
| **Roadmap / phases** | `report` with `timeline` block | same as report |
| **Process / pipeline** | `report` with `flow` block | same as report |
| **Concept map / structure** | `report` with `mindmap` block | same as report |

**Red lines**: narrative content must NOT be forced into cardwall; >80 items should use a static site generator instead.

## When NOT to Use

| Scenario | Use Instead |
|---|---|
| >80 items or multi-page navigation | Astro Starlight / VitePress |
| Live dashboard (services/monitoring) | Glance / Homepage |
| Computation-embedded documents | Quarto / MyST |
| Real web console | Tabler |
| No browser available / needs git diff | Plain Markdown |

## 3-Step Generation

1. **Copy template** from `assets/` to output directory, rename by topic
2. **Edit data island only**: replace the `<script id="aos-data">` JSON block. Rules:
   - `meta.updated` required (snapshot date)
   - `meta.theme` optional ("light" default, "dark" available)
   - Charts use data from the report itself; percentages must show their base
   - Images: contextual only (the game/section being discussed); prefer local `images/` folder
   - No `</script>` inside the JSON
3. **Run QA gates** (all must pass):
   - `python scripts/qa_smoke.py <file>` → ALL PASS
   - `impeccable detect --json <file>` → exit 0
   - Screenshot review (one round)

## Gotchas

1. **Font sizing**: all rem-based, base 17px. Never use px font-size in new styles
2. **Light theme default**: dark is opt-in via `meta.theme:"dark"`. Status colors auto-darken in light mode
3. **Chip limits**: status >6, tags >8 auto-collapse with "+N" expander
4. **SVG text**: use `pointer-events:none` on SVG text to prevent hover interception
5. **Template batch edits**: always grep-verify anchors before string replacement; verify count after
