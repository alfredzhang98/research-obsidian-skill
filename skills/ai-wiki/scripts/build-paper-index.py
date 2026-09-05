#!/usr/bin/env python3
"""Build a lookup index of every paper note from their frontmatter.

The index exists so that duplicate detection and "have I read this?" do not
require walking and opening every note. Grepping one file scales; globbing a
tree and reading each file does not.

It is GENERATED, never hand-edited. A hand-maintained index rots the first time
someone forgets to update it, and a rotten index is worse than none because it
is trusted. Regenerate it whenever a paper note is added, moved, or deleted.

Usage:
    python build-paper-index.py <papers-dir> [-o <index-path>]

    <papers-dir>   e.g. <vault>/<AI_WIKI>/Research/papers
    -o             defaults to <papers-dir>/../paper-index.md, i.e. a sibling
                   of papers/ and topics/ so it is never mistaken for a note

Stdlib only: this must run under whatever Python is on PATH, with no install
step and no virtualenv.

Exit status is 0 even when integrity problems are found; the problems are
reported in the index and on stderr so a human decides. Only genuine I/O
failures exit non-zero.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

# Frontmatter keys pulled into the index. Order here is the column order.
WANTED = ("title", "authors", "year", "venue", "arxiv", "doi", "status", "date_added")


def parse_frontmatter(text: str) -> dict[str, str]:
    """Minimal flat YAML frontmatter reader.

    Deliberately not PyYAML: the note frontmatter is flat `key: value` plus two
    bracketed lists, and a stdlib-only script runs anywhere without setup.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not m:
            continue
        value = m.group(2).strip()
        if value[:1] in {'"', "'"} and value[-1:] == value[:1] and len(value) > 1:
            value = value[1:-1]
        out[m.group(1)] = value
    return out


def first_author(raw: str) -> str:
    """'[Jane Doe, John Roe]' -> 'Jane Doe'. Surname-only would lose CJK and
    particle-bearing names, so keep the whole first author."""
    s = raw.strip().lstrip("[")
    return s.split(",")[0].strip(" ]\"'")


def cell(value: str, dash: str = "—") -> str:
    """Table-safe cell: pipes escaped, empty rendered as an em dash."""
    value = (value or "").strip()
    return value.replace("|", "\\|") if value else dash


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("papers_dir", type=pathlib.Path, help="the Research/papers directory")
    ap.add_argument("-o", "--out", type=pathlib.Path, default=None, help="output path (default: ../paper-index.md)")
    args = ap.parse_args()

    papers = args.papers_dir.resolve()
    if not papers.is_dir():
        sys.exit(f"error: not a directory: {papers}")
    out_path = (args.out or papers.parent / "paper-index.md").resolve()

    rows = []
    for path in sorted(papers.rglob("*.md")):
        if path.resolve() == out_path:          # never index the index
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not fm.get("title"):                 # not a paper note
            continue
        # The folder is the topic slug; a note at the papers/ root is unfiled.
        topic = path.parent.name if path.parent != papers else ""
        rows.append({
            "slug": path.stem,
            "topic": topic,
            "author": first_author(fm.get("authors", "")),
            **{k: fm.get(k, "") for k in WANTED},
        })

    # --- integrity checks -------------------------------------------------
    dupes: list[str] = []
    for key, label in (("arxiv", "arXiv"), ("doi", "DOI")):
        seen: dict[str, list[str]] = {}
        for r in rows:
            v = (r.get(key) or "").strip()
            if v:
                seen.setdefault(v, []).append(r["slug"])
        for value, slugs in sorted(seen.items()):
            if len(slugs) > 1:
                dupes.append(f"{label} `{value}` 同时出现在：{', '.join(f'`{s}`' for s in slugs)}")

    keyless = [r["slug"] for r in rows if not (r.get("arxiv") or "").strip() and not (r.get("doi") or "").strip()]
    unfiled = [r["slug"] for r in rows if not r["topic"]]

    # --- render -----------------------------------------------------------
    by_topic: dict[str, int] = {}
    for r in rows:
        by_topic[r["topic"] or "（未归入 topic）"] = by_topic.get(r["topic"] or "（未归入 topic）", 0) + 1
    spread = "、".join(f"{t} {n}" for t, n in sorted(by_topic.items()))

    L = [
        "---",
        "title: \"Paper index（自动生成）\"",
        "type: index",
        "tags: [index]",
        "---",
        "",
        "# Paper index",
        "",
        "> [!warning] 这个文件是**生成**的，不要手动编辑",
        "> 任何手改都会在下次重建时被覆盖。新增、移动或删除 paper note 之后重新生成：",
        "> ```bash",
        "> python .claude/skills/ai-wiki/scripts/build-paper-index.py <AI_WIKI>/Research/papers",
        "> ```",
        "",
        f"共 **{len(rows)}** 篇（{spread}）。",
        "",
        "本表存在的理由是**查重与识别**：给定一个 arXiv ID、DOI 或标题，grep 这一个文件即可，",
        "不需要遍历并打开每一篇笔记。`/ai-wiki` 第 0 步就查这里。",
        "",
        "| 笔记 | 标题 | 一作 · 年 | arXiv | DOI | topic | status |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in sorted(rows, key=lambda r: (r["topic"], r["slug"])):
        L.append(
            f"| [[{r['slug']}]] | {cell(r['title'])} | {cell(r['author'])} · {cell(r['year'])} "
            f"| {cell(r['arxiv'])} | {cell(r['doi'])} | {cell(r['topic'], '（未归入）')} | {cell(r['status'])} |"
        )

    if dupes or keyless or unfiled:
        L += ["", "## 索引自检", ""]
        if dupes:
            L += ["**标识符重复 —— 很可能是同一篇被写了两次：**", ""] + [f"- {d}" for d in dupes] + [""]
        if keyless:
            L += [
                "**既无 arXiv 也无 DOI** —— 这些只能靠一作 + 年份 + 标题查重（老会议论文常见，不算错）：",
                "",
            ] + [f"- [[{s}]]" for s in keyless] + [""]
        if unfiled:
            L += [
                "**尚未归入任何 topic**（`/ai-wiki` 的产出，留在 `papers/` 根目录）：",
                "",
            ] + [f"- [[{s}]]" for s in unfiled] + [""]

    out_path.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")

    print(f"indexed {len(rows)} notes -> {out_path}")
    for d in dupes:
        print(f"  DUPLICATE IDENTIFIER: {d}", file=sys.stderr)
    if keyless:
        print(f"  {len(keyless)} note(s) with neither arXiv nor DOI: {', '.join(keyless)}", file=sys.stderr)
    if unfiled:
        print(f"  {len(unfiled)} note(s) not filed under a topic: {', '.join(unfiled)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
