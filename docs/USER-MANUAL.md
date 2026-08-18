# User Manual

The command-and-trigger reference for the research-obsidian skill suite. Read
the README first for the big picture; this is the day-to-day cheat sheet.

## 1. Trigger phrases

`ai-wiki` is the orchestrator. Most of the time you do not invoke it by name —
it triggers when your request means "put this into the knowledge base":

| You say (any of these) | Result |
|---|---|
| "read arXiv 2309.06440" / "study this paper" | paper note, filed under a topic hub |
| "save / organize / file this" / "write this up as a note" / "archive this into the knowledge base" | route + write whatever content is in hand |
| "write up the Kalman derivation we just did" | learning note |
| "turn needle-impedance sensing into a research plan" | full topic plan |
| "dump these 10 arXiv hits somewhere" | Inbox (staging, swept later) |
| "save this GitHub repo / article" | design/web save via `defuddle` |

You can also call it explicitly: `/ai-wiki`.

## 2. Skills, in one line each

| Skill | How to use |
|---|---|
| `ai-wiki` | auto-triggers on filing requests; owns routing + note specs |
| `paper-figures` | runs as part of a paper note; extracts `figN.png` from the PDF |
| `paper-search` | "search for X", "find papers on Y" |
| `defuddle` | auto-triggers on any non-paper URL you want read or saved |

## 3. Reading a paper — the full flow

```
you: "read arXiv 2309.06440"
```

What happens, in order:

1. **Parse** — `claude-paper:study` (or `paper-search read`) downloads and
   extracts the text.
2. **Figures** — `paper-figures` crops `figN.png` / `tableN.png` into
   `<AI_WIKI>/_attachments/paper-figures/<slug>/`.
3. **Note** — `ai-wiki` copies `Templates/paper-note.md` to
   `Research/papers/<first-author>-<year>-<slug>.md` and fills all ten sections.
4. **Topic** — if no topic hub covers the paper, `ai-wiki` creates a
   *lightweight companion* hub first, then links the two reciprocally.
5. **Register** — if it opens a new direction, a one-line pointer lands in
   `.claude/rules/active.md`.

The two sections that carry the note are **§2 (Research gap and novelty)** and
**§8 (Synthesis — my take)**. A note whose §8 gives you no research opening was
not worth writing.

## 4. The three note types

### 4.1 Paper note

- **File:** `Research/papers/<first-author>-<year>-<2-3-keyword-slug>.md`
- **Ten sections:** Quick card · Problem · Gap & novelty · Method · Math ·
  Setup · Results · Limitations & future work · Synthesis (verdict, what
  transfers, research openings, what I'd do differently) · Citation · Figures.
- **Always** links back to its topic hub.

### 4.2 Learning note

- **File:** `Research/learning/<topic-slug>-<YYYYMMDD>.md`
- Triggered by a conversation that produced a keep-worthy concept or derivation.
- **§1 is your question verbatim**, **§5 has a worked numeric example** — both
  mandatory.

### 4.3 Topic plan / MOC

- **File:** `Research/topics/<topic-slug>.md` (living document, no date).
- Two modes:
  - **Lightweight companion** — auto-created when a paper needs a home. ~40
    lines, reads only the paper + its bibliography.
  - **Full research plan** — created only when you explicitly ask to explore a
    direction.

## 5. The topic-search trigger (explicit only)

A systematic literature search **never** starts on its own — not from reading a
paper, not when a hub reaches five papers. It starts only when you say
something equivalent to:

- "run the search for <topic>"
- "systematically explore <topic>"
- "expand this direction"
- "flesh out this topic"

Then `ai-wiki` fills the topic plan's §3 (verbatim `paper-search` queries),
runs them, and files hits into §4's **Search hits** block — always separate
from **User-supplied** and **From bibliography**.

## 6. paper-figures — command reference

```bash
"<python>" "<extract-figures.py>" "<paper.pdf>" "<out-dir>" [options]
```

| Option | Meaning | Default |
|---|---|---|
| `--zoom 2.0` | render zoom (~144 DPI) | 2.0 |
| `--pages 1,4,9` | also render those pages full-page | — |
| `--figures-only` | figures only | — |
| `--tables-only` | tables only | — |
| `--max-fig-height-ratio 0.85` | cap crop height as page fraction | 0.85 |

The script prints a JSON manifest on stdout. **Verify each crop before you embed
it** — the detector is a heuristic, not a semantic parser.

## 7. paper-search — command reference

```bash
uv run --directory "<paper-search-dir>" paper-search <command> [args]
```

| Command | Purpose |
|---|---|
| `search "<q>" --sources arxiv,semantic,crossref,openalex` | literature search |
| `download <source> <id> --save-path <dir>` | fetch a PDF |
| `read <source> <id> --save-path <dir>` | extract text |
| `sources` | list active sources |

Prefer a focused source set over `all`. Record the exact query + source set when
results are filed into a topic plan.

## 8. The rules modules

Three always-on files in `<vault>/.claude/rules/`:

| File | Purpose | You edit it |
|---|---|---|
| `my.md` | who you are, research directions, writing style | once at install, then as needed |
| `permissions.md` | free-hand vs additive-only zones | rarely |
| `active.md` | current focus, in-flight work | Claude maintains it |

`active.md` is the only dynamic one — Claude updates it when you mention current
work. The other two are static spec.

## 9. Folder routing cheat sheet

| Content | Folder (under `<AI_WIKI>/`) |
|---|---|
| A paper you want to study | `Research/papers/` |
| A non-paper URL worth keeping | `Research/designs/` |
| A research direction | `Research/topics/` |
| A concept from a conversation | `Research/learning/` |
| Your own un-vetted idea | `Research/ideas/` |
| A figure reused across notes | `Research/figures/` |
| A project workspace | `Projects/` |
| A permanent reference/cheat sheet | `Resources/references/` |
| Today's journal | `Daily Notes/YYYY-MM-DD.md` |
| Not sure yet | `Inbox/` (sweep weekly) |
| Binary assets | `_attachments/` |
| Valuable but inactive | `Archive/` (explicit only) |

## 10. Troubleshooting

| Problem | Fix |
|---|---|
| A placeholder like `{{PAPER_SEARCH_DIR}}` still appears in a skill | re-run the installer; it renders placeholders |
| `paper-figures` crop is a thin strip | render the page with `--pages N` and crop manually |
| `paper-search` reports missing `uv` | install `uv`, or run from the cloned repo's environment |
| A note has no `[[wikilink]]` | every paper/learning note needs at least one; the hub back-link is mandatory |
| Installer overwrote nothing I cared about | it never overwrites `my.md` / `active.md` once they exist |
