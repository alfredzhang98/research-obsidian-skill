---
name: ai-wiki
description: "Route, write, and file knowledge-base content into the AI-managed vault folder — paper notes (background → prior-art gap → method → experiments → results → limitations & future work → synthesis with research openings), topic plans/MOCs, learning notes, web/design saves, references, daily notes, inbox captures. TRIGGER when the user asks to read up or write up a paper, to save / organize / file / archive anything into the knowledge base, or when a session produced keep-worthy output that needs a home. Owns folder routing, filename and frontmatter specs, figure embedding, and the mandatory wikilink discipline."
---

# ai-wiki — filing content into the knowledge base

Turns "write this up" into a correctly-named, correctly-linked note inside the AI-managed vault folder.

## Where output goes

Throughout this skill, **`<AI_WIKI>`** means the configured AI-managed folder at the vault root. Resolve it once at the start of the task: use the value declared by the vault's `CLAUDE.md` or local rules, otherwise use `0ai_wiki/`. Never create a literal folder named `<AI_WIKI>`. Everything this skill files lands under the resolved folder. That is the point of the skill, not a permission wall.

| Zone | How to treat it |
|---|---|
| `<AI_WIKI>/**` | create / edit / move / rename / delete — free hand |
| every other top-level folder | the user's own notes. Read and search freely; additive edits fine; **ask before** deleting, renaming, moving, or overwriting |
| `.claude/rules/`, `CLAUDE.md` | static configuration; edit only when the user asks to change Claude's behaviour. The sole dynamic exception is `.claude/rules/active.md` |
| `.obsidian/`, `.trash/` | reachable but hands-off — editing Obsidian's own config can break the vault |

Nothing is blocked at the permission layer, so the restraint above is judgement, not a wall. An Obsidian vault is usually not a git repo: a bad overwrite of a hand-written note is only recoverable from whatever cloud version history backs the folder.

Reading *from* those zones and filing a summary into `<AI_WIKI>/` is exactly what this skill is for.

## Reference files — read the one you need, not all four

| File | Read it when |
|---|---|
| `references/vault-guide.md` | deciding **which folder** — full routing table, utterance examples, the tags/wikilinks model |
| `references/note-specs.md` | **writing** a paper note, learning note, or topic plan — filenames, frontmatter, section-by-section spec |
| `references/figures-diagrams.md` | the note needs **figures or a diagram** — extraction command, embedding format, mermaid rules |
| `references/tools.md` | choosing **which skill or CLI** handles the input, plus the end-to-end canonical workflows |

Routine filing (one obvious folder, no figures) needs none of them — the procedure below is enough.

## Procedure

1. **Classify** — pick exactly one destination folder from the routing table in `references/vault-guide.md`. One piece of content maps to one folder; everything cross-cutting rides on `tags:` and `[[wikilinks]]`, never a duplicate copy.
   - Uncommitted / exploratory / batch hits go to `<AI_WIKI>/Inbox/`, not a real folder.
   - Genuinely ambiguous between two folders: ask, do not guess-and-duplicate.
2. **Name** — filename per `references/note-specs.md` (lowercase kebab-case):
   - paper: `Research/papers/<first-author-lastname>-<year>-<2-3-keyword-slug>.md`
   - learning: `Research/learning/<topic-slug>-<YYYYMMDD>.md`
   - topic plan / MOC: `Research/topics/<topic-slug>.md`
3. **Check for an existing note first** — glob the target folder before writing. Updating the right note beats creating a near-duplicate; if a near-duplicate already exists, merge into it and say so.
4. **Fill** — read the matching skeleton in `<AI_WIKI>/Templates/` (`paper-note.md` / `learning-note.md` / `topic-plan.md`) and fill it in place; never rebuild the structure from memory. Section-by-section guidance lives in `references/note-specs.md`, not in the skeleton's `{{...}}` prompts.
   - The template's `> [!callout]` blocks are the emphasis system — keep them, do not invent new ones.
   - The **Quick card** at the top is written **last**: it compresses the finished note. If you cannot fill its six lines, the note is not done.
   - A paper note answers, in order: background (S1) then **what prior work could not do** (S2) then method and math (S3-S4) then what was run (S5) then what came out (S6) then limitations and the authors' future work (S7) then **your synthesis and research openings** (S8).
   - **S2 and S8 are why the note exists.** They are the two sections that must never be filled with generic prose. S4's math must be reconstructible from the note, not merely recognisable.
   - Each S8 opening carries all four lines: opening, why still open, first experiment, which topic it feeds. "No opening worth taking — <why>" is a valid S8; an invented one is not.
   - Read the paper before writing. Never fill a section from the abstract alone; if the PDF text for a section is unavailable, write `Not available in the provided source.` rather than plausible filler.
5. **Figures** — per `references/figures-diagrams.md`: paper figures via the `paper-figures` skill into `<AI_WIKI>/_attachments/paper-figures/<paper-slug>/`, embedded inline at the section where each figure does its work. Authored diagrams go in a mermaid fence. ASCII art is banned.
6. **File it under a topic (mandatory for every paper note)** — a paper with no home never gets found again, and the topic is what turns a pile of papers into something learnable.
   - No matching topic exists: create the **lightweight companion** hub first (see `references/note-specs.md`, "Two modes") — a real summary of the broad direction, 2-4 coarse sub-areas, and 3-5 recommended next reads **taken from the paper's own bibliography**. Roughly ten minutes, roughly forty lines.
   - **Do not over-build it.** No `paper-search` run, no speculative sub-area taxonomy, no invented research plan, no query strings nobody ran. The user asked for a paper to be read; the hub is scaffolding, not the deliverable.
   - A lightweight hub with five or more linked paper notes is mature enough for a full plan. Recommend the upgrade, but do not expand it or run a systematic search until the user explicitly asks.
   - **Systematic search is explicit-only.** Run it only when the user says something equivalent to "run the search for <topic>" or "systematically explore <topic>". Without that request, S3 stays "no systematic search run yet" and S4 grows only from user-supplied papers and bibliographies.
   - **Keep S4's three sources in separate labelled blocks**: user-supplied, bibliography-recommended, search hits (with the query string). Mixing them hides which entries carry the user's own judgement.
   - The link is **reciprocal**: the paper links back to `[[<topic-slug>]]`; the topic's S4 row and S6 list link forward. Both sides, always.
   - Learning notes need at least one `[[wikilink]]` to any existing note; a topic hub is preferred but not required.
7. **Register** — if this opens a new direction or is in-flight work, add a one-line pointer to `.claude/rules/active.md` and bump its `updated:`. Do not mirror detailed state there. `active.md` is the only rules file that this workflow updates without an explicit request to change configuration.

## Self-check before finishing

- [ ] Every path written starts with `<AI_WIKI>/`
- [ ] Filename matches the spec for its note type
- [ ] Frontmatter complete (`tags:` present and specific, not just `research/`)
- [ ] At least one `[[wikilink]]`, reciprocal if filed under a topic plan
- [ ] Built from the actual template file, section order and callouts intact
- [ ] Quick card filled last, and it genuinely stands alone
- [ ] No `{{placeholder}}` left in the delivered note
- [ ] Figures embedded inline, not dumped at the end
- [ ] **Paper note:** S2 names actual prior methods and their specific failure; S7 separates author-stated, mine, and their future work; S8 gives a verdict with evidence and openings that survive the four-line test
- [ ] **Learning note:** S1 is the user's question verbatim; S5 has a real numeric example
- [ ] Told the user the exact path or paths written

## Related

Tool choice per input type: `references/tools.md`. Zone rules in full: `.claude/rules/permissions.md`.
