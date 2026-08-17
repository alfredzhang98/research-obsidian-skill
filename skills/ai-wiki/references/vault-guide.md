---
name: vault-guide
description: All routing — which folder content goes in, with utterance examples and the classification model
metadata:
  type: spec
updated: 2026-08-18
---

# Vault Folder Guide

**Single source of truth for routing.** One piece of content maps to one folder. Cross-cutting concerns ride on YAML `tags:` plus `[[wikilinks]]`, never duplicate folders.

`<AI_WIKI>` below is the AI-managed folder at the vault root (`0ai_wiki/` by default). All paths in the table are relative to it.

## Folder routing

| Folder | For | Use when | Example utterance |
|---|---|---|---|
| `Research/papers/` | Deep per-paper notes (spec: `references/note-specs.md`) | The user has a specific paper (arXiv / PDF / DOI) to study | "read arXiv 2309.06440 for me" then write `<author>-<year>-<slug>.md` |
| `Research/designs/` | Web pages, repos, hardware builds converted to clean markdown | The user points at a non-paper URL worth keeping | "save this GitHub repo into designs" then run `defuddle` and write here |
| `Research/topics/` | Lightweight topic hubs and full topic plans / MOCs (spec: `references/note-specs.md`) | The first paper in a direction needs a home; the user asks for a topic plan; or a lightweight hub reaches 5+ linked papers and is ready for a recommended upgrade | "create a hub for safe robot learning"; run a systematic search only if the user explicitly requests it |
| `Research/learning/` | Conversation-derived understanding (spec: `references/note-specs.md`) | A session produced a keep-worthy concept or derivation | "write up the Kalman derivation we just did as a learning note" |
| `Research/ideas/` | The user's **own** unvetted research ideas — one file per idea, carrying an explicit prior-art-check gate | The user proposes something they might work on, before any literature check confirms it is novel | "record this adaptive-control idea for later" then `<idea-slug>.md`; keep it out of `topics/` until the prior-art check passes |
| `Research/figures/` | Curated figures reused across **multiple** notes | A figure is canonical beyond one paper | (per-paper extracts go to `_attachments/` instead) |
| `Projects/` | Project workspaces (notes, logs, todos) | Actual project work, not literature | "start a project folder for the prototype" |
| `Resources/references/` | Permanent reference material (cheat sheets, glossaries) | Broadly useful, not tied to one paper or topic | "make a probability notation cheat sheet" |
| `Daily Notes/` | Daily journal `YYYY-MM-DD.md`, one per day | "today's summary" / today's progress | — |
| `Inbox/` | Unclassified staging; sweep weekly | Exploratory captures, batch search hits, "triage later" | "dump these 10 arXiv hits somewhere" |
| `Templates/` | Note skeletons — copy and fill, not read for guidance | Starting a note that has a template | — |
| `_attachments/` | Binary assets only, never prose | `paper-figures/<slug>/` per paper; `screenshots/` | — |
| `Archive/` | Valuable but inactive | Explicit "archive X" only — never auto-archive | — |

## Straight-in vs Inbox

- **Straight in** — the user has clearly committed: a paper to read carefully, a design to keep, a learning note from a finished conversation.
- **Via Inbox** — exploratory captures, batch hits, "maybe interesting".

## Classification mental model

Three orthogonal axes; every note uses all three.

1. **Folder** = "what type" — exactly one per note.
2. **`tags:`** = "what subject" — `research/bioimpedance`, `method/grpo` — many per note.
3. **`[[wikilinks]]`** = "what relations" — in the note body.

Want a note in two folders? Pick the dominant folder and use tags plus wikilinks for the rest.

## Linking discipline (the rule that keeps the vault navigable)

Every new paper or learning note must contain at least one `[[wikilink]]` to an existing topic, paper, or learning note. Isolated notes become unfindable — they sit as orphan dots in the graph view and are never reopened. Full naming and linkage rules live in `references/note-specs.md`.

For a direction's first paper, create a lightweight topic hub and link both ways. Once a lightweight hub reaches five linked paper notes, recommend upgrading it to a full topic plan. Recommendation is not authorization to run a systematic literature search; that search remains explicit-only.
