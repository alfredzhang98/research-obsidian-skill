---
name: note-specs
description: Filename, frontmatter, and section specs for paper notes, learning notes, and topic research plans
metadata:
  type: spec
updated: 2026-09-04
---

# Note Specs

Three note types. Skeletons live in `Templates/` (copy and fill). This file is the **spec** — how to fill each section well, not a duplicate of the skeleton.

## Shared rules

### Use the template file — do not reconstruct it

Always `Read` the skeleton in `Templates/` (`paper-note.md` / `learning-note.md` / `topic-plan.md`) and fill it in place. Never rebuild the structure from memory: the templates carry the section order, the `> [!callout]` emphasis blocks, and the table shapes the rest of the vault is consistent with. If a section genuinely does not apply, keep the heading and write one line saying why — do not silently drop it, or notes stop being comparable side by side.

Obsidian's Templates core plugin points at `Templates/`, so the user inserts these by hand too. Keep them renderable: `{{title}}` and `{{date}}` are substituted by Obsidian on insert; every other `{{...}}` is a fill-in prompt that must be gone from a delivered note.

### Wording requirements (mandatory)

A note is a professional technical document, not an essay. **Do not use metaphorical or slogan-like labels.** Specifically:

| Do not write | Write instead |
|---|---|
| "this paper's cut", "the killer move" | What this paper does / method summary |
| "the verdict", "sentencing" | Conclusion and evidence |
| "strongest number" | Main result |
| "where others got stuck" | Why existing methods fall short |
| "feeds into X" | Files under topic X |
| "what I'd do differently" | Experiments I think should have been run |
| "crushes", "destroys", "blows away" | Use the actual margin: higher by Y points on X |

Every judgement must land on specific evidence. "Works well" and "very innovative" are failed writing; "`Transport` from pixels, 0% to 90% across three seeds" is not.

### Filenames (lowercase kebab-case)

- **Paper note** → `Research/papers/<first-author-lastname>-<year>-<2-3-keyword-slug>.md`
  - First author: last name only, ASCII-folded ("Müller" → "muller", "Wang Lin" → "wang").
  - Slug: the 2-3 most distinctive title keywords; drop generic words (a/the/novel/deep/learning/based/towards); hyphenate.
  - This slug is **identical** to the `paper-slug` used for figure attachments — see `references/figures-diagrams.md`.
  - e.g. `shaw-2023-leap-hand.md`, `zhang-2024-bioz-needle.md`.
  - Use the **publication year** for published papers (the conference or journal year); the arXiv year for preprints.
- **Learning note** → `Research/learning/<topic-slug>-<YYYYMMDD>.md`
  - topic-slug: 2-4 hyphenated keywords; date = conversation date.
  - e.g. `kalman-derivation-20260513.md`, `bioz-front-end-noise-20260520.md`.
- **Topic plan / MOC** → `Research/topics/<topic-slug>.md`
  - topic-slug: 2-3 hyphenated keywords for the research direction; no date (it is a living document).
  - e.g. `bioz-needle-sensing.md`, `us-guided-cvc.md`.

### Linkage requirement

Every paper and learning note **must** contain at least one `[[wikilink]]` to a topic MOC, another paper note, or a learning note. Isolated notes become unfindable.

- `/ai-wiki` (default, lightweight): link to any **existing** note; **do not create a topic**.
- `/ai-wiki-full`: file under a topic per the rules below, with reciprocal links.

