---
name: figures-diagrams
description: Figure extraction, inline embedding, Mermaid conventions, and visual-asset routing for research notes
metadata:
  type: spec
updated: 2026-08-18
---

# Figures and Diagrams

Choose the visual workflow by source. Preserve a paper's original figure when it is readable; use Mermaid for a diagram authored specifically for the note.

| Source | Tool | Output |
|---|---|---|
| Figure or table in a paper PDF | `paper-figures` skill | `<AI_WIKI>/_attachments/paper-figures/<paper-slug>/figN.png` or `tableN.png` |
| Diagram authored for the note | Mermaid code fence | inline in the note |
| Freeform markup or whiteboard | Obsidian Canvas if available | `.canvas` file |

## Extract from a PDF

Invoke the installed `paper-figures` skill with the PDF path and this output directory:

```text
<AI_WIKI>/_attachments/paper-figures/<paper-slug>/
```

The skill detects numbered figure and table captions, writes named PNG files, and prints a JSON manifest. Use the manifest to verify the page, caption, and dimensions before embedding anything. If automatic cropping fails, follow the full-page fallback documented by `paper-figures`; do not silently embed a bad crop.

## Embed extracted assets

- Embed a figure in the section where it carries the argument: motivation in S1, pipeline in S3, results or ablations in S6.
- Do not collect all figures at the end of the note.
- Use an interpretive alt label that tells the reader what to inspect and why it matters:

```markdown
![Fig. 3 — the gating branch activates only under high uncertainty](../../../_attachments/paper-figures/<paper-slug>/fig3.png)
```

- Keep the paper note's S10 mapping table current: `Figure | file | embedded section | content`.
- Do not publish or redistribute copyrighted paper figures outside the user's private research context unless the user has the necessary rights.

### The `../` depth is not fixed — the most common way to break a note

Paper notes are stored in per-topic folders (see `references/note-specs.md`, "Filenames"), so the number of `../` segments depends on where the note lives:

| Note location | Embed prefix |
|---|---|
| `Research/papers/<topic-slug>/<slug>.md` (`/ai-wiki-full`, filed under a topic) | `../../../_attachments/paper-figures/<slug>/figN.png` |
| `Research/papers/<slug>.md` (`/ai-wiki`, not yet filed) | `../../_attachments/paper-figures/<slug>/figN.png` |

**When a note moves between those two places — filing it under a topic, or a hub merge or rename — the prefix must be updated in the same edit.** Obsidian resolves `[[wikilinks]]` by filename anywhere in the vault, so moving a note never breaks a link; but markdown image embeds are real relative paths and fail *silently* (the image just does not render, with no error). Spot-check one image after writing or moving a note.

**The attachment tree itself stays flat** — `_attachments/paper-figures/<paper-slug>/`, never mirrored into topic folders. Papers move between topics when hubs merge or get re-filed; the paper-slug does not. Mirroring the topic tree into attachments would manufacture a batch of broken paths on every reorganisation.

## Author diagrams with Mermaid

Obsidian renders Mermaid without an additional plugin. Choose the smallest diagram type that explains the relationship:

| Type | Use for |
|---|---|
| `flowchart` | pipelines, data flow, training stages |
| `sequenceDiagram` | agent-tool interaction and protocols |
| `stateDiagram-v2` | control flow, state machines, training phases |
| `classDiagram` or `erDiagram` | module structure and data schemas |
| `gitGraph` | branching histories or ablation narratives |

Keep node labels short. Use `subgraph` for stages, `-->` for required flow, and `-.->` for data lineage or a non-runtime dependency. Do not redraw a complex paper figure when embedding the original communicates more faithfully.

## Avoid ASCII diagrams

ASCII boxes are fragile across fonts and do not render as structured diagrams in Obsidian. Use Mermaid instead.

## Optional Canvas fallback

If an Obsidian JSON Canvas tool is available, use it for spatial annotation or whiteboard-style work. If it is unavailable, use Mermaid for structured relationships or save a clearly named image under `<AI_WIKI>/_attachments/screenshots/`. Do not require an optional plugin for the core workflow.

## Asset locations

- `<AI_WIKI>/_attachments/paper-figures/<paper-slug>/` — assets used by one paper note. **Stays flat; never mirrored into topic folders** (papers move between topics, the slug does not).
- `<AI_WIKI>/_attachments/screenshots/` — screenshots and ad hoc visual captures.
- `<AI_WIKI>/Research/figures/` — curated visuals reused across multiple notes.
- `claude-defuddle` saves downloaded web images beside its note in an `img/` directory; preserve that local relationship.
