---
name: tools
description: Tool selection, fallbacks, and canonical workflows for paper, topic, web, and learning notes
metadata:
  type: spec
updated: 2026-08-21
---

# Tool and Skill Selection

Folder routing lives in `references/vault-guide.md`. This file chooses the tool and defines fallbacks so the core workflow does not depend on optional plugins.

## Decision table

| Input or task | Preferred tool | Fallback |
|---|---|---|
| arXiv ID, DOI, or paper URL | an installed paper-study plugin | `paper-search` to locate and download/read the paper |
| Local paper PDF | an installed PDF-reading or paper-study tool | extract locally available text; if no capable tool exists, report the missing dependency instead of inferring from the abstract |
| Figures or tables in a paper PDF | `paper-figures` | render named full pages with its `--pages` option and crop only after visual verification |
| Web page, article, or repository page | `claude-defuddle` | Claude Code's built-in web fetch when available and appropriate |
| Systematic literature search | `paper-search` | no silent substitute; ask the user to install the dependency if unavailable |
| Search inside the vault | an installed Obsidian search plugin | `rg --files` plus `rg` from the vault root |
| Authored structured diagram | Mermaid | none required; Mermaid is the portable default |
| Freeform diagram | an installed JSON Canvas tool | Mermaid or a saved image |
| Conversation-derived learning note | direct template-based write | none |

Treat plugin names as capabilities, not requirements. Check whether a preferred plugin is actually available before invoking it. Do not claim that an unavailable tool ran.

## Two filing commands — choose before acting

| Command | What it does | When to use |
|---|---|---|
| `/ai-wiki` (default) | Writes one note, requiring at least one wikilink to an **existing** note. **Creates no topic** | Reading a paper, saving a conversation, quick filing |
| `/ai-wiki-full` | The same, plus placement under a topic hub with reciprocal links; a hub is created only after the admission test passes | Explicitly filing under a direction, building or extending a direction map, tidying a topic |

`/ai-wiki` is the default because once the topic count approaches the paper count, hubs organise nothing. The admission test is in `references/note-specs.md` under "What qualifies as a topic".

## New paper note (`/ai-wiki`, default)

1. Resolve `<AI_WIKI>` from vault configuration, defaulting to `0ai_wiki/`.
2. Read the full paper with the preferred paper tool or the fallback above. Do not write a deep note from the abstract alone.
3. Run `paper-figures` when figures or tables materially aid understanding. Save output under `<AI_WIKI>/_attachments/paper-figures/<paper-slug>/` and inspect its JSON manifest.
4. Copy `Templates/paper-note.md` to `Research/papers/<paper-slug>.md` (this command creates no topic, so the note goes at the `papers/` root; `/ai-wiki-full` places it in `papers/<topic-slug>/`), fill it per `references/note-specs.md`, and embed verified figures inline. **The embed prefix depends on depth**: `../../_attachments/` at the root, `../../../_attachments/` inside a topic folder.
   - **S0 "What this paper does, in plain language" and all six quick-card lines must be concrete.** If S0 cannot be written, the paper is not understood — reread before continuing.
   - **Professional wording**: no metaphorical labels; see the wording table in `note-specs.md`.
5. **At least one `[[wikilink]]` to an existing note** — `Glob` `Research/topics/*.md` and `Research/papers/**/*.md` first (papers have per-topic subfolders), link to the nearest, and state the relationship. **This command creates no topic.**
6. If the note fits an existing topic, add the forward link to that topic's S6 list.
7. If this opens active work, add one concise pointer to `.claude/rules/active.md`. This is the only dynamic rules file.

## Place a note under a topic (`/ai-wiki-full`)

Run steps 1-4 and 7 above, then:

1. `Glob` `Research/topics/` and **read S1 of every existing hub**. Filing under an existing topic is the default.
2. If none fits, run the **admission test** (`note-specs.md`): can you name three other papers that belong in it; could it hold 5-15 notes; can no existing hub really hold it? **All three must pass to create one.**
   - On a fail, link to the nearest existing hub and, where useful, add a sub-area row to its S2. **Fine distinctions become sub-areas, not new files.**
   - Count first: a file count in `Research/topics/` close to that of `Research/papers/` means the granularity is already wrong, and the fix is to merge rather than add.
3. On a pass, build the *lightweight companion* hub (`note-specs.md`, "Two modes"). S3 reads "no systematic search run yet"; S4 grows only from this paper's bibliography. **Do not run a search to build a hub.**
4. Move the note into `Research/papers/<topic-slug>/` (creating that folder alongside a new hub) and, if it came from the `papers/` root, change its embed prefix `../../_attachments/` → `../../../_attachments/`. Then link both ways: paper to topic, and topic S4 row plus S6 list to paper.
5. When a lightweight hub reaches five linked papers, recommend upgrading it to a full plan. Recommending is not doing — do not expand or search until the user agrees.
6. Check granularity in passing: merge, upgrade, or split candidates are **proposed**; execution needs the user's agreement.

## Expand a topic without a search

Use this workflow when the user asks to strengthen or organize a topic but does not explicitly ask for a literature search.

1. Expand the existing hub in place; never create a second file for the same topic.
2. Synthesize only linked notes, user-supplied papers, and already-read bibliographies.
3. Keep S3 labelled `no systematic search run yet`.
4. Preserve provenance blocks in S4: **User-supplied** and **From bibliography**. Do not create a **Search hits** block.
5. State the evidence boundary clearly.

## Systematic topic search

**Trigger this workflow only when the user explicitly asks to run a search or systematically explore the topic.** A paper-reading request, a fifth linked paper, or a recommendation to upgrade is not sufficient authorization.

1. Confirm the topic scope and inclusion criteria.
2. Add concrete, verbatim queries to S3.
3. Run `paper-search` for each query.
4. Put actual results in S4's **Search hits** block and record the query that produced each group. Keep **User-supplied** and **From bibliography** separate.
5. Send low-confidence results to `<AI_WIKI>/Inbox/` rather than presenting them as reviewed evidence.
6. Process selected papers with the new-paper workflow and maintain reciprocal links.
7. Update S5 with consensus, contradictions, and gaps. Derive a later search iteration from those gaps only with the user's continued approval.

## New learning note

1. Confirm that the conversation or derivation is worth preserving.
2. Copy `<AI_WIKI>/Templates/learning-note.md` to `Research/learning/<slug>-YYYYMMDD.md`.
3. Fill it per `references/note-specs.md`, especially the verbatim original question and the mandatory worked example.
4. Add at least one meaningful `[[wikilink]]`.

## Web save

1. Use `claude-defuddle` when available; otherwise use the built-in web fetch capability.
2. Verify the extracted title, canonical URL, and main content before saving.
3. Route the note with `references/vault-guide.md` and preserve a `source:` URL in frontmatter.
4. Keep locally downloaded images beside the saved web note unless the same image is curated for reuse across notes.

## When not to reach for a skill

- A one-off script — a single crop, a throwaway regex, one fetch — that will not recur. Run it inline; skills are for workflows that repeat.
- Vault operations the user can do faster by hand in the Obsidian UI.

Building a skill for work that happened once costs more than it saves, and the
unused skill still occupies the selection table afterwards.

## Failure discipline

- If a dependency is missing, say which capability is unavailable and give the user the relevant installer instruction. Do not fabricate results.
- If a PDF section, figure, or web page cannot be read, mark the gap in the note.
- If a tool returns an error or partial output, preserve the error context long enough to diagnose it; do not represent partial output as complete.
