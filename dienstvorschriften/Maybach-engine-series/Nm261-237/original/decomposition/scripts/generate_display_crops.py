"""Generate a display copy of each page's source.jpg with scan-background trimmed.

Overwrites, per page directory: `source_display.jpg` (derived, safe to regenerate)
and the `display_scan` / `display_scan_crop_box_px` fields in `manifest.json`, and
the `source.display_image` field in `content.json`. Also mirrors the updated page
manifest into the global `manifest.json`. Never touches `source.jpg` itself.

Heuristic: the aged cream/tan paper is warm (R notably greater than B); the
grey/neutral cover stock and margins are cooler. For each edge, scan a bounded
window inward and find the steepest warmth rise (background -> paper).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

MAX_TRIM_FRAC_W = 0.15
MAX_TRIM_FRAC_H = 0.08
MARGIN_PX = 6
MIN_JUMP = 8.0


def warmth(arr):
    r = arr[..., 0].astype(np.int16)
    b = arr[..., 2].astype(np.int16)
    return r - b


def steepest_rise_from_start(profile, window):
    n = len(profile)
    span = 5
    best_idx, best_jump = 0, 0.0
    for i in range(1, window):
        jump = profile[min(i + span, n - 1)] - profile[max(i - span, 0)]
        if jump > best_jump:
            best_jump = jump
            best_idx = i
    return best_idx, best_jump


def steepest_rise(profile, window, reverse=False):
    n = len(profile)
    if not reverse:
        return steepest_rise_from_start(profile, window)
    idx, jump = steepest_rise_from_start(profile[::-1], window)
    return n - idx, jump


def find_crop_box(arr):
    h, w = arr.shape[:2]
    warm = warmth(arr)
    col_mean = warm.mean(axis=0)
    row_mean = warm.mean(axis=1)

    max_left = int(w * MAX_TRIM_FRAC_W)
    max_right = int(w * MAX_TRIM_FRAC_W)
    max_top = int(h * MAX_TRIM_FRAC_H)
    max_bottom = int(h * MAX_TRIM_FRAC_H)

    left, left_jump = steepest_rise(col_mean, max_left, reverse=False)
    right_idx, right_jump = steepest_rise(col_mean, max_right, reverse=True)
    top, top_jump = steepest_rise(row_mean, max_top, reverse=False)
    bottom_idx, bottom_jump = steepest_rise(row_mean, max_bottom, reverse=True)

    left = left if left_jump >= MIN_JUMP else 0
    right = right_idx if right_jump >= MIN_JUMP else w
    top = top if top_jump >= MIN_JUMP else 0
    bottom = bottom_idx if bottom_jump >= MIN_JUMP else h

    left = max(0, left - MARGIN_PX)
    top = max(0, top - MARGIN_PX)
    right = min(w, right + MARGIN_PX)
    bottom = min(h, bottom + MARGIN_PX)
    return left, top, right, bottom


def process_page(page_dir: Path) -> dict:
    source_path = page_dir / "source.jpg"
    image = Image.open(source_path).convert("RGB")
    arr = np.array(image)
    left, top, right, bottom = find_crop_box(arr)
    cropped = image.crop((left, top, right, bottom))
    display_path = page_dir / "source_display.jpg"
    cropped.save(display_path, quality=92)

    manifest_path = page_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["display_scan"] = "source_display.jpg"
    manifest["display_scan_crop_box_px"] = [left, top, right, bottom]
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    content_path = page_dir / "content.json"
    content = json.loads(content_path.read_text(encoding="utf-8"))
    content["source"]["display_image"] = "source_display.jpg"
    content_path.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"{page_dir}: {image.size} -> {cropped.size} (box={left},{top},{right},{bottom})")
    return manifest


def main():
    global_manifest_path = ROOT / "manifest.json"
    global_manifest = json.loads(global_manifest_path.read_text(encoding="utf-8"))

    updated_by_page = {}
    for entry in global_manifest["pages"]:
        page_number = entry["page"]
        section = entry["section"]
        section_dir = ROOT / ("frontmatter" if section == "FrontMatter" else f"sections/{section}")
        page_dir = section_dir / "pages" / f"{page_number:03d}"
        updated_by_page[page_number] = process_page(page_dir)

    for entry in global_manifest["pages"]:
        page_number = entry["page"]
        entry.clear()
        entry.update(updated_by_page[page_number])
    global_manifest_path.write_text(
        json.dumps(global_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
