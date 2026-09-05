---
name: ai-wiki-export
description: Package a research topic (its hub, all paper notes filed under it, and the figures those notes embed) into a single zip at a user-specified path. Use when the user asks to export, package, bundle, or zip up a topic to send, archive, or read offline. Requires an explicit destination path.
---

# ai-wiki-export — package one research direction as a zip

```
/ai-wiki-export <destination-path> [topic-slug]
```

Produces a self-contained archive: **the topic hub, every paper note filed under it, and the figures those notes embed**. It reads correctly in any markdown viewer after extraction, images included.

## Arguments

| Argument | Required | Meaning |
|---|---|---|
| `<destination-path>` | **yes** | a directory (the zip is named `<topic>.zip`) or a full `.zip` filename |
| `[topic-slug]` | no | omit it and the topics are listed for the user to choose |

Order is not significant: an argument that looks like a path is the path; one matching a slug in `Research/topics/` is the topic.

## Procedure

### 1. No path given → stop and ask. Never guess.

**This is the most important rule in this skill.** When the user has not written a destination:

- **Do not** default to the working directory, the desktop, somewhere inside the vault, or any other "reasonable-looking" location.
- **Do not** invent a path on the user's behalf.
- Ask: "Where should the archive go?" and offer one or two concrete examples (`D:/exports`, `C:/tmp`) so the answer is cheap to give.

The underlying `export-topic.py` defaults to the current directory when invoked directly from a shell. **This skill overrides that default** and always passes `-o` explicitly. The caller of a slash command usually cannot see what the working directory is, and a 5 MB archive landing silently somewhere is worse than an error.

### 2. No topic given → list them and let the user choose

```bash
python .claude/skills/ai-wiki/scripts/export-topic.py <AI_WIKI> --list
```

Show that table to the user verbatim — it carries paper counts, figure counts, and bundle size. **Do not choose for them**, and confirm even when only one topic exists, unless the user already named the direction in the same sentence.

### 3. Check the destination

- **Directory does not exist** → ask before creating it. Do not silently create nested directories; a typo would leave debris in an unexpected place.
- **A zip of that name already exists** → report its size and modification time, then ask whether to overwrite or rename. **Never overwrite silently.**
- Quote paths containing spaces.

### 4. Export

```bash
python .claude/skills/ai-wiki/scripts/export-topic.py <AI_WIKI> <topic-slug> -o "<full zip path>"
```

Add `--all-figures` when the user wants extracted-but-unembedded crops as well (an archival copy) — but state the size difference first, typically several-fold, and let them decide.

To export every direction at once: `--all -o <directory>`, producing one zip per topic.

### 5. Report

When it finishes, tell the user:

- **full path and size**
- **what is inside**: 1 hub + N paper notes + M figures
- **wikilinks pointing outside the bundle** — the script reports these and the bundle README lists them. They point at notes belonging to other topics and will not open inside this archive. That is expected, not a defect.
- **where to extract**: if the script warned about path length, pass on that on Windows the archive should be extracted somewhere short (e.g. `C:\tmp`), or extraction can fail against the 260-character MAX_PATH limit.

## Archive layout

```
<topic-slug>/
  README.md                            ← manifest, structure, outside links
  Research/topics/<topic>.md           ← the hub; read this first
  Research/papers/<topic>/*.md         ← the paper notes
  _attachments/paper-figures/<slug>/   ← figures each note embeds
```

**The directory depths are deliberate — do not "tidy" them into a flat structure.** Image embeds inside the notes are real relative paths (`../../../_attachments/...`); only the original depth lets them resolve after extraction. Flattening any level breaks every image, and it breaks *silently*.

**Only embedded figures ship by default.** Figure extraction is deliberately over-inclusive — one paper may yield 27 crops of which a note embeds 2 — so whole folders inflate the archive several-fold.

## When not to use this command

- The user wants **one paper**, not a direction → give them that note's path, or send the file directly; no archive needed.
- The user wants a **backup of the whole vault** → that is the file-sync or git story, not this skill.
- The user just wants to **see what a direction contains** → run `--list` or read the hub's S6; do not produce a zip.

## Related

Writing notes: `/ai-wiki` (no topic), `/ai-wiki-full` (filed under a topic).
The script itself: `.claude/skills/ai-wiki/scripts/export-topic.py` (`--help` for full arguments).
