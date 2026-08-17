# research-obsidian-skill

A Claude Code skill suite for turning research papers and conversations into a
well-organized, cross-linked Obsidian knowledge base. Built around one idea:
**every paper gets read once and filed once** — into a structured note with
figures, a verdict, and research openings, linked into a topic hub that turns a
pile of papers into something you can actually learn from.

## What's inside

| Component | What it does |
|---|---|
| `skills/ai-wiki/` | The filing brain. Routes content to the right folder, enforces filename + frontmatter + section specs, embeds figures, and maintains the reciprocal wikilink discipline. Ships with 4 reference docs (routing, note specs, figures, tool selection). |
| `skills/paper-figures/` | Crops named `figN.png` / `tableN.png` out of a paper PDF by caption-region detection, for inline embedding in a note. |
| `skills/paper-search/` | Wrapper for the `paper-search-mcp` CLI (arXiv, PubMed, Semantic Scholar, Crossref, OpenAlex, …) — search, download, and read. |
| `skills/claude-defuddle/` | *(installed, not vendored)* third-party skill for extracting clean markdown from web pages, YouTube, podcasts, and papers. |
| `templates/` | The three note skeletons: `paper-note.md`, `learning-note.md`, `topic-plan.md`. |
| `rules/` | The always-on `.claude/rules/` modules: user profile, permissions, active state. |
| `install/` | Cross-platform installer (`.sh` / `.ps1`). |

## Quick start

```bash
# 1. Clone into the vault you want to manage (or anywhere; the installer asks)
git clone https://github.com/alfredzhang98/research_obsidian_skill.git

# 2. Run the installer — it copies skills into ~/.claude/skills/, sets up
#    the 0ai_wiki/ folder structure, templates, and rules.
cd research_obsidian_skill
./install/install.sh /path/to/your/vault        # macOS / Linux
# or, on Windows:
# .\install\install.ps1 -VaultPath C:\path\to\vault

# 3. Fill in your profile
#    edit <vault>/.claude/rules/my.md
```

The installer is idempotent: re-run it after a `git pull` to refresh skills and
templates. It will not overwrite your `my.md` or `active.md` once they exist.

### Prerequisites

- **Claude Code** with skills enabled.
- **Git** (for cloning `claude-defuddle` and `paper-search-mcp`).
- **Python 3** (the installer creates a `paper-figures` venv with PyMuPDF + Pillow).
- **uv** and **paper-search-mcp** — the installer clones the latter for you; `uv`
  is used to run its pinned environment.

## The workflow it enables

The end-to-end flow the suite is designed for:

```
"read arXiv 2309.06440 for me"
      │
      ▼
claude-paper (or paper-search) ──► paper-figures ──► ai-wiki
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
  topic hub* — never a full literature search. A systematic `paper-search` run
  happens only when you ask for it in so many words.
- **Provenance is preserved.** A topic's reading queue keeps *user-supplied*,
  *bibliography-recommended*, and *search-hit* papers in separate blocks.
- **Figures belong inline.** Extracted figures are embedded where they carry
  the argument, not dumped at the end of the note.
- **Your content never ships.** The repo ships only skills, templates, and
  rules. Real notes, PDFs, and extracted figures are all gitignored, and your
  filled-in `my.md` is excluded so personal information stays local.

## Repository layout

```
research_obsidian_skill/
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── .gitignore
├── .gitattributes
├── skills/
│   ├── ai-wiki/
│   │   ├── SKILL.md
│   │   └── references/{vault-guide,note-specs,figures-diagrams,tools}.md
│   ├── paper-figures/
│   │   ├── SKILL.md
│   │   └── scripts/extract-figures.py
│   └── paper-search/SKILL.md
├── templates/{paper-note,learning-note,topic-plan}.md
├── rules/{my,permissions,active}.md
├── integrations/claude-defuddle/portable.patch
├── install/{install.sh,install.ps1,CLAUDE.template.md,settings.template.json}
└── docs/USER-MANUAL.md
```

The installer renders `{{...}}` placeholders in the skills, rules, and the two
`install/` templates, and writes `CLAUDE.md` + `.claude/settings.json` into your
vault.

## Documentation

- **`docs/USER-MANUAL.md`** — the full command reference: every trigger phrase,
  the `paper-figures` options, the three note types, and the topic-search flow.

## License

MIT. See `LICENSE`. The installer pulls in two third-party dependencies
(`claude-defuddle`, `paper-search-mcp`), each under its own upstream license;
they are not vendored here.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
