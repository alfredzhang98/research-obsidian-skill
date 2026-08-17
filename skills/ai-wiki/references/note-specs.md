---
name: note-specs
description: Filename, frontmatter, and section specs for paper notes, learning notes, and topic research plans
metadata:
  type: spec
updated: 2026-08-18
---

# Note Specs

Covers three note types. Skeletons live in `<AI_WIKI>/Templates/` (copy and fill). This file is the **spec** — how to fill each section well, not a duplicate of the skeleton.

## Shared rules

### Use the template file — do not reconstruct it

Always read the skeleton in `<AI_WIKI>/Templates/` (`paper-note.md` / `learning-note.md` / `topic-plan.md`) and fill it in place. Never rebuild the structure from memory: the templates carry the section order, the `> [!callout]` emphasis blocks, and the table shapes that the rest of the vault is consistent with. If a section genuinely does not apply, keep the heading and write one line saying why — do not silently drop it, or notes stop being comparable side by side.

Obsidian's Templates core plugin points at `<AI_WIKI>/Templates`, so the user inserts these by hand too. Keep them renderable: `{{title}}` and `{{date}}` are substituted by Obsidian on insert; every other `{{...}}` is a fill-in prompt that must be gone from a delivered note.

### Emphasis convention (Obsidian callouts, render natively)

| Marker | Used for |
|---|---|
| `> [!abstract]` | the Quick card / TL;DR block at the top of every note type |
| `> [!question]` | each research opening in paper note S8 |
| `> [!tip]` | the learning note's "the line where it clicks" |
| `<!-- Writing note: ... -->` | **instructions addressed to whoever is filling the template** |

**Callouts are for the reader; HTML comments are for the writer.** Anything that tells the *author* what to do ("do not gloss this section", "this is mandatory", "reciprocal link required") goes in an HTML comment — Obsidian's reading view drops it entirely, so a leaked instruction can never end up looking like a finding. Never render writer guidance as a callout box: a delivered note that lectures the reader about how it should have been written is a bug.

Do not invent new callout types, and do not use them for ordinary prose — the signal dies if everything is a box.

### Filenames (lowercase kebab-case)

- **Paper note** — `<AI_WIKI>/Research/papers/<first-author-lastname>-<year>-<2-3-keyword-slug>.md`
  - First author: last name only, ASCII-folded ("Müller" becomes "muller", "Wang Lin" becomes "wang").
  - Slug: the 2-3 most distinctive title keywords; drop generic words (a, the, novel, deep, learning, based, towards); hyphenate.
  - This slug is **identical** to the `paper-slug` used for figure attachments — see `references/figures-diagrams.md`.
  - Examples: `shaw-2023-leap-hand.md`, `lee-2024-robust-policy.md`.
- **Learning note** — `<AI_WIKI>/Research/learning/<topic-slug>-<YYYYMMDD>.md`
  - topic-slug: 2-4 hyphenated keywords; date is the conversation date.
  - Examples: `kalman-derivation-20260513.md`, `policy-gradient-baseline-20260520.md`.
- **Topic plan / MOC** — `<AI_WIKI>/Research/topics/<topic-slug>.md`
  - topic-slug: 2-3 hyphenated keywords for the research direction; no date, it is a living document.
  - Examples: `safe-robot-learning.md`, `multimodal-state-estimation.md`.

### Mandatory linkage

Every paper or learning note **must** contain at least one `[[wikilink]]` to an existing topic MOC (`Research/topics/`), another paper note, or a learning note. Isolated notes become unfindable. If no relevant link exists, create a topic-MOC stub first; if the note opens a fresh area with no links at all, flag it in `.claude/rules/active.md`.

---

## Paper note

### Frontmatter

```yaml
---
title: "Paper Title"
authors: [Author1, Author2]
year: 2026
venue: ""
arxiv: ""           # optional
code: ""            # optional
date_added: YYYY-MM-DD
tags: [research/robotics, method/state-estimation]
status: read         # or: skim / queued
---
```

### Sections (in order)

0. **Quick card** — a `> [!abstract]` callout directly under the H1, filled **last** (it is a compression of the finished note, not a first draft). Six lines: one-sentence summary / where others got stuck / this paper's cut / strongest number (with units and condition) / what it means for me / verdict. This is what the user reads when reopening the note months later — if it cannot be written in six lines, the note below it is not finished.
1. **Problem and motivation** — the clinical or engineering problem, and why now. One paragraph. Not a paraphrase of the abstract.
2. **Research gap and novelty (do not gloss)** — the most important section. Be specific:
   - *Limitations of prior work* — name specific prior methods and what each fails at; quote the limitation when the paper states it.
   - *The exact gap* — one sharp sentence: "Prior X cannot do Y under Z; this paper does."
   - *Concrete novelty claims* — list each, tagged **Architectural** (structure / sensor / geometry), **Algorithmic** (loss / estimator / control law), or **Experimental** (dataset / in-vivo / benchmark).
   - *Why it stayed open* — the barrier that kept the gap open; this is what lets you judge real advance versus incremental.