If a note opens a genuinely unlinkable new area, flag it in `.claude/rules/active.md` rather than inventing a topic for it.

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
tags: [research/bioimpedance, research/medical-ai]
status: read         # or: skim / queued
---
```

### Sections (in order)

**0. Quick card** — a `> [!abstract]` block directly under the H1, written **last** (it compresses the finished note). Six lines, each a concrete statement:

| Line | Requirement | Counter-example |
|---|---|---|
| Problem being solved | The specific task and conditions | "improves robot performance" |
| Why existing methods fall short | Under what condition prior work fails, and how | "does not work well" |
| **What this paper does** | **Plain-language method: what goes in, what is computed, what comes out. After this line the reader must know what the paper does** | "proposes a new framework" |
| Main result | Metric X to Y + units + condition + who it beats | "results are significant" |
| Conclusion | Real advance / incremental / engineering integration + which result supports it | "very valuable" |
| Use to me | Borrow / adapt / baseline / unrelated | "relevant to my direction" |

**0'. What this paper does, in plain language** — a `## 0.` section below the card, 3-5 sentences. This exists to prevent "I read the note and still do not know what the paper does". Write it for someone who knows the field basics but has not read this paper. Fixed order: **the situation they face → what they built → why it works → what they got**. No jargon dumping; explain each proper noun on first use. **If you cannot write this section you have not understood the paper — stop and reread rather than continuing.**

1. **Problem and motivation** — the clinical or engineering problem, and why now. One paragraph, not a paraphrase of the abstract. Division of labour: S0 covers "what they did", S1 covers "why it is worth doing".
2. **Research gap and novelty** — the most important section, and it must not be vague:
   - *Limitations of prior work* — name specific prior methods and what each fails at; quote the limitation where the paper states it.
   - *The exact gap* — one sharp sentence: "Prior X cannot do Y under Z; this paper does."
   - *Novelty claims* — list each, tagged **Architectural** (structure / sensor / geometry), **Algorithmic** (loss / estimator / control law), or **Experimental** (dataset / in-vivo / benchmark), with a judgement on whether it is genuinely new.
   - *Why the gap stayed open* — the barrier that blocked prior work; this decides real advance versus incremental.
3. **Method** — high-level pipeline first (1-3 sentences or a mermaid diagram per `references/figures-diagrams.md`), then each component using the paper's own naming.
4. **Mathematical foundation** — per equation: one line on *what it computes*; a *symbol table* with units and dimensions (e.g. `$x_k \in \mathbb{R}^n$ — state vector (m, m/s)`); one line on *how to read it* (which term dominates when, what it reduces to in the limit — the bar is reconstruction, not recognition). Obsidian LaTeX: inline `$...$`, display `$$...$$`. Preserve the original notation; if reformulating, say so.
5. **Experimental setup** — dataset / phantom / animal model, hardware, baselines, metrics, key hyperparameters. Numbers with units.
6. **Key results** — quantitative numbers with units and uncertainty; tables where they help; headline separated from ablation.
7. **Limitations and future work** — three separately labelled blocks, never merged:
   - *Author-stated limitations* — in the paper's own framing.
   - *Problems the authors do not mention* — unreported baselines, a metric that hides the failure mode, phantom-only validation sold as clinical, n too small for the claimed effect.
   - *Author-stated future work* — the field's published roadmap; anything already on it is a crowded lane, so S8's opportunities should avoid it or state why you would win that race.
8. **My analysis and judgement** — the second reason this note exists (S2 is the first). Prose, not a list of compliments. Four blocks:
   - *Conclusion and evidence* — 1-2 sentences: real advance or incremental, **and on which result or ablation**. If the novelty is mostly engineering, say so.
   - *What transfers to my work* — concrete, tied to a named direction in `.claude/rules/my.md`: **borrow as-is**, **needs adaptation** (say which part), **use as a baseline** (what you must now beat or cite). A bare "relevant to bioimpedance" is a failed section.
   - *Research opportunities* — the payload. Each gets four lines: `Opportunity` (one sentence, buildable) → `Why it is still unsolved` (point back to S2 or S7) → `First experiment` (the smallest thing that would falsify it) → `Files under topic` (`[[topic-slug]]`, or "no matching direction yet"). Cross-check against S7's author-stated future work: an opportunity already announced there needs an explicit edge. Two or three specific opportunities beat six vague ones; **zero is a legitimate answer** — write "no opportunity worth taking: <why>" rather than manufacturing one.
   - *Experiments I think should have been run* — the methodological critique: the missing experiment, the missing baseline.
