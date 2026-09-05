---
name: ai-wiki-full
description: File content into the knowledge base and place it under a topic hub with reciprocal links, creating the hub only if it passes the admission test. Use when the user asks to file a paper under a research direction, build or extend a topic map, or organise notes into a topic. For a single note without a hub, use ai-wiki instead.
---

# ai-wiki-full — file a note and place it under a topic

The full version of `/ai-wiki`: write the note as `/ai-wiki` does, then **place it under a research direction** with reciprocal links.

**First read `.claude/skills/ai-wiki/SKILL.md` and run its procedure (steps 1-7)**, then let this file replace step 6 and append step 8. The reference files are shared from `.claude/skills/ai-wiki/references/`; this skill does not duplicate them.

Which command to use:

| Situation | Use |
|---|---|
| Read a paper, save a conversation, file something quickly | `/ai-wiki` |
| Explicitly place a paper under a direction, build or extend a direction map, tidy a topic | `/ai-wiki-full` |

---

## Step 6 (replaced): place under a topic

### 6.1 Search before you build

`Glob` `Research/topics/` and **open and read S1 of every existing hub**. The default action is to **file under an existing topic**.

Only when no existing hub can hold it do you proceed to the admission test.

### 6.2 Admission test — all three must pass to create a new topic

Full criteria in `references/note-specs.md` under "What qualifies as a topic". In short:

1. **Can you name three other papers you would actually read that belong in it?** If not, it is not a topic — it is one paper.
2. **Could it hold 5-15 notes without becoming a jumble?** If not, it is too fine; it belongs as an S2 sub-area of an existing topic.
3. **Can no existing hub really hold it?** Answer only after reading their S1 sections.

**Any one failing means do not create it.** Link the paper note to the nearest existing hub and explain in S8's "files under topic" why it sits there. Where useful, add a sub-area row to that hub's S2 to accommodate it — **fine distinctions become sub-areas, not new files.**

> **A 1:1 ratio is a failure signal.** Count before acting: if the file count in `Research/topics/` approaches that of `Research/papers/`, the granularity is already wrong. The correct action then is to merge, not to add another.

### 6.3 All three pass: build the lightweight companion hub

`Read` `Templates/topic-plan.md`, fill it in place, and follow the **lightweight companion** column of the "Two modes" table in `references/note-specs.md`:

- S1 genuinely summarises what the broad direction is about (the recurring question, why it is hard, where the community disagrees), written for the user's future self.
- S2 gives 2-4 coarse sub-areas, each with a `research/<area>` or `method/<x>` tag.
- S3 says "no systematic search run yet". **Never write speculative query strings.**
- S4 gives 3-5 recommended next reads **taken from this paper's own bibliography**, in clearly labelled provenance blocks (user-supplied / from bibliography / search hits — kept separate).
- S5 is one honest line, flagged as n=1.

**Do not over-build it.** No `paper-search` run, no speculative sub-area taxonomy, no invented research plan, no query strings nobody ran. The user asked for a paper to be read; the hub is scaffolding, not the deliverable. ~10 minutes, ~40 lines.

### 6.4 Put the note in the topic's folder

Paper notes live in per-topic folders: `Research/papers/<topic-slug>/<paper-slug>.md`, where **the folder name is the hub's slug**.

- Filing under an existing topic → write into that existing folder.
- A new hub was created → create `Research/papers/<new-topic-slug>/` alongside it.
- The note was written at the `papers/` root by `/ai-wiki` and is only now being filed → move it into the subfolder **and change its embed prefix from `../../_attachments/` to `../../../_attachments/`**.

After moving a note, **rebuild the index** (`scripts/build-paper-index.py`) so the folder change is reflected in the topic column, and the next duplicate check searches current data.

> **This is the one step in this workflow that fails silently.** `[[wikilinks]]` resolve by filename anywhere in the vault, so moving a note never breaks a link; markdown image embeds are real relative paths, and a wrong depth shows up only as an image that does not render. Spot-check one image after moving. The attachment tree `_attachments/paper-figures/<paper-slug>/` **stays flat and does not follow the topic** — papers change topics, slugs do not.

### 6.5 Reciprocal linking (mandatory)

- The paper note links back to `[[<topic-slug>]]` (in "Related links", and named in S8's "files under topic").
- The topic's **S4 queue row** (status + note link) and **S6 list** link forward, with S6 grouping it under the right S2 sub-area.
- Both directions, always — one missing side and the graph stops clustering.
- A paper that genuinely spans two topics: pick the dominant one for the reciprocal link and mention the other with a plain `[[wikilink]]`. **Never file the same paper under two hubs.**

### 6.6 Five notes is a recommendation threshold, not authorisation

When a lightweight hub reaches five linked notes, **say it is mature enough for a full plan, then stop**. Reaching the threshold authorises nothing: no expansion, no `paper-search`, until the user agrees.

S1-S4 are expanded only when the user **explicitly triggers** the topic search ("run the search for `<topic>`", "expand this direction", "complete this topic"). Absent that, S3 stays "no systematic search run yet" and S4 grows only from bibliographies.

**Expanding is not searching.** "Tidy up this topic" is not a search request: synthesise only from linked notes, user-supplied papers, and already-read bibliographies; open no search-hits block; state the evidence boundary out loud.

---

## Step 8 (appended): granularity maintenance

Each time this command runs, check once and **propose** (do not execute):

- **Merge candidates**: two hubs whose S1 sections substantially overlap, or a hub that has grown by one note in six months. Propose keeping the one with more papers as the primary hub, folding the other's content into its S2 and S6, and reducing the old file to a one-line redirect.
- **Upgrade candidates**: a lightweight hub that has reached five notes.
- **Split candidates**: a hub past roughly 15 notes where one S2 sub-area alone would hold five — only then is splitting justified, and the split-out topic passes the admission test by construction.

Merging, splitting, and upgrading **all require the user's agreement before execution**. Rebuild the index afterwards. When executing, **move the `Research/papers/<topic-slug>/` folder with the hub**: relocate notes from the absorbed folder into the surviving hub's folder and delete the empty directory. Folder-to-folder moves keep the same depth, so embed prefixes do not change.

---

## Self-check (in addition to the `/ai-wiki` checklist)

- [ ] Read S1 of every existing hub before considering a new one
- [ ] If a hub was created, all three admission tests were explicitly passed in the note or the conversation
- [ ] No hub was created merely to house one paper (the 1:1 check)
- [ ] Reciprocal links complete: paper note → topic, and topic S4 row + S6 list → paper note
- [ ] The paper is filed under exactly one hub
- [ ] The note sits in `Research/papers/<topic-slug>/` and its embeds use `../../../_attachments/` (not `../../`), with one image spot-checked
- [ ] A new hub's S3 reads "no systematic search run yet" (unless the user explicitly asked for a search)
- [ ] S4's three provenance blocks are labelled and not merged into one table
- [ ] At the five-note threshold, only a recommendation was given — no unilateral upgrade

## Related

To write a single note without a hub, use `/ai-wiki`.
Full spec: `.claude/skills/ai-wiki/references/note-specs.md`. Tool choice: `.claude/skills/ai-wiki/references/tools.md`.