3. **Method** — high-level pipeline first (1-3 sentences or a mermaid diagram per `references/figures-diagrams.md`), then each component using the paper's own naming.
4. **Mathematical foundation** — per equation: one line on *what it computes*; a *symbol table* with units and dimensions (e.g. `$x_k \in \mathbb{R}^n$ — state vector (m, m/s)`); one line of *intuition* (how to read it, which term dominates when — enough to reconstruct it, not just recognise it). Obsidian LaTeX: inline `$...$`, display `$$...$$`. Preserve the paper's notation; if you reformulate, say so explicitly.
5. **Experimental setup** — dataset / phantom / animal model, hardware, baselines, metrics, key hyperparameters. Numbers with units.
6. **Key results** — quantitative numbers with units and uncertainty; tables where they help; keep the headline result separate from ablations.
7. **Limitations and future work** — three separately labelled blocks, never merged:
   - *Author-stated limitations* — what the paper admits, in the paper's own framing.
   - *My own observations* — what the paper does **not** admit: unreported baselines, a metric that hides the failure mode, phantom-only validation sold as clinical, n too small for the claimed effect.
   - *Author-stated future work* — what they say comes next. This is the field's published roadmap: anything already on it is a crowded lane, so S8's openings should either avoid it or state why you would win that race.