9. **Quotable sentence** — one quotable line plus the full reference.
10. **Figures and attachments** — mapping table `Asset | File | Embedded in | Content`; extraction per `references/figures-diagrams.md`.

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

0. **Quick card** — `> [!abstract]` under the H1: what became clear / where the sticking point was / the sentence that resolved it. Written last.
1. **Original question** — the user's question **verbatim**, so the framing can be recovered later.
2. **Context** — which conversation, paper, or project; what prior knowledge is assumed. One paragraph.
3. **Key concepts** — per concept: a one-line definition plus the line where it *clicks* (an analogy, a contrast with a sibling concept, or a worked unit check).
4. **Derivation / code** — same maths format as paper-note S4. Code: minimum runnable snippet, language-tagged fence, comment only the non-obvious.
5. **Worked example** — at least one concrete numeric example or small experiment. **Mandatory** — generic notes rot fastest.
6. **Pitfalls and common confusions** — first-pass mistakes; siblings that are often conflated.
7. **Open questions** — phrased as questions, not vague topics.
8. **What to read next** — papers, docs, or repos with a link or full citation.

---

## Topic plan / MOC

A **living** document: a research-direction plan that doubles as the Map-of-Content hub. It is the cluster nucleus in the graph view — every note in the direction links back to it.

### What qualifies as a topic — read this before creating one

**The most common mistake is treating one paper's subject as a direction.** When the topic count approaches the paper count, the granularity is wrong: the hubs organise nothing and merely give each paper a longer filename.

**A topic is a research direction, not a paper's subject.** Align it with the directions listed in `.claude/rules/my.md`, not with the title of the paper you just read.

**Admission test — all three must pass:**

1. **Can you name three other papers you would actually read that belong in it?** If not, it is not a topic, it is one paper.
2. **Could it hold 5-15 notes without becoming a jumble?** If not, it is too fine and belongs as an S2 sub-area of an existing topic.
3. **Can no existing hub really hold it?** Open and read S1 of each existing hub in `Research/topics/` before answering. **The default action is to file under an existing topic, not to create one.**

**Fine distinctions go in S2 sub-areas, not in new files.** Different angles, method families, and application settings within one direction are all sub-areas. A healthy hub holds 5-15 notes across 3-6 sub-areas. Three hubs of two notes each are always worse than one hub of six notes across three sub-areas.

**Granularity self-check**: after writing S1, ask whether it describes a direction you would invest in for a year or two, or a reworded abstract of one paper. If the latter, do not create it — link the paper note to the nearest existing hub.

**When to merge**: two hubs whose S1 sections substantially overlap, or a hub that has grown by one note in six months. Propose keeping the one with more papers as the primary hub, folding the other's content into its S2 and S6, and reducing the old file to a one-line redirect. Merging is a **proposed action requiring the user's agreement**.

**Creation happens only under `/ai-wiki-full`.** `/ai-wiki` (the default) never creates a topic.

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

0. **Quick card** — `> [!abstract]` under the H1: central question / the line I am betting on (and why) / progress. Refresh on every update — it is the one line the user reads to decide whether to resume this direction.
1. **Scope and central question** — one paragraph: the question this direction answers and its explicit boundaries (what is in, what is deliberately out). Sharp scope, clean clusters.
2. **Sub-questions / sub-areas** — 3-6 of them. Each gets a `research/<area>` or `method/<x>` tag; these become the tag sub-clusters in the graph. **This is where fine distinctions go** — do not split them into separate topic files.
3. **Search strategy** — concrete and executable: verbatim query strings for `paper-search`, seed sources / venues / authors, time window and inclusion criteria.
4. **Reading queue** — the tracker table, updated as work proceeds:

   | Paper | Sub-area | Priority | Status | Note |
   |---|---|---|---|---|
   | first-author year, short title | S2 tag | high/med/low | queued / skim / read | `[[author-year-slug]]` once written |

5. **Synthesis and open questions** — filled progressively: what the literature agrees on, contradictions, the gap you could exploit. Derive the next round of queries from the gaps here.
6. **Linked notes** — `[[wikilink]]` list to every note in this direction (the MOC hub), grouped by S2 sub-area.

