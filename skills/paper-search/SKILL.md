---
name: paper-search
description: Search, download, and extract text from academic papers across arXiv, PubMed, Semantic Scholar, Crossref, OpenAlex, and other scholarly sources. Use when the user asks to find literature, compare search results, resolve a DOI or paper identifier, download a paper PDF, or read paper text through the installed paper-search CLI.
---

# Paper Search

Use the `paper-search` CLI installed from the attributed `openags/paper-search-mcp` dependency. The repository installer renders `{{PAPER_SEARCH_DIR}}` to that dependency's absolute directory.

Before running a command, check that the placeholder was rendered and the directory exists. If `{{PAPER_SEARCH_DIR}}` remains literal, stop and tell the user to rerun the repository installer.

## Command prefix

```bash
uv run --directory "{{PAPER_SEARCH_DIR}}" paper-search
```

Do not assume `paper-search` is globally installed. Use the full prefix so the pinned dependency environment is selected consistently.

## Search

```bash
uv run --directory "{{PAPER_SEARCH_DIR}}" paper-search search "<query>" \
  --max-results <results-per-source> \
  --sources <comma-separated-sources> \
  [--year <year-or-range>]
```

- Default `--max-results` is 5 per source.
- Default `--sources` is `all`. Prefer a focused set such as `arxiv,semantic,crossref,openalex` for an initial pass; broaden only when coverage matters more than latency.
- `--year` filters Semantic Scholar and accepts a year or range such as `2022` or `2020-2024`.
- Search output is JSON. Preserve each result's title, authors, year, source, paper identifier, DOI, and URL when present.

## Download a PDF

```bash
uv run --directory "{{PAPER_SEARCH_DIR}}" paper-search download \
  <source> <paper-id> --save-path "<output-directory>"
```

Report the actual saved path. A metadata hit does not guarantee that a lawful open PDF is available; do not claim a download succeeded until the file exists.

## Read paper text

```bash
uv run --directory "{{PAPER_SEARCH_DIR}}" paper-search read \
  <source> <paper-id> --save-path "<output-directory>"
```

The command downloads the paper when possible and prints extracted text. Treat missing sections, OCR failures, or truncated text as evidence limits. Do not fill a deep paper note from the abstract alone.

## List active sources

```bash
uv run --directory "{{PAPER_SEARCH_DIR}}" paper-search sources
```

Common sources include `arxiv`, `pubmed`, `biorxiv`, `medrxiv`, `google_scholar`, `iacr`, `semantic`, `crossref`, `openalex`, `pmc`, `core`, `europepmc`, `dblp`, `openaire`, `citeseerx`, `doaj`, `base`, `zenodo`, `hal`, `ssrn`, and `unpaywall`. Use the command output as the current authority.

## Credentials

Most sources work without credentials, with lower rate limits where applicable. Optional environment variables include:

- `PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY`
- `PAPER_SEARCH_MCP_IEEE_API_KEY`
- `PAPER_SEARCH_MCP_ACM_API_KEY`

Keep keys in the process environment or an ignored local `.env` file under the dependency directory. Never write a key into this skill, a vault note, a command transcript, or a committed file. Do not print or partially reveal a credential while diagnosing configuration.

## Research workflow

1. Translate the research question into two or three complementary query strings.
2. Search focused sources first.
3. Deduplicate by DOI, then normalized title and author list.
4. Present a compact comparison table and identify review candidates separately from primary studies.
5. Download or read only the papers selected for deeper inspection.
6. Record the exact query and source set when results are filed into a topic plan.

For `ai-wiki`, a systematic search is explicit-only: do not run one merely because a paper needs a topic hub or a hub reaches five linked papers.

## Failure handling

- Missing `uv` or dependency directory: report the missing prerequisite and point to the repository installer.
- Empty or invalid source list: run `sources` and retry with supported names.
- Rate limit: narrow the source set, reduce result count, or wait; do not silently substitute invented results.
- Download unavailable: retain the metadata and URL, label full text unavailable, and ask before trying a different access route.
