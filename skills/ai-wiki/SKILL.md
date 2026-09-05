---
name: ai-wiki
description: File content into the knowledge base as a single well-formed note, without creating a topic hub. Use when the user asks to write up a paper, save a conversation, or file content into the vault. For topic-hub filing with reciprocal links, use ai-wiki-full instead.
---

# ai-wiki — file content into the knowledge base (lightweight, default)

Turns "write this up" into a correctly named, correctly linked note inside the AI-managed folder.

**This command does not create topics.** It produces one note and requires at least one `[[wikilink]]` to an **existing** note. To place a note under a topic hub with reciprocal links, use `/ai-wiki-full`.

> Why topics are off by default: when every paper gets its own hub, the hub organises nothing — it only gives the paper a longer name. A topic is a research direction, not a paper's subject. The test is in `references/note-specs.md` under "What qualifies as a topic".

## Where output goes

**Everything this skill files lands in the AI-managed folder.**

| Zone | How to treat it |
|---|---|
| AI-managed folder (`<AI_WIKI>/**`) | create / edit / move / rename / delete — free hand |
| The user's own note folders | read and search freely; additive edits fine; **ask before** deleting, renaming, moving, or overwriting |
| `.claude/rules/`, `CLAUDE.md` | static config — edit only when the user asks to change Claude's behaviour; bump `updated:`. The sole dynamic exception is `.claude/rules/active.md` |
| `.obsidian/`, `.trash/` | reachable but hands-off — editing Obsidian's config can break the vault |

Nothing is blocked at the permission layer, so the restraint above is judgement. A vault is usually not a git repo; a bad overwrite of a hand-written note is recoverable only from file-sync version history.

Reading *from* those zones and filing a summary into the AI-managed folder is exactly what this skill is for.

## Reference files — read the one you need, not all four

| File | Read it when |
|---|---|
| `references/vault-guide.md` | deciding **which folder** — routing table, example user phrasings, the tags/wikilinks model |
| `references/note-specs.md` | **writing** a paper note, learning note, or topic plan — filenames, frontmatter, section specs, wording rules |
| `references/figures-diagrams.md` | the note needs **figures** — extraction command, embedding format, mermaid rules |
| `references/tools.md` | choosing **which skill or CLI** handles the input, plus the end-to-end workflows |

Routine filing (one obvious folder, no figures) needs none of them — the procedure below is enough.

## Procedure

1. **Classify** — pick exactly one destination folder from the routing table in `references/vault-guide.md`. One piece of content, one folder; anything cross-cutting rides on `tags:` and `[[wikilinks]]`, never a duplicate copy.
   - Uncommitted, exploratory, or batch hits go to `Inbox/`, not a real folder.
   - Genuinely ambiguous between two folders: ask, do not guess and duplicate.
2. **Name** — per `references/note-specs.md` (lowercase kebab-case):
   - paper → `Research/papers/<first-author-lastname>-<year>-<2-3-keyword-slug>.md` (**this command creates no topic, so the note goes at the root of `papers/`**; `/ai-wiki-full` places it in `papers/<topic-slug>/`)
   - learning → `Research/learning/<topic-slug>-<YYYYMMDD>.md`
3. **Check for an existing note first** — `Glob` the target folder before writing (for papers use `Research/papers/**/*.md`; **note the per-topic subfolders**). Updating the right note beats creating a near-duplicate; if one already exists, merge into it and say so.
4. **Fill** — `Read` the matching skeleton in `Templates/` (`paper-note.md` / `learning-note.md`) and fill it **in place**; never rebuild the structure from memory. Section guidance is in `references/note-specs.md`, not in the skeleton's `{{...}}` prompts.
   - The `> [!callout]` blocks are the emphasis system — keep them, do not add new types.
   - The **quick card at the top is written last**: it compresses the finished note. If its six lines cannot be filled, the note below is not done.
   - **S0 "What this paper does, in plain language" is mandatory**: 3-5 sentences for someone who knows the field basics but has not read this paper. Order: the situation they face, what they built, why it works, what they got. **If you cannot write this section you have not understood the paper — stop and reread rather than continuing.**
   - A paper note answers, in order: S0 plain language → S1 background → **S2 what prior work could not do** → S3-S4 method and maths → S5 what was run → S6 what came out → S7 limitations and the authors' future work → **S8 my analysis and research opportunities**.
   - **S2 and S8 are why the note exists** — neither may be filled with generic prose. S4's maths must be reconstructible from the note, not merely recognisable.
   - Each S8 opportunity carries all four lines (opportunity → why still unsolved → first experiment → which topic it files under). "No opportunity worth taking — <why>" is valid; an invented one is not.
   - **Professional wording**: no metaphorical labels ("this paper's cut", "the verdict", "strongest number"). See the wording table in `references/note-specs.md`. Every judgement must land on specific evidence.
   - Read the paper before writing. Never fill a section from the abstract; if the PDF text for a section is unavailable, write `{{not available in source}}` rather than plausible filler.
5. **Figures** — per `references/figures-diagrams.md`: paper figures via the `paper-figures` skill into `_attachments/paper-figures/<paper-slug>/` (**the attachment tree stays flat, never mirrored into topic folders**), embedded **at the section where each figure does the work**.
   - **The embed prefix depends on the note's depth**: `../../_attachments/...` at the `papers/` root, `../../../_attachments/...` inside `papers/<topic-slug>/`. This is the one thing that fails silently when a note moves — spot-check one image.
   - Authored diagrams use a mermaid fence. ASCII art is banned.
6. **Link (mandatory, at least one)** — the note must carry at least one `[[wikilink]]` to an **existing** note: a hub in `Research/topics/`, another paper note, or a learning note.
   - `Glob` `Research/topics/` and `Research/papers/` first, pick the nearest target, and state the relationship in a sentence rather than dropping a bare link.
   - **This command does not create topics.** If there is genuinely nothing to link to, flag in `.claude/rules/active.md` that this opens a new area and tell the user that `/ai-wiki-full` is the command that builds a hub.
   - When the note does fit an existing topic, add the forward link to that topic's S6 list — reciprocal links are what make the graph cluster.
7. **Register** — if this opens a new direction or is in-flight work, add a one-line pointer to `.claude/rules/active.md` and bump its `updated:`. Do not mirror state there. `active.md` is the only rules file this workflow touches without an explicit request to change configuration.

## Self-check before finishing

- [ ] Every path written is inside the AI-managed folder
- [ ] Filename matches the spec for its note type; a paper note sits at the `papers/` root (this command creates no topic)
- [ ] **Embed prefix matches the note's depth**, and at least one image was spot-checked
- [ ] Frontmatter complete (`tags:` present and specific, not just `research/`)
- [ ] At least one `[[wikilink]]` to an **existing** note, with the relationship stated
- [ ] Built from the actual template file, section order and callouts intact
- [ ] **S0 plain-language summary filled**, without jargon dumping
- [ ] Quick card written last; all six lines are concrete statements and it stands alone
- [ ] No `{{placeholder}}` left in the delivered note
- [ ] **No metaphorical labels**
- [ ] Figures embedded inline, not dumped at the end
- [ ] **Paper note:** S2 names actual prior methods and their specific failure; S7 separates author-stated / mine / their future work; S8's conclusion cites evidence and each opportunity has all four lines
- [ ] **Learning note:** S1 is the user's question verbatim; S5 has a real numeric example
- [ ] Told the user the exact path(s) written

## Related

To create or find a topic hub with reciprocal links, use `/ai-wiki-full`.
Tool choice per input type: `references/tools.md`. Zone rules in full: `.claude/rules/permissions.md`.
