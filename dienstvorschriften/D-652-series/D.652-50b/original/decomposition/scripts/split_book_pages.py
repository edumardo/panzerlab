"""Split each photographed two-page spread into individual book-page images.

Each spread photo shows the open book on a neutral marble background that
surrounds it on all four sides. The camera rig was fixed for the whole shoot,
so the book occupies the same region of the frame in every spread; the crop
box below was calibrated by visual inspection of spreads 3, 4, 30, 57 and 58
(see decomposition/README.md) and reused for all of them. One spread
(spread_002, holding book page 1) was captured at ~4.17x higher resolution
than the rest, so the box is scaled by the image's actual width before use
rather than assumed constant in pixels.

Writes only inside frontmatter/pages/<NNN>/ or sections/<ID>/pages/<NNN>/;
never touches the original PDF or the extracted spreads.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parents[1]

# Calibrated against a spread of reference width REFERENCE_WIDTH px.
REFERENCE_WIDTH = 3456
BOOK_BOX = (330, 160, 3170, 2115)  # left, top, right, bottom
GUTTER_X = 1750


def crop_box_for(image_width: int, side: str) -> tuple[int, int, int, int]:
    scale = image_width / REFERENCE_WIDTH
    left, top, right, bottom = (round(v * scale) for v in BOOK_BOX)
    gutter = round(GUTTER_X * scale)
    if side == "left":
        return left, top, gutter, bottom
    return gutter, top, right, bottom


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Report crop boxes without writing files")
    parser.add_argument("--only-page", type=int, help="Process a single book page number (debug)")
    args = parser.parse_args()

    manifest_path = ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pages = manifest["pages"]
    if args.only_page:
        pages = [p for p in pages if p["page"] == args.only_page]

    by_spread: dict[int, list[dict]] = {}
    for entry in pages:
        by_spread.setdefault(entry["pdf_spread"], []).append(entry)

    updated_pages = 0
    for spread_number in sorted(by_spread):
        spread_path = ROOT / "assets" / "spreads" / f"spread_{spread_number:03d}.jpg"
        image = Image.open(spread_path).convert("RGB")

        for entry in by_spread[spread_number]:
            side = entry["side"]
            box = crop_box_for(image.width, side)
            cropped = image.crop(box)
            page = entry["page"]
            section = entry["section"]
            page_dir = (ROOT / "frontmatter" if section == "FrontMatter" else ROOT / "sections" / section) / "pages" / f"{page:03d}"

            print(f"page {page:03d} (spread {spread_number:03d} {side}): box={box} size={cropped.size} -> {page_dir}")

            if args.dry_run:
                continue

            page_dir.mkdir(parents=True, exist_ok=True)
            (page_dir / "figures").mkdir(exist_ok=True)
            cropped.save(page_dir / "source.jpg", quality=95, optimize=True)
            entry["source_scan_status"] = "extracted_clean"
            updated_pages += 1

    if not args.dry_run and updated_pages:
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Updated source_scan_status for {updated_pages} pages in manifest.json")


if __name__ == "__main__":
    main()
