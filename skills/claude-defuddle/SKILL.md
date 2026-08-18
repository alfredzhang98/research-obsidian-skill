---
name: defuddle
description: Extract clean Markdown from web pages and supported media URLs with the installed Defuddle integration, optionally saving a structured note and local images into an Obsidian vault. Use when the user provides an article, documentation page, repository page, YouTube URL, Apple Podcasts URL, DOI, or arXiv URL to read, summarize, or archive.
---

# Claude Defuddle

This skill wraps the attributed `spaceage64/claude-defuddle` integration. The repository installer clones the pinned upstream commit, applies the portable patch, and renders the interpreter and script paths below.

Before running a command, verify that `{{DEFUDDLE_PYTHON}}` and `{{DEFUDDLE_SCRIPT}}` were rendered and exist. If either placeholder remains literal, stop and tell the user to rerun the repository installer.

## Extract and present

```bash
"{{DEFUDDLE_PYTHON}}" "{{DEFUDDLE_SCRIPT}}" --url "<url>"
```

Without `--project`, the script prints extracted content instead of writing to a vault. Use that output to answer the user's question. Check the title, canonical URL, and whether the result contains the main content before trusting it.

Supported upstream paths include ordinary web pages, YouTube transcripts, Apple Podcasts transcripts when locally available, and academic papers reached through DOI or arXiv URLs. Availability depends on platform, installed command-line tools, and lawful source access.

## Save to a vault

Set the destination in the process environment, then pass a project path:

```bash
export OBSIDIAN_VAULT_PATH="<absolute-vault-or-ai-wiki-directory>"
"{{DEFUDDLE_PYTHON}}" "{{DEFUDDLE_SCRIPT}}" \
  --url "<url>" \
  --project "<relative-project-path>" \
  --created "<YYYY-MM-DD>" \
  [--filename "<kebab-case-name>"] \
  [--method native|native-md|native-page|googlebot|wayback|archive-is]
```

On PowerShell, set the environment variable for the current process with:

```powershell
$env:OBSIDIAN_VAULT_PATH = "<absolute-vault-or-ai-wiki-directory>"
```

The upstream save layout is `<OBSIDIAN_VAULT_PATH>/<project>/defuddle/<filename>.md`, with downloaded images in a sibling `img/` directory. For `ai-wiki`, set `OBSIDIAN_VAULT_PATH` to the resolved `<AI_WIKI>` directory and use a project such as `Research/designs`.

Treat `--project` as an untrusted relative path. Do not pass `..`, an absolute path, or a path outside the user-approved vault. Confirm the saved path printed by the script.

## Credentials

Use environment variables; never store credentials in a skill, vault note, `CLAUDE.md`, committed file, or command transcript.

- `GEMINI_API_KEY` — Gemini enrichment when the integration is configured for Gemini.
- `OPENAI_API_KEY` — OpenAI-compatible enrichment when configured for OpenAI.
- `DATALAB_API_KEY` — optional cloud PDF-to-Markdown conversion.

The portable patch prefers these variables. It retains the upstream `~/.claude/CLAUDE.md` parser only as a legacy fallback for existing installations; do not add new keys there. Do not print, echo, or partially reveal a credential while diagnosing configuration.

If no provider key is configured, upstream may fall back to a Claude CLI subprocess. Tell the user before invoking a path that can incur paid API or model usage when cost is material or unclear.

## Source-specific handling

### Ordinary web pages

Use automatic mode first. It tries direct Markdown, Defuddle parsing, a Googlebot-style fetch, and archive fallbacks. A fallback result is not automatically complete; verify the content.

### YouTube

The integration uses `yt-dlp` for metadata and captions. If captions are absent or blocked, report that limitation rather than inventing a transcript.

### Apple Podcasts

Transcript extraction depends on a transcript already cached by a supported local Podcasts application. If stderr says the transcript is not cached, show the printed deep link and ask the user to open the episode transcript, then retry only after confirmation. This workflow may be unavailable on non-Apple platforms.

### Papers

DOI and arXiv handling may require `pandoc`, a PDF converter, or a configured cloud service. Prefer lawful open copies. Do not use the tool to bypass access controls or redistribute copyrighted full text.

## Stop conditions

- If stderr asks the user to solve an archive captcha or manually archive a page, stop. Present the exact user-action URL and wait for confirmation before retrying the same command.
- If the retrieved content is empty, obviously truncated, or unrelated, do not save it as a successful capture.
- If a required executable is missing, name it and point to the repository installation guide; do not silently switch to a lower-quality result without saying so.
- If saving would overwrite an existing note or image directory, inspect the target and ask before destructive replacement.

## Optional fallback

If this integration is unavailable and the task only requires reading a standard page, use Claude Code's built-in web fetch capability when available. Preserve the source URL and state which extraction path was used. Do not claim that Defuddle ran when it did not.
