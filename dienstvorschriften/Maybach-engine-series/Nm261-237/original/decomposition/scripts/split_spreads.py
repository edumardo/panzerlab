"""Split each photographed spread (assets/spreads/spread_NNN.jpg) into the
individual printed pages it contains, per an explicit crop map for this
document. Overwrites source.jpg under the target page/asset directories;
never touches assets/spreads/ (the untouched archival scans).

Crop fractions were calibrated by visual inspection of each spread (see
processing notes) because spread widths vary (unequal leaf widths for the
cover stock vs. text-block leaves) and a blind 50/50 split clips the wider
leaves.
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SPREADS = ROOT / "assets" / "spreads"

# (spread_number, [(fraction_start, fraction_end, output_relpath), ...])
JOBS = [
    (1, [(0.5, 1.0, "frontmatter/cover.jpg")]),
    (2, [(0.0, 0.44, "frontmatter/inside_cover_blank.jpg"),
         (0.44, 1.0, "frontmatter/pages/001/source.jpg")]),
    (3, [(0.0, 0.5, "frontmatter/pages/002/source.jpg"),
         (0.5, 1.0, "frontmatter/pages/003/source.jpg")]),
    (4, [(0.0, 0.5, "sections/A01/pages/004/source.jpg"),
         (0.5, 1.0, "sections/A01/pages/005/source.jpg")]),
    (5, [(0.0, 0.5, "sections/A02/pages/006/source.jpg"),
         (0.5, 1.0, "sections/A02/pages/007/source.jpg")]),
    (6, [(0.0, 0.5, "sections/A03/pages/008/source.jpg"),
         (0.5, 1.0, "sections/A03/pages/009/source.jpg")]),
    (7, [(0.0, 0.5, "sections/A04/pages/010/source.jpg"),
         (0.5, 1.0, "sections/A04/pages/011/source.jpg")]),
    (8, [(0.0, 0.5, "sections/A05/pages/012/source.jpg"),
         (0.5, 1.0, "sections/A05/pages/013/source.jpg")]),
    (9, [(0.0, 0.5, "sections/A06/pages/014/source.jpg"),
         (0.5, 1.0, "sections/A06/pages/015/source.jpg")]),
    (10, [(0.0, 0.5, "sections/A07/pages/016/source.jpg"),
          (0.5, 1.0, "sections/A07/pages/017/source.jpg")]),
    (11, [(0.0, 0.5, "sections/A08/pages/018/source.jpg"),
          (0.5, 1.0, "sections/A08/pages/019/source.jpg")]),
    (12, [(0.0, 0.5, "sections/A09/pages/020/source.jpg"),
          (0.5, 1.0, "sections/A09/pages/021/source.jpg")]),
    # 13: blank endpaper leaves, not archived as numbered pages.
    (14, [(0.0, 0.33, "frontmatter/provenance_note.jpg")]),
    (15, [(0.0, 1.0, "frontmatter/cover_back.jpg")]),
]


def main():
    for spread_number, crops in JOBS:
        spread_path = SPREADS / f"spread_{spread_number:03d}.jpg"
        img = Image.open(spread_path)
        w, h = img.size
        for frac_start, frac_end, relpath in crops:
            x0 = int(w * frac_start)
            x1 = int(w * frac_end)
            crop = img.crop((x0, 0, x1, h))
            out_path = ROOT / relpath
            out_path.parent.mkdir(parents=True, exist_ok=True)
            crop.save(out_path, "JPEG", quality=95)
            print(f"spread {spread_number:03d} [{frac_start:.2f},{frac_end:.2f}] -> {relpath} ({crop.size})")


if __name__ == "__main__":
    main()
