"""Split each extracted spread into its left/right printed book pages.

Reads decomposition/manifest.json for the page map, crops each spread at a
smoothed spine position (found per-spread by locating the darkest vertical
band near mid-width, then median-smoothed across neighbours to avoid single
outlier crops), and writes source.jpg into each page's canonical directory
(frontmatter/pages/NNN/ or sections/<id>/pages/NNN/). Never overwrites an
existing source.jpg (idempotent: re-run after deleting a page dir to redo).
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parents[1]
SPREADS = ROOT / "assets" / "spreads"


def spine_fraction(path: Path, lo_f: float = 0.46, hi_f: float = 0.54) -> float:
    im = Image.open(path).convert("L")
    w, _ = im.size
    arr = np.asarray(im)
    lo, hi = int(w * lo_f), int(w * hi_f)
    band = arr[:, lo:hi]
    col_mean = band.mean(axis=0)
    return (lo + int(col_mean.argmin())) / w


def page_dir(section: str, page: int) -> Path:
    base = ROOT / "frontmatter" if section == "FrontMatter" else ROOT / "sections" / section
    return base / "pages" / f"{page:03d}"


def main() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    pages = manifest["pages"]

    pdf_pages = sorted({p["pdf_page"] for p in pages})
    fractions = {}
    for n in pdf_pages:
        spread = SPREADS / f"spread_{n:03d}.jpg"
        if spread.exists():
            fractions[n] = spine_fraction(spread)

    smoothed = {}
    for n in pdf_pages:
        window = [fractions[m] for m in pdf_pages if abs(m - n) <= 2 and m in fractions]
        smoothed[n] = statistics.median(window)

    written, skipped = 0, 0
    for entry in pages:
        n = entry["pdf_page"]
        side = entry["side"]
        spread_path = SPREADS / f"spread_{n:03d}.jpg"
        im = Image.open(spread_path)
        w, h = im.size

        if side == "single":
            crop = im
            box = (0, 0, w, h)
        else:
            spine_x = round(smoothed[n] * w)
            if side == "left":
                box = (0, 0, spine_x, h)
            else:
                box = (spine_x, 0, w, h)
            crop = im.crop(box)

        out_dir = page_dir(entry["section"], entry["page"])
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "source.jpg"
        if out_path.exists():
            skipped += 1
            continue
        crop.save(out_path, "JPEG", quality=92, optimize=True)
        written += 1

    print(f"wrote {written} page images, skipped {skipped} existing")


if __name__ == "__main__":
    main()
