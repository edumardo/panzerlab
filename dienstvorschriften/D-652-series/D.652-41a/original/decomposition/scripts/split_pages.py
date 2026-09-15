"""Split extracted spreads into per-printed-page source.jpg files.

Reads page_map.json (see build_page_map.py) and:
  - "cover" entry: copies spread_001.jpg whole into sections/FM/pages/cover/.
  - "text"/"blank"/"divider" entries: crop the left or right half of the
    matching spread (with a small gutter overlap correction, mirroring the
    LEFT_R/RIGHT_L overlap used by the original recrop.py) into
    sections/<section>/pages/<NNN>/source.jpg.
  - "plate" entries: copy the whole sheet (never split -- plates cross the
    gutter) into sections/G/pages/<sheet:03d>/source.jpg.

Idempotent: re-running overwrites only these derived source.jpg files, never
assets/spreads/*.jpg.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SPREADS = ROOT / "assets" / "spreads"
SECTIONS = ROOT / "sections"
FRONTMATTER = ROOT / "frontmatter"

# Fraction of the spread width each half claims, allowing a small overlap
# across the gutter so text is not clipped (mirrors D.652-41a's original
# recrop.py LEFT_R=0.53 / RIGHT_L=0.47).
LEFT_FRACTION = 0.53
RIGHT_FRACTION = 0.47


def crop_half(spread: Image.Image, side: str) -> Image.Image:
    width, height = spread.size
    if side == "left":
        return spread.crop((0, 0, round(width * LEFT_FRACTION), height))
    return spread.crop((round(width * (1 - RIGHT_FRACTION)), 0, width, height))


def page_dir(section: str, page_key: str) -> Path:
    base = FRONTMATTER if section == "FrontMatter" else SECTIONS / section
    d = base / "pages" / page_key
    d.mkdir(parents=True, exist_ok=True)
    return d


def main() -> None:
    page_map = json.loads((ROOT / "page_map.json").read_text(encoding="utf-8"))
    written = []

    for entry in page_map["pages"]:
        section = entry["section"]
        pdf_page = entry["pdf_page"]
        page_key = f"{entry['page']:03d}"
        spread_path = SPREADS / f"spread_{pdf_page:03d}.jpg"
        out_dir = page_dir(section, page_key)

        if entry["kind"] in ("cover", "plate"):
            shutil.copyfile(spread_path, out_dir / "source.jpg")
            written.append(str(out_dir / "source.jpg"))
            continue

        # text / blank / divider: crop half
        with Image.open(spread_path) as spread:
            half = crop_half(spread, entry["side"])
            half.save(out_dir / "source.jpg", "JPEG", quality=95, optimize=True)
        written.append(str(out_dir / "source.jpg"))

    print(f"Wrote {len(written)} page images")


if __name__ == "__main__":
    main()