### Two modes — pick by what triggered the note

|  | **Lightweight companion** (the common case) | **Full research plan** |
|---|---|---|
| Triggered by | `/ai-wiki-full` was used and the paper passed the admission test | the user describes a direction they want explored systematically |
| Effort | ~10 minutes; rides along with the paper note | its own task; confirm scope with the user first |
| S1 Scope | a real summary of **what the broad direction is about** — the recurring question, why it is hard, where the community disagrees. Written for the user's future self, not as a placeholder | full scope with explicit in/out boundaries |
| S2 Sub-areas | 2-4, coarse, allowed to be provisional | 3-6, each tagged, deliberate |
| S3 Search strategy | **skip** — write "no systematic search run yet" | required, with verbatim queries |
| S4 Reading queue | 3-5 **recommended next reads** from the paper's own bibliography, clearly marked as such. Do **not** run a search to build it | full triage output of an actual `paper-search` run |
| S5 Synthesis | one honest line: what this single paper suggests, flagged as n=1 | consensus / contradictions / exploitable gap |

**Do not over-build a lightweight companion.** Its job is to give the paper a home and an obvious next read, not to pre-empt a literature review the user has not asked for. When in doubt, less: an honest 40-line hub beats a 200-line speculative plan.

### Promotion is user-triggered only

A lightweight hub with five or more linked notes is mature enough for a full plan. **Recommend the upgrade at that point; do not perform it.** Promotion needs the user's agreement, and a systematic literature search needs an explicit search request — the threshold on its own authorises neither.

A hub is promoted **only when the user explicitly asks for the topic search** — "run the search for `<topic>`", "expand this direction", "complete this topic". Until that sentence exists:

- **S1 stays a summary**, not a scope analysis with in/out boundaries.
- **S2 stays 2-4 coarse sub-areas** — no taxonomy, no per-area status columns, no priority scheme.
- **S3 stays empty** — literally "no systematic search run yet". Never write speculative query strings; a query list nobody ran reads like a plan that exists.
- **S4 grows only from bibliographies**, never from a search.

On the trigger, and only then: run `paper-search` per `references/tools.md`, expand S1-S3 properly, triage hits into S4, and flip the mode. Expanding a hub unprompted is the easiest way to waste the user's attention — the paper was the deliverable, not the plan.

**Expanding is not searching.** If the user asks to strengthen or tidy the hub without asking for a search, synthesise only from linked notes, user-supplied papers, and already-read bibliographies; S3 stays "no systematic search run yet" and no search-hits block appears. Never let a note imply a search ran when it did not.

### S4 provenance — keep the three sources separate

Never merge papers of different provenance into one undifferentiated list. Where an entry came from determines how much it is worth, and mixing them destroys that signal. Use three labelled blocks, omitting any that is empty:

| Block | Contains | Present when |
|---|---|---|
| **User-supplied** | papers the user handed over directly (a link, a PDF, "read this") | always, if any |
| **From bibliography** | picked out of an already-read paper's bibliography — no search was run | the lightweight mode's only growth path |
| **Search hits** | `paper-search` output, with the query string that produced it | only after the user triggered the search |

State each block's origin in one line so a future reader knows which entries carry the user's own judgement and which are the assistant's suggestions.

### Linkage rule (reciprocal, mandatory)

**Under `/ai-wiki-full`, every paper note is filed under exactly one topic — no exceptions.** A paper with no home will never be found again, and the topic is what makes a cluster of papers legible as a body of understanding rather than a pile.

- No matching topic → run the **admission test** above. Only on a pass do you create the lightweight companion hub and then write the paper note; **on a fail, link to the nearest existing hub** and explain in S8's "files under topic" why it sits there.
- The paper note links back to `[[<topic-slug>]]`; the topic's S4 row (status + note link) and S6 list link forward. Both directions, always.
- A paper that genuinely spans two topics: pick the dominant one for the reciprocal link and mention the other with a plain `[[wikilink]]`. Never file the same paper under two hubs.
