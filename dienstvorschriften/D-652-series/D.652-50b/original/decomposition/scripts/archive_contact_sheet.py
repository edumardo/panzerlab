"""Create a labelled contact sheet for a range of archived book pages."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ORIGINAL = Path(__file__).resolve().parents[1]


def locate(page: int) -> Path:
    manifest = ORIGINAL / "manifest.json"
    import json
    data = json.loads(manifest.read_text(encoding="utf-8"))
    section = next(item["section"] for item in data["pages"] if item["page"] == page)
    base = ORIGINAL / ("frontmatter" if section == "FrontMatter" else f"sections/{section}")
    return base / "pages" / f"{page:03d}" / "source.jpg"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("start", type=int)
    parser.add_argument("end", type=int)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    cell_w, cell_h, columns = 360, 520, 5
    pages = list(range(args.start, args.end + 1))
    rows = (len(pages) + columns - 1) // columns
    canvas = Image.new("RGB", (cell_w * columns, cell_h * rows), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for index, page in enumerate(pages):
        with Image.open(locate(page)) as image:
            thumb = image.convert("RGB")
            thumb.thumbnail((330, 465), Image.Resampling.LANCZOS)
        x = (index % columns) * cell_w + (cell_w - thumb.width) // 2
        y = (index // columns) * cell_h + 35
        canvas.paste(thumb, (x, y))
        draw.text(((index % columns) * cell_w + 15, (index // columns) * cell_h + 12), f"Page {page}", fill="black", font=font)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.output, "JPEG", quality=90, optimize=True)


if __name__ == "__main__":
    main()
