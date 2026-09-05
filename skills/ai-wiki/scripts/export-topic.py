#!/usr/bin/env python3
"""List topics and export one (or all) as a self-contained zip.

A bundle contains the topic hub, every paper note filed under it, and every
figure those notes embed.

The zip MIRRORS THE VAULT LAYOUT rather than flattening it, and that is the
whole trick. A paper note embeds its figures with a real relative path
(`../../../_attachments/paper-figures/<slug>/figN.png`), so if the archive
preserved only the notes, or rearranged them, every image would break. Keeping
`Research/papers/<topic>/` and `_attachments/` at their original depths means
the existing paths resolve unchanged inside the extracted folder -- no
rewriting, and the bundle renders in any markdown viewer, not just Obsidian.

Usage:
    python export-topic.py <ai-wiki-dir> --list
    python export-topic.py <ai-wiki-dir> <topic-slug> [-o out.zip]
    python export-topic.py <ai-wiki-dir> --all [-o outdir]

    <ai-wiki-dir>  the AI-managed folder, e.g. <vault>/0ai_wiki

Stdlib only.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
import zipfile

IMG_RE = re.compile(r"\]\(([^)]*_attachments/[^)]+)\)")
LINK_RE = re.compile(r"\[\[([^\]|#]+)")


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} GB"


def note_title(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r'^title:\s*"?(.+?)"?\s*$', text, re.M)
    return m.group(1) if m else path.stem


def collect(ai: pathlib.Path, topic: str, all_figures: bool = False):
    """Return (hub, notes, assets, missing_assets) for one topic.

    By default only figures actually embedded by a note are shipped. Figure
    extraction is deliberately over-inclusive -- a paper yielding 27 crops of
    which the note embeds 2 is normal -- so packing whole folders inflates a
    bundle several-fold with crops the notes already judged not worth showing.
    `all_figures=True` ships the complete folders for archival copies.
    """
    hub = ai / "Research" / "topics" / f"{topic}.md"
    papers_dir = ai / "Research" / "papers" / topic
    notes = sorted(papers_dir.glob("*.md")) if papers_dir.is_dir() else []
    assets: list[pathlib.Path] = []
    missing: list[str] = []
    for note in notes:
        for rel in IMG_RE.findall(note.read_text(encoding="utf-8")):
            target = (note.parent / rel).resolve()
            if target.is_file():
                assets.append(target)
            else:
                missing.append(f"{note.stem}: {rel}")
    if all_figures:
        for d in {a.parent for a in assets}:
            assets.extend(p for p in d.iterdir() if p.is_file())
    return hub, notes, sorted(set(assets)), missing


def dangling_links(ai: pathlib.Path, notes: list[pathlib.Path], hub: pathlib.Path) -> list[str]:
    """Wikilinks pointing outside this bundle -- reported, not resolved."""
    inside = {p.stem for p in notes} | {hub.stem}
    out: set[str] = set()
    for p in ([hub] if hub.is_file() else []) + notes:
        text = re.sub(r"`[^`\n]*`", "", p.read_text(encoding="utf-8"))
        for name in LINK_RE.findall(text):
            name = name.strip()
            if name and name not in inside and not name.startswith("{{"):
                out.add(name)
    return sorted(out)


def list_topics(ai: pathlib.Path) -> None:
    topics_dir = ai / "Research" / "topics"
    if not topics_dir.is_dir():
        sys.exit(f"error: no Research/topics under {ai}")
    rows = []
    for hub_path in sorted(topics_dir.glob("*.md")):
        hub, notes, assets, _ = collect(ai, hub_path.stem)   # embedded-only: matches the export default
        size = sum(p.stat().st_size for p in notes + assets) + (hub.stat().st_size if hub.is_file() else 0)
        rows.append((hub_path.stem, note_title(hub_path), len(notes), len(assets), size))

    unfiled = [p for p in (ai / "Research" / "papers").glob("*.md")]
    width = max((len(r[0]) for r in rows), default=10)
    print(f"{'TOPIC'.ljust(width)}  {'PAPERS':>6}  {'FIGURES':>7}  {'SIZE':>9}   TITLE")
    for slug, title, n_notes, n_assets, size in rows:
        print(f"{slug.ljust(width)}  {n_notes:>6}  {n_assets:>7}  {human(size):>9}   {title}")
    print()
    print(f"{len(rows)} topic(s). Export one with:  export-topic.py <ai-wiki-dir> <TOPIC>")
    if unfiled:
        print(f"note: {len(unfiled)} paper note(s) at the papers/ root are not filed under any topic "
              f"and are in no bundle: {', '.join(p.stem for p in unfiled)}")


def export(ai: pathlib.Path, topic: str, out: pathlib.Path, all_figures: bool = False) -> int:
    hub, notes, assets, missing = collect(ai, topic, all_figures)
    if not hub.is_file():
        sys.exit(f"error: no topic hub at Research/topics/{topic}.md")
    if not notes:
        print(f"warning: no paper notes under Research/papers/{topic}/", file=sys.stderr)

    dangling = dangling_links(ai, notes, hub)
    root = topic  # every archive member sits under this one folder

    readme = [
        f"# {note_title(hub)}",
        "",
        f"从 Obsidian 知识库导出的 **{topic}** 主题包。",
        "",
        f"- topic hub：1 篇",
        f"- paper notes：{len(notes)} 篇",
        f"- 图片附件：{len(assets)} 个文件" + (
            "（含抽取出来但未嵌入的全部图）" if all_figures else
            "（只含笔记里真正嵌入的图。每篇 §10 里\"抽取出来但没有嵌入的\"未包含 —— "
            "导出时加 `--all-figures` 可一并带上）"),
        "",
        "## 目录结构",
        "",
        "```",
        f"{root}/",
        f"  Research/topics/{topic}.md          ← 主题 hub（先读这个）",
        f"  Research/papers/{topic}/*.md        ← 各篇 paper note",
        f"  _attachments/paper-figures/<slug>/  ← 每篇引用的图",
        "```",
        "",
        "**目录层级是刻意保持的**：笔记里的图片用的是相对路径",
        "（`../../../_attachments/...`），只有维持原有深度，图才能在解压后正常显示。",
        "移动或摊平任何一层都会让图失效。用任意 markdown 阅读器打开均可，不限 Obsidian。",
        "",
    ]
    if dangling:
        readme += [
            "## 指向包外的链接",
            "",
            "以下 `[[wikilink]]` 指向本包**未包含**的笔记（它们属于其他 topic）。",
            "链接本身保留原样，但在这个包里点不开：",
            "",
        ] + [f"- `{d}`" for d in dangling] + [""]
    if missing:
        readme += ["## 缺失的图片", "", "以下嵌图在源库中就找不到文件：", ""] + [f"- `{m}`" for m in missing] + [""]

    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{root}/README.md", "\n".join(readme))
        z.write(hub, f"{root}/Research/topics/{hub.name}")
        for n in notes:
            z.write(n, f"{root}/Research/papers/{topic}/{n.name}")
        for a in assets:
            z.write(a, f"{root}/{a.relative_to(ai).as_posix()}")

    size = out.stat().st_size
    print(f"{out}  ({human(size)})")
    print(f"  hub 1 + notes {len(notes)} + assets {len(assets)}")

    # Windows refuses paths over 260 chars unless long-path support is enabled,
    # and the extraction directory is prepended to every member. Long topic
    # slugs cost double here: the slug appears both as the archive root and
    # again inside Research/papers/<topic>/.
    longest = max((len(n) for n in zipfile.ZipFile(out).namelist()), default=0)
    if longest > 120:
        print(f"  note: longest path inside the archive is {longest} chars; on Windows, extract "
              f"somewhere short (e.g. C:\\tmp) or extraction may fail with MAX_PATH", file=sys.stderr)
    if dangling:
        print(f"  {len(dangling)} wikilink(s) point outside the bundle (listed in README)", file=sys.stderr)
    if missing:
        print(f"  {len(missing)} embedded image(s) missing from the vault itself", file=sys.stderr)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ai_wiki_dir", type=pathlib.Path)
    ap.add_argument("topic", nargs="?", help="topic slug to export")
    ap.add_argument("--list", action="store_true", help="list topics with paper/figure counts and size")
    ap.add_argument("--all", action="store_true", help="export every topic")
    ap.add_argument("--all-figures", action="store_true",
                    help="also ship extracted-but-unembedded crops (much larger archives)")
    ap.add_argument("-o", "--out", type=pathlib.Path, default=None)
    args = ap.parse_args()

    ai = args.ai_wiki_dir.resolve()
    if not ai.is_dir():
        sys.exit(f"error: not a directory: {ai}")

    if args.list or (not args.topic and not args.all):
        list_topics(ai)
        return 0

    if args.all:
        outdir = args.out or pathlib.Path.cwd() / "topic-bundles"
        for hub_path in sorted((ai / "Research" / "topics").glob("*.md")):
            export(ai, hub_path.stem, outdir / f"{hub_path.stem}.zip", args.all_figures)
        return 0

    return export(ai, args.topic, args.out or pathlib.Path.cwd() / f"{args.topic}.zip", args.all_figures)


if __name__ == "__main__":
    raise SystemExit(main())
