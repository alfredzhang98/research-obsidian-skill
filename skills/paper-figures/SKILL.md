---
name: paper-figures
description: Extract numbered figures and tables from a local academic-paper PDF into named PNG files by detecting caption blocks and cropping the associated page regions. Use when a paper note needs inline figures or tables, when raw page images are not useful, or when the user asks to extract figure-level assets from a PDF.
---

# Paper Figures

Run the bundled extraction script with the interpreter and paths rendered by the repository installer:

```bash
"{{PAPER_FIGURES_PYTHON}}" "{{PAPER_FIGURES_SCRIPT}}" \
  "<paper.pdf>" "<output-directory>" [options]
```

Before running it, verify that `{{PAPER_FIGURES_PYTHON}}` and `{{PAPER_FIGURES_SCRIPT}}` were rendered and that both paths exist. If either placeholder remains literal, stop and tell the user to rerun the repository installer.

For an `ai-wiki` paper note, use:

```bash
"{{PAPER_FIGURES_PYTHON}}" "{{PAPER_FIGURES_SCRIPT}}" \
  "<paper.pdf>" \
  "{{AI_WIKI_DIR}}/_attachments/paper-figures/<paper-slug>"
```

`{{AI_WIKI_DIR}}` is installer-rendered and defaults to `0ai_wiki`. The paper slug must match the paper-note filename without `.md`.

## Options

- `--zoom 2.0` — render zoom; 2.0 is approximately 144 DPI and is the default.
- `--pages 1,4,9` — additionally render selected 1-indexed pages as `page_N_full.png`.
- `--figures-only` — extract figure captions only.
- `--tables-only` — extract table captions only.
- `--max-fig-height-ratio 0.85` — cap the inferred crop height as a fraction of page height.

`--figures-only` and `--tables-only` are mutually exclusive.

## Output contract

The script writes:

- `figN.png` for each detected figure caption.
- `tableN.png` for each detected table caption.
- `page_N_full.png` for requested full pages.
- A JSON manifest on stdout with `pdf`, `out_dir`, `figures`, `tables`, and `full_pages`. Each asset entry includes the file name, source page, caption when applicable, and pixel dimensions.

Capture or inspect the manifest. Confirm that an asset exists and its crop is plausible before embedding it in a note.

## Detection model

Caption matching accepts blocks beginning with `Figure N`, `Fig. N`, or `Table N`.

- For a figure, the script looks above its caption. It prefers overlapping raster-image bounds, falls back to vector drawing bounds, and uses nearby text as a boundary.
- For a table, it looks below its caption and uses horizontal rules plus nearby paragraph text to estimate the table body.
- The height cap prevents a failed inference from silently consuming nearly the whole page.
- Duplicate numbers on later pages receive a `-p<page>` suffix.

This is a heuristic, not a semantic figure parser. Always verify important crops.

## Failure recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| Crop is a thin strip or contains only the caption | caption placement differs from the assumed layout | render the source page with `--pages N`, inspect it, then crop manually |
| Figure top is missing | a nearby text fragment became the upper boundary | render the full page; a larger height cap helps only when the inferred boundary is otherwise correct |
| Table body is missing | the paper places table captions below tables | render the full page and crop manually |
| No captions detected | scanned PDF, unusual labels, or broken text extraction | the script renders the first three pages as a fallback; request the relevant pages explicitly |
| Output is too small | render zoom is insufficient | rerun with a larger `--zoom`, considering memory and file size |

Do not silently replace a failed crop with an unverified full-page image.

## Embed in Obsidian

Place each verified asset in the section where it supports the explanation:

```markdown
![Fig. 2 — the uncertainty gate controls when the correction branch activates](../../_attachments/paper-figures/<paper-slug>/fig2.png)
```

Use interpretive alt text rather than repeating the printed caption. Keep the paper note's figure mapping table synchronized with the actual files.

## Dependencies and rights

The script requires Python, PyMuPDF, and Pillow in the installer-created environment. PyMuPDF and Pillow retain their own licenses; the repository license does not replace them.

Paper figures can be copyrighted even when the PDF is accessible. Use extracted assets for the user's research notes and do not republish them without appropriate permission or a valid exception.
