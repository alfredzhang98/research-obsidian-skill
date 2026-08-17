#!/usr/bin/env python3
"""
Extract real figures and tables from a paper PDF by caption-region detection.

Algorithm:
  1. Open PDF with pymupdf.
  2. For each page, find caption blocks ("Figure N:", "Fig. N:", "Table N:").
  3. Infer figure bounding box: the rect ABOVE the caption, within the caption's
     column, clipped at the nearest text-block edge or page margin.
  4. Render the page at the requested zoom, crop the bbox, save as figN.png /
     tableN.png. Filenames are deduplicated across pages.

Falls back to rendering full pages (page_N_full.png) when no caption is found
or when --pages is given.

Usage:
  python extract-figures.py <pdf> <out-dir> [--zoom 2.0] [--pages 1,4,9]
                                            [--figures-only | --tables-only]
                                            [--max-fig-height-ratio 0.85]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: pymupdf not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(2)

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(2)


CAPTION_RE = re.compile(
    # "Figure 1:", "Fig. 1.", and Springer/Nature style "Fig. 1 Caption text"
    # (no colon/period after the number). \b after the digits keeps it anchored
    # to caption-start blocks while accepting a plain space separator.
    r"^\s*(Figure|Fig\.?|Table)\s+(\d+)\b",
    re.IGNORECASE,
)


def find_captions(page):
    """Return {kind, number, bbox, text} dictionaries for figure/table captions."""
    blocks = page.get_text("blocks")  # (x0, y0, x1, y1, text, block_no, block_type)
    caps = []
    for block in blocks:
        if len(block) < 5:
            continue
        x0, y0, x1, y1, text = block[0], block[1], block[2], block[3], block[4]
        if not isinstance(text, str):
            continue
        match = CAPTION_RE.match(text)
        if not match:
            continue
        kind = "table" if match.group(1).lower().startswith("table") else "fig"
        number = int(match.group(2))
        caps.append(
            {
                "kind": kind,
                "number": number,
                "bbox": (x0, y0, x1, y1),
                "text": text[:140].replace("\n", " "),
            }
        )
    return caps


def _image_bboxes_above(page, caption_bbox, col_x0, col_x1):
    """Return image bboxes above the caption that overlap the caption column."""
    _, cy0, _, _ = caption_bbox
    out = []
    for image in page.get_images(full=True):
        xref = image[0]
        try:
            rects = page.get_image_rects(xref)
        except Exception:
            continue
        for rect in rects:
            if rect.y1 > cy0 + 2:
                continue
            if rect.x1 < col_x0 or rect.x0 > col_x1:
                continue
            if (rect.x1 - rect.x0) < 6 or (rect.y1 - rect.y0) < 6:
                continue
            out.append((rect.x0, rect.y0, rect.x1, rect.y1))
    return out


def _vector_bbox_above(page, caption_bbox, col_x0, col_x1):
    """Return the union of vector-drawing bboxes above a figure caption."""
    _, cy0, _, _ = caption_bbox
    page_h = page.rect.height
    xs0, ys0, xs1, ys1 = None, None, None, None
    try:
        drawings = page.get_drawings()
    except Exception:
        return None
    for drawing in drawings:
        rect = drawing.get("rect")
        if rect is None:
            continue
        rx0, ry0, rx1, ry1 = rect.x0, rect.y0, rect.x1, rect.y1
        if ry1 > cy0 + 2:
            continue
        if rx1 < col_x0 or rx0 > col_x1:
            continue
        if (rx1 - rx0) * (ry1 - ry0) < 200:
            continue
        if xs0 is None:
            xs0, ys0, xs1, ys1 = rx0, ry0, rx1, ry1
        else:
            xs0 = min(xs0, rx0)
            ys0 = min(ys0, ry0)
            xs1 = max(xs1, rx1)
            ys1 = max(ys1, ry1)
    if xs0 is None:
        return None
    if (ys1 - ys0) < 0.05 * page_h:
        return None
    return (xs0, ys0, xs1, ys1)


def infer_figure_rect(page, caption, max_height_ratio=0.85, kind="fig"):
    """
    Return the bbox enclosing the figure or table referred to by caption.

    Figures are assumed to sit above their captions. Tables are assumed to sit
    below their captions. Raster bounds, vector bounds, and nearby text blocks
    constrain each inferred region.
    """
    cx0, _, cx1, _ = caption["bbox"]
    page_rect = page.rect
    page_w = page_rect.width

    cap_width = cx1 - cx0
    is_full_width = cap_width > 0.75 * page_w
    if is_full_width:
        col_x0 = page_rect.x0 + 0.04 * page_w
        col_x1 = page_rect.x1 - 0.04 * page_w
    else:
        col_x0, col_x1 = cx0 - 6, cx1 + 6

    if kind == "fig":
        return _infer_above_caption(page, caption, col_x0, col_x1, max_height_ratio)
    return _infer_below_caption(page, caption, col_x0, col_x1, max_height_ratio)


def _infer_above_caption(page, caption, col_x0, col_x1, max_height_ratio):
    _, cy0, _, cy1 = caption["bbox"]
    page_rect = page.rect
    page_h = page_rect.height

    fig_top_candidates = []
    fig_left, fig_right = col_x0, col_x1

    image_bboxes = _image_bboxes_above(page, caption["bbox"], col_x0, col_x1)
    if image_bboxes:
        fig_top_candidates.append(min(bbox[1] for bbox in image_bboxes))
        fig_left = min(fig_left, min(bbox[0] for bbox in image_bboxes) - 4)
        fig_right = max(fig_right, max(bbox[2] for bbox in image_bboxes) + 4)
    else:
        vector_bbox = _vector_bbox_above(page, caption["bbox"], col_x0, col_x1)
        if vector_bbox:
            fig_top_candidates.append(vector_bbox[1])
            fig_left = min(fig_left, vector_bbox[0] - 4)
            fig_right = max(fig_right, vector_bbox[2] + 4)

    fig_img_top = min(fig_top_candidates) if fig_top_candidates else cy0
    nearest_paragraph_bottom = page_rect.y0 + 0.04 * page_h
    for block in page.get_text("blocks"):
        if len(block) < 5:
            continue
        bx0, by0, bx1, by1, text = block[0], block[1], block[2], block[3], block[4]
        if not isinstance(text, str) or not text.strip():
            continue
        if (bx0, by0, bx1, by1) == caption["bbox"]:
            continue
        if by1 >= fig_img_top - 2:
            continue
        if bx1 < col_x0 or bx0 > col_x1:
            continue
        if by1 > nearest_paragraph_bottom:
            nearest_paragraph_bottom = by1
    fig_top_candidates.append(nearest_paragraph_bottom)

    fig_top = min(fig_top_candidates)
    fig_bottom = cy1 + 2
    if fig_bottom - fig_top > max_height_ratio * page_h:
        fig_top = fig_bottom - max_height_ratio * page_h
    fig_top = max(page_rect.y0 + 0.02 * page_h, fig_top - 4)
    return (fig_left, fig_top, fig_right, fig_bottom)


def _infer_below_caption(page, caption, col_x0, col_x1, max_height_ratio):
    """Infer a table body below its caption."""
    _, cy0, _, cy1 = caption["bbox"]
    page_rect = page.rect
    page_h = page_rect.height

    bottom_candidates = []
    table_left, table_right = col_x0, col_x1

    try:
        for drawing in page.get_drawings():
            rect = drawing.get("rect")
            if rect is None:
                continue
            if rect.y0 < cy1 - 2:
                continue
            if rect.x1 < col_x0 or rect.x0 > col_x1:
                continue
            bottom_candidates.append(rect.y1)
            table_left = min(table_left, rect.x0 - 4)
            table_right = max(table_right, rect.x1 + 4)
    except Exception:
        pass

    col_width = col_x1 - col_x0
    next_paragraph_top = page_rect.y1 - 0.04 * page_h
    text_block_bottoms = []
    for block in page.get_text("blocks"):
        if len(block) < 5:
            continue
        bx0, by0, bx1, by1, text = block[0], block[1], block[2], block[3], block[4]
        if not isinstance(text, str) or not text.strip():
            continue
        if (bx0, by0, bx1, by1) == caption["bbox"]:
            continue
        if by0 < cy1 + 2:
            continue
        if bx1 < col_x0 or bx0 > col_x1:
            continue
        line_count = text.count("\n") + 1
        if line_count >= 2 and (bx1 - bx0) > 0.6 * col_width:
            if by0 < next_paragraph_top:
                next_paragraph_top = by0
        else:
            text_block_bottoms.append(by1)

    bottom_candidates.append(next_paragraph_top)
    bottom_candidates.extend(
        block_bottom
        for block_bottom in text_block_bottoms
        if block_bottom < next_paragraph_top
    )

    table_bottom = (
        max(bottom_candidates) if bottom_candidates else cy1 + 0.2 * page_h
    )
    table_top = cy0 - 2

    if table_bottom - table_top > max_height_ratio * page_h:
        table_bottom = table_top + max_height_ratio * page_h
    table_bottom = min(page_rect.y1 - 0.02 * page_h, table_bottom + 4)
    return (table_left, table_top, table_right, table_bottom)


def render_and_crop(page, rect_pdf, zoom, out_path):
    """Render the page at zoom and crop rect_pdf, which uses PDF coordinates."""
    matrix = fitz.Matrix(zoom, zoom)
    pixmap = page.get_pixmap(matrix=matrix, alpha=False)
    image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    x0, y0, x1, y1 = [int(round(value * zoom)) for value in rect_pdf]
    x0 = max(0, x0)
    y0 = max(0, y0)
    x1 = min(pixmap.width, x1)
    y1 = min(pixmap.height, y1)
    if x1 <= x0 or y1 <= y0:
        return None
    crop = image.crop((x0, y0, x1, y1))
    crop.save(out_path, optimize=True)
    return crop.size


def render_full_page(page, zoom, out_path):
    matrix = fitz.Matrix(zoom, zoom)
    pixmap = page.get_pixmap(matrix=matrix, alpha=False)
    pixmap.save(out_path)
    return (pixmap.width, pixmap.height)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("out_dir")
    parser.add_argument(
        "--zoom",
        type=float,
        default=2.0,
        help="render zoom (2.0 is approximately 144 DPI). Default: 2.0",
    )
    parser.add_argument(
        "--pages",
        type=str,
        default=None,
        help="comma-separated 1-indexed pages to also render in full",
    )
    output_filter = parser.add_mutually_exclusive_group()
    output_filter.add_argument("--figures-only", action="store_true")
    output_filter.add_argument("--tables-only", action="store_true")
    parser.add_argument("--max-fig-height-ratio", type=float, default=0.85)
    args = parser.parse_args()

    pdf_path = args.pdf
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    document = fitz.open(pdf_path)
    results = {
        "pdf": pdf_path,
        "out_dir": str(out_dir),
        "figures": [],
        "tables": [],
        "full_pages": [],
    }

    seen = {"fig": set(), "table": set()}

    for page_num in range(1, document.page_count + 1):
        page = document[page_num - 1]
        captions = find_captions(page)
        for caption in captions:
            if args.figures_only and caption["kind"] != "fig":
                continue
            if args.tables_only and caption["kind"] != "table":
                continue
            key = (caption["kind"], caption["number"])
            if key in seen[caption["kind"]]:
                filename = (
                    f"{caption['kind']}{caption['number']}-p{page_num}.png"
                )
            else:
                filename = f"{caption['kind']}{caption['number']}.png"
                seen[caption["kind"]].add(key)
            rect = infer_figure_rect(
                page,
                caption,
                max_height_ratio=args.max_fig_height_ratio,
                kind=caption["kind"],
            )
            out_path = out_dir / filename
            size = render_and_crop(page, rect, args.zoom, str(out_path))
            entry = {
                "file": filename,
                "page": page_num,
                "number": caption["number"],
                "caption": caption["text"],
                "size": size,
            }
            destination = (
                results["figures"]
                if caption["kind"] == "fig"
                else results["tables"]
            )
            destination.append(entry)

    if args.pages:
        for page_string in args.pages.split(","):
            page_string = page_string.strip()
            if not page_string:
                continue
            page_number = int(page_string)
            if page_number < 1 or page_number > document.page_count:
                continue
            out_path = out_dir / f"page_{page_number}_full.png"
            size = render_full_page(
                document[page_number - 1], args.zoom, str(out_path)
            )
            results["full_pages"].append(
                {"file": out_path.name, "page": page_number, "size": size}
            )

    total_pages = document.page_count
    document.close()

    if not results["figures"] and not results["tables"] and not results["full_pages"]:
        for page_number in range(1, min(4, total_pages + 1)):
            fallback_document = None
            try:
                fallback_document = fitz.open(pdf_path)
                fallback_path = out_dir / f"page_{page_number}_full.png"
                size = render_full_page(
                    fallback_document[page_number - 1],
                    args.zoom,
                    str(fallback_path),
                )
                results["full_pages"].append(
                    {
                        "file": fallback_path.name,
                        "page": page_number,
                        "size": size,
                    }
                )
            except Exception:
                pass
            finally:
                if fallback_document is not None:
                    fallback_document.close()

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
