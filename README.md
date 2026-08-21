# research-obsidian-skill

[![skills.sh](https://skills.sh/b/alfredzhang98/research-obsidian-skill)](https://skills.sh/alfredzhang98/research-obsidian-skill)

A Claude Code skill suite that turns research papers and conversations into a
well-organized, cross-linked Obsidian knowledge base. Built around one idea:
**every paper gets read once and filed once** — into a structured note with
figures, a verdict, and research openings, linked into a topic hub that turns a
pile of papers into something you can actually learn from.

```bash
npx skills add alfredzhang98/research-obsidian-skill
```

That installs the skills. To also get the folder skeleton, note templates, and
rules modules, run the full installer below.

## What's inside

| Component | What it does |
|---|---|
| `skills/ai-wiki/` | The filing brain. Routes content to the right folder, enforces filename + frontmatter + section specs, embeds figures, and maintains the reciprocal wikilink discipline. Ships with 4 reference docs (routing, note specs, figures, tool selection). |
| `skills/paper-figures/` | Crops named `figN.png` / `tableN.png` out of a paper PDF by caption-region detection, for inline embedding in a note. |
| `skills/paper-search/` | Wrapper for the `paper-search-mcp` CLI (arXiv, PubMed, Semantic Scholar, Crossref, OpenAlex, …) — search, download, and read. |
| `skills/claude-defuddle/` | *(installed, not vendored)* third-party skill for extracting clean markdown from web pages, YouTube, podcasts, and papers. |
| `templates/` | The three note skeletons: `paper-note.md`, `learning-note.md`, `topic-plan.md`. |
| `rules/` | The always-on `.claude/rules/` modules: user profile, permissions, active state. |
| `install/` | Cross-platform installer (`.sh` / `.ps1`, both wrapping `installer.py`). |

## Using it

`ai-wiki` is the orchestrator, and most of the time you never type its name — it
triggers on any request that means *"put this into the knowledge base"*. Type
`/ai-wiki` when you want to force it, or when your phrasing is ambiguous.

### What goes after `/ai-wiki`

The same thing you would have said in plain language: **what to file**, and
optionally where. There are no flags to memorise.

| You type | What lands on disk |
|---|---|
| `/ai-wiki read arXiv 2309.06440` | `Research/papers/<author>-<year>-<slug>.md` — the ten-section note, figures cropped and embedded inline — plus a lightweight `Research/topics/<topic>.md` hub if nothing covers it yet, linked in both directions |
| `/ai-wiki save https://github.com/foo/bar` | `Research/designs/<repo-slug>.md` — clean markdown via `claude-defuddle`, `source:` URL preserved in frontmatter, downloaded images kept in a sibling `img/` folder |
| `/ai-wiki write up the Kalman derivation we just did` | `Research/learning/kalman-<YYYYMMDD>.md` — §1 is your question verbatim, §5 is a worked numeric example. Both mandatory; a learning note without them is not done |
| `/ai-wiki turn needle impedance sensing into a research plan` | `Research/topics/needle-impedance-sensing.md` — a **full** topic plan: scope with in/out boundaries, 3–6 tagged sub-areas, verbatim search queries |
| `/ai-wiki run the search for tactile RL` | Fills that topic's §3 with the queries actually run and triages the hits into §4's **Search hits** block |
| `/ai-wiki dump these 10 arXiv hits somewhere` | `Inbox/` — staging, swept later. Nothing pretends to be a reviewed note |
| `/ai-wiki file this` (after a long session) | Whatever is in hand gets routed by `references/vault-guide.md` and written to the folder that fits |

Plain-language equivalents work identically — `"read arXiv 2309.06440 for me"`,
`"save this repo"`, `"write that up as a note"`, `"archive this into the
knowledge base"`.

### What you get back

Reading one paper produces two linked files:

```
0ai_wiki/
├── Research/
│   ├── papers/
│   │   └── kang-2026-retaf-tf-gripper.md      ← 10 sections, figures inline
│   └── topics/
│       └── tactile-rl-vla.md                  ← hub; §4 row + §6 entry link back
└── _attachments/paper-figures/
    └── kang-2026-retaf-tf-gripper/
        ├── fig1.png   fig3.png   table2.png
```

The paper note's ten sections run: quick card · problem · **gap and novelty** ·
method · math · setup · results · limitations and future work · **synthesis** ·
citation. The two in bold are why the note exists. §2 must name the actual prior
methods and the specific thing they could not do; §8 must end in a verdict plus
research openings, each carrying four lines — the opening, why it is still open,
the first experiment, and which topic it feeds. `"No opening worth taking —
<why>"` is a legitimate §8. An invented one is not.

### What it will not do on its own

A systematic literature search **never** starts by itself — not from reading a
paper, and not when a hub reaches five papers. It starts only when you ask in so
many words: *"run the search for X"*, *"systematically explore X"*, *"expand
this direction"*. Everything else grows a topic only from bibliographies of
papers already read, and §3 stays labelled `no systematic search run yet`.

This is deliberate. The most common way a filing assistant wastes your attention
is producing a 200-line research plan when you asked it to read one paper.

## Install

```bash
git clone https://github.com/alfredzhang98/research-obsidian-skill.git
cd research-obsidian-skill

./install/install.sh /path/to/your/vault          # macOS / Linux
.\install\install.ps1 -VaultPath C:\path\to\vault # Windows
```

Then fill in your profile at `<vault>/.claude/rules/my.md`.

The installer is idempotent — re-run it after a `git pull` to refresh skills and
templates. It never overwrites `my.md` or `active.md` once they exist, and never
overwrites an existing `CLAUDE.md`.

### Prerequisites

- **Claude Code** with skills enabled
- **Git** — for the pinned `claude-defuddle` and `paper-search-mcp` checkouts
- **Python 3** — the installer builds a `paper-figures` environment with PyMuPDF + Pillow
- **uv** — used to run `paper-search-mcp` in its pinned environment

## Working across several machines

Put the vault in a sync folder — OneDrive, Dropbox, Syncthing, or a git repo of
its own — and the design splits cleanly in two.

**Travels with the vault.** Your notes, `.claude/rules/`, `CLAUDE.md`, the
vault-scoped `ai-wiki` skill, this repository, and `<vault>/.claude/secrets/`
holding your API keys. Nothing here is machine-specific.

**Cannot travel.** The user-scoped skills (`paper-search`, `paper-figures`,
`claude-defuddle`) and their dependencies. Their `SKILL.md` files have absolute
paths rendered into them — interpreter, script, dependency checkout — and the
`paper-figures` virtualenv holds platform-specific binaries. Copying those to a
second machine produces a broken install, not a working one. They are cheap to
regenerate, so regenerate them.

Sync is the normal transport; `git pull` is the backstop for when it lags.

### New machine: hand this to your coding agent

The setup is one command, but you do not have to remember it. Paste this:

```text
This Obsidian vault syncs between my machines, but the machine-scoped half of my
Claude Code skills does not. Please set this machine up.

1. From the vault root, run:
     python research-obsidian-skill/install/installer.py --skip-vault
   (the folder may be named research_obsidian_skill if it arrived by file sync)

2. Verify: ~/.claude/skills/ should now hold paper-search, paper-figures and
   claude-defuddle, and no SKILL.md under it should still contain "{{".

3. Smoke-test the search CLI:
     PYTHONIOENCODING=utf-8 uv run --directory ~/paper-search-mcp \
       paper-search search "bioimpedance needle" -s arxiv -n 1

4. Confirm ~/paper-search-mcp/.env has values. The installer seeds it from
   <vault>/.claude/secrets/paper-search.env when that file exists; if it did not,
   tell me which keys are missing rather than inventing any.

Prerequisites are Python 3, git and uv. If one is missing, tell me — do not
install system software without asking. Report the exact paths you wrote.
```

`--skip-vault` is the important flag: it installs only the machine-scoped half
and leaves the synced vault files alone. Without it, this repo's generic public
copies of `ai-wiki`, `permissions.md` and `settings.json` overwrite the ones you
have tuned. The installer is idempotent — re-run it after every `git pull`.

### API keys

Keys live in `<vault>/.claude/secrets/<name>.env` so they ride along with the
vault and never enter this repository. On install, `<name>.env` is copied to the
matching dependency; an `.env` that already holds values is left untouched, so a
local override always wins.

Today one file is read: **`paper-search.env`** → `~/paper-search-mcp/.env`.
Create it by copying `~/paper-search-mcp/.env.example`, then fill in only what
you need — every key is optional, and the sources that need no key at all
(arXiv, PubMed, Crossref, OpenAlex, bioRxiv, DBLP) are most of the useful ones.

| Key | Get it from | What you lose without it |
|---|---|---|
| `PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY` | [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api) | Semantic Scholar still answers but rate-limits hard; this is the only source that returns citation counts, so it is the one key worth getting |
| `PAPER_SEARCH_MCP_UNPAYWALL_EMAIL` | just your email address | The open-access PDF fallback is skipped entirely — cheapest win on this list |
| `PAPER_SEARCH_MCP_CORE_API_KEY` | [core.ac.uk/services/api](https://core.ac.uk/services/api) | CORE searches are rate-limited and truncated |
| `PAPER_SEARCH_MCP_DOAJ_API_KEY` | [doaj.org/apply-for-api-key](https://doaj.org/apply-for-api-key/) | DOAJ drops to 100 requests/hour |
| `PAPER_SEARCH_MCP_ZENODO_ACCESS_TOKEN`, `..._OPENAIRE_API_KEY`, `..._IEEE_API_KEY`, `..._ACM_API_KEY`, `..._CITESEERX_API_KEY` | each provider | Those specific sources are unavailable; leave blank unless you use them |

Leave a key blank rather than inventing a value — the CLI prints a clear warning
for each unset key at startup and carries on with the sources that work.

> **Do not commit a secrets directory.** `scripts/validate_repo.py` scans every
> text file for GitHub, OpenAI, Google and Semantic Scholar credential shapes,
> plus machine paths, and fails the build on a hit. Run it before pushing.

## The workflow it enables

```
"read arXiv 2309.06440 for me"
      │
      ▼
paper-search ────────────────────► paper-figures ──► ai-wiki
  download + parse                 crop figN.png      file the note
                                                        │
                    ┌───────────────────────────────────┤
                    ▼                                   ▼
          Research/papers/<slug>.md            Research/topics/<slug>.md
          (10-section note w/ figures)         (topic hub, reciprocal link)
```

`ai-wiki` is the orchestrator: it decides the folder, fills the template,
extracts and embeds figures, and — critically — files every paper under a
**topic hub** with a reciprocal `[[wikilink]]`, so the graph view clusters
instead of scattering.

## Key design decisions

- **Two tiers of instruction.** Three lean always-on rules modules (`my`,
  `permissions`, `active`) load every session; the heavy filing rules live in
  the on-demand `ai-wiki` skill, read only when content is actually written.
- **Explicit-only systematic search.** Reading a paper creates a *lightweight
  topic hub* — never a full literature search. Reaching five linked papers earns
  a *recommendation* to upgrade, which is still not authorisation to search.
- **Provenance is preserved.** A topic's reading queue keeps *user-supplied*,
  *bibliography-recommended*, and *search-hit* papers in separate blocks, so you
  can always see which entries carry your own judgement.
- **Tools are capabilities, not requirements.** Every row of the tool table has
  a fallback, and an unavailable tool is reported as missing rather than
  silently substituted or pretended.
- **Figures belong inline.** Extracted figures are embedded where they carry
  the argument, not dumped at the end of the note.
- **Your content never ships.** The repo carries only skills, templates, and
  rules. Notes, PDFs, extracted figures, and your filled-in `my.md` are all
  gitignored.

## Repository layout

```
research-obsidian-skill/
├── README.md            LICENSE            THIRD_PARTY_NOTICES.md
├── skills/
│   ├── ai-wiki/SKILL.md + references/{vault-guide,note-specs,figures-diagrams,tools}.md
│   ├── paper-figures/SKILL.md + scripts/extract-figures.py
│   ├── paper-search/SKILL.md
│   └── claude-defuddle/SKILL.md
├── templates/{paper-note,learning-note,topic-plan}.md
├── rules/{my,permissions,active}.md
├── integrations/claude-defuddle/portable.patch
├── install/{installer.py,install.sh,install.ps1,dependencies.env,
│            CLAUDE.template.md,settings.template.json}
├── scripts/validate_repo.py
└── docs/USER-MANUAL.md
```

`scripts/validate_repo.py` checks required files, skill frontmatter, JSON
validity, relative links, Python syntax, and scans every text file for leaked
credentials and machine paths. Run it before pushing.

## Documentation

**`docs/USER-MANUAL.md`** — the day-to-day cheat sheet: every trigger phrase,
the `paper-figures` options, the three note types, and the topic-search flow.

## License

MIT. See `LICENSE`. The installer pulls in two third-party dependencies
(`claude-defuddle`, `paper-search-mcp`), each under its own upstream license;
they are not vendored here. See `THIRD_PARTY_NOTICES.md`.