8. **Synthesis — my take (do not gloss)** — the second reason this note exists (S2 is the first). Prose, not bullets of praise. Four blocks:
   - *Verdict* — 1-2 sentences: real advance or incremental, **and on what evidence** (which result, which ablation). If the novelty is mostly engineering, say so.
   - *What transfers to my work* — concrete and tied to a named direction in the user's configured profile when one exists: what to **borrow** (a method or trick you would reuse as-is), **adapt** (needs modification — say which), and **compare against** (a baseline you must now beat or cite). A bare "relevant to my work" is a failed section.
   - *Research openings* — the payload. Each opening gets four lines:
     `Opening` (one sentence, phrased as something buildable), `Why still open` (what in this paper or the prior art leaves it unresolved — cite S2's gap analysis or S7), `First experiment` (the smallest thing that would falsify it), `Feeds` (the `[[topic-slug]]` it belongs to, or "new direction").
     Cross-check against S7's author-stated future work: an opening already announced there needs an explicit edge, not silence. Two or three sharp openings beat six vague ones; **zero is a legitimate answer** — write "no opening worth taking: <why>" rather than manufacturing one.
   - *What I would do differently* — the methodological critique: the experiment that should have been run, the baseline that should have been included.
9. **Useful citation sentence** — one quotable line plus the full reference.
10. **Paper figures and attachments** — a mapping table `Figure | file | embedded section | content`; extraction per `references/figures-diagrams.md`.

---

## Learning note

### Frontmatter

```yaml
---
title: "Topic"
type: learning-note
source: claude
date: YYYY-MM-DD
tags: [learning, research/<area>]
status: draft       # or: reviewed / archived
---
```

### Sections (in order)

0. **Quick card** — a `> [!abstract]` callout under the H1: what I now understand / where I was stuck / the sentence that unlocked it. Written last.
1. **Original question** — the user's question **verbatim**, so the framing can be recovered later.
2. **Context** — which conversation, paper, or project this came from; what prior knowledge is assumed. One paragraph.
3. **Key concepts** — per concept: a one-line definition plus the line where it *clicks* (an analogy, a contrast with a sibling concept, or a worked unit check — the highest-value line per concept).
4. **Derivation / code** — same math format as paper note S4. Code: a minimum runnable snippet, language-tagged fence, comment only the non-obvious.
5. **Worked example** — at least one concrete numeric example or small experiment. **Mandatory** — generic notes rot fastest.
6. **Pitfalls / common confusions** — first-pass mistakes; sibling concepts that are often conflated. High value per line.
7. **Open questions** — phrased as questions, not as vague topics.
8. **Next to read** — papers, docs, or repos with a link or full citation.

---

## Topic plan / MOC

A **living** Map-of-Content hub that can grow into a full research plan. Create a lightweight hub for the first paper in a direction so that the paper is never orphaned. A user can also request a full plan directly. Every paper and learning note in the direction links back to the same hub.

### Frontmatter

```yaml
---
title: "Topic Name"
type: topic-plan
date_started: YYYY-MM-DD
tags: [topic, research/<area>]
status: active       # or: paused / done
updated: YYYY-MM-DD
---
```

### Sections (in order)

0. **Quick card** — a `> [!abstract]` callout under the H1: central question / the line I am betting on (plus why) / progress. Refresh it on every update — it is the one line the user reads to decide whether to resume this direction.
1. **Scope and central question** — one paragraph: the question this direction answers, and explicit boundaries (what is in, what is deliberately out). Sharp scope produces sharp clusters.
2. **Sub-questions / sub-areas** — decompose into 3-6 sub-areas. Each gets a `research/<area>` or `method/<x>` tag; these become the tag-node sub-clusters in the graph. List the tag next to each sub-area.
3. **Search strategy** — concrete and executable, not vague:
   - Queries to run (verbatim strings for `paper-search`).
   - Sources, venues, and seminal authors to seed from.
   - Time window and inclusion criteria (what makes a hit worth a full note versus Inbox-only).
4. **Reading queue** — the tracker table, updated as work proceeds:

   | Paper | Sub-area | Priority | Status | Note |
   |---|---|---|---|---|
   | first-author year, short title | S2 tag | high/med/low | queued / skim / read | `[[author-year-slug]]` once written |

5. **Synthesis and open questions** — filled progressively as notes accumulate: what the literature agrees on, where it contradicts itself, and the gap the user could exploit. Re-derive new search queries from the gaps here.
6. **Linked notes** — a `[[wikilink]]` list to every paper and learning note in this direction (the MOC hub). Group by sub-area from S2.

### Two modes — pick by what triggered the note

|  | **Lightweight companion** (the common case) | **Full research plan** |
|---|---|---|
| Triggered by | the first paper in a direction needs a home and no topic covers it | the user explicitly asks to develop or systematically explore a direction |
| Effort | ~10 minutes; it rides along with the paper note | its own task; confirm scope with the user first |
| S1 Scope | a real summary of **what this broad direction is about** — the recurring question, why it is hard, what the community currently disagrees on. Written for the user's future self, not as a placeholder | full scope plus explicit in/out boundaries |
| S2 Sub-areas | 2-4, coarse, allowed to be provisional | 3-6, each with its tag, deliberate |
| S3 Search strategy | **skip** — write "no systematic search run yet" | planned verbatim queries, clearly marked unrun until the user explicitly requests execution |
| S4 Reading queue | 3-5 **recommended next reads**, drawn from the paper's own bibliography and clearly marked as such. Do **not** run a literature search to build it | linked notes and known papers; add a **Search hits** block only after an actual user-requested `paper-search` run |
| S5 Synthesis | one honest line: what this single paper suggests, flagged as n=1 | consensus / contradictions / exploitable gap |

**Do not over-build a lightweight companion.** Its job is to give the paper a home and an obvious next read — not to pre-empt a literature review the user has not asked for. When in doubt, less: an honest 40-line hub beats a 200-line speculative plan.

### Promotion and search gates

A lightweight hub with five or more linked paper notes is mature enough for a full plan. Recommend the upgrade at that point, but do not perform it merely because the threshold was reached. Promotion requires the user's agreement, and a systematic literature search requires an explicit search request.

Until the user agrees to expand the hub:

- **S1 stays a summary**, not a scope analysis with in/out boundaries.
- **S2 stays 2-4 coarse sub-areas** — no taxonomy, no per-area status columns, no priority scheme.
- **S3 stays empty** — literally "no systematic search run yet". Never write speculative query strings; a query list nobody ran reads like a plan that exists.
- **S4 grows only from bibliographies**, never from a search.

If the user asks to expand the hub without asking for a search, synthesize only the linked notes, user-supplied papers, and cited bibliographies; keep S3 labelled "no systematic search run yet". If the user explicitly asks to search, run `paper-search` per `references/tools.md`, add the actual queries to S3, and triage the returned papers into S4's **Search hits** block. Never imply that a search ran when it did not.

### S4 provenance — keep the three sources separate

Never merge papers of different provenance into one undifferentiated list. Where an entry came from determines how much it is worth, and mixing them destroys that signal. Use three labelled blocks, omitting any that is empty:

| Block | Contains | Present when |
|---|---|---|
| **User-supplied** | papers the user handed over directly (a link, a PDF, "read this one") | always, if any |
| **From bibliography** | picked out of an already-read paper's reference list — no search was run | the lightweight mode's only growth path |
| **Search hits** | `paper-search` output, with the query string that produced it | only after the user triggered the search |

State each block's origin in one line so a future reader knows which entries carry the user's own judgement and which are the assistant's suggestions.

### Linkage rule (reciprocal, mandatory)

**Every paper note is filed under exactly one topic — no exceptions.** A paper with no home is a paper that will never be found again, and the topic is what makes a cluster of papers legible as a body of understanding rather than a pile.

- Paper note has no matching topic: **create the lightweight companion first**, then write the paper note.
- The paper note links back to `[[<topic-slug>]]`; the topic's S4 row (status plus note link) and S6 list link forward to it. Both directions, always — one missing side and the graph stops clustering.
- A paper that genuinely spans two topics: pick the dominant one for the reciprocal link, and mention the other with a plain `[[wikilink]]`. Never file the same paper under two hubs.
- When the fifth paper is linked to a lightweight hub, recommend promotion to a full plan. Do not create a second topic file, expand the plan, or run a search without the user's approval.
