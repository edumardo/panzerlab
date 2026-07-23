"""Extract the clean base scan from each PDF page.

Selects the largest raster image XObject per page directly via pypdf, without
rendering the PDF page, so any compositing artefacts from a PDF viewer are
avoided. Writes assets/spreads/spread_NNN.jpg (full photographed spread, two
facing printed pages per PDF page) and assets/thumbs/spread_NNN_thumb.jpg.
"""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
from typing import Iterator

from PIL import Image
from pypdf import PdfReader
import pypdf.filters


Image.MAX_IMAGE_PIXELS = None
pypdf.filters.ZLIB_MAX_OUTPUT_LENGTH = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--start", type=int, default=1, help="First PDF page (1-based)")
    parser.add_argument("--end", type=int, help="Last PDF page (1-based, inclusive)")
    parser.add_argument("--thumb-width", type=int, default=1550)
    return parser.parse_args()


def iter_image_xobjects(resources, prefix: str = "") -> Iterator[tuple[str, object]]:
    if not resources or "/XObject" not in resources:
        return
    for name, ref in resources["/XObject"].get_object().items():
        obj = ref.get_object()
        subtype = obj.get("/Subtype")
        path = f"{prefix}{name}"
        if subtype == "/Image":
            yield path, obj
        elif subtype == "/Form":
            yield from iter_image_xobjects(obj.get("/Resources"), prefix=f"{path}/")


def decode_xobject(obj) -> tuple[Image.Image, bytes | None]:
    filters = obj.get("/Filter", [])
    if not isinstance(filters, list):
        filters = [filters]

    jpeg_data = None
    if "/DCTDecode" in filters:
        jpeg_data = obj._data if filters == ["/DCTDecode"] else obj.get_data()
        with Image.open(io.BytesIO(jpeg_data)) as im:
            im.load()
            return im.copy(), jpeg_data

    data = obj.get_data()
    width = int(obj["/Width"])
    height = int(obj["/Height"])
    colour_space = obj.get("/ColorSpace")
    mode = "L" if colour_space == "/DeviceGray" else "RGB"
    return Image.frombytes(mode, (width, height), data), None


def extract_page(page, page_number: int, output_dir: Path, thumb_width: int) -> dict:
    candidates = []
    for index, (name, obj) in enumerate(iter_image_xobjects(page["/Resources"])):
        try:
            im, jpeg_data = decode_xobject(obj)
            candidates.append(
                {
                    "index": index,
                    "name": name,
                    "width": im.width,
                    "height": im.height,
                    "mode": im.mode,
                    "area": im.width * im.height,
                    "image": im,
                    "jpeg_data": jpeg_data,
                }
            )
        except Exception as exc:
            candidates.append({"index": index, "name": name, "error": f"{type(exc).__name__}: {exc}", "area": -1})

    usable = [c for c in candidates if c["area"] > 0]
    if not usable:
        raise RuntimeError(f"No decodable raster image found on PDF page {page_number}")

    selected = max(usable, key=lambda c: c["area"])
    base = selected.pop("image")
    jpeg_data = selected.pop("jpeg_data")
    if base.mode not in ("RGB", "L"):
        base = base.convert("RGB")

    spread_path = output_dir / "spreads" / f"spread_{page_number:03d}.jpg"
    thumb_path = output_dir / "thumbs" / f"spread_{page_number:03d}_thumb.jpg"
    spread_path.parent.mkdir(parents=True, exist_ok=True)
    thumb_path.parent.mkdir(parents=True, exist_ok=True)

    if jpeg_data:
        spread_path.write_bytes(jpeg_data)
    else:
        base.save(spread_path, "JPEG", quality=95, optimize=True)
    thumb = base.copy()
    if thumb.width > thumb_width:
        height = round(thumb.height * thumb_width / thumb.width)
        thumb.thumbnail((thumb_width, height), Image.Resampling.LANCZOS)
    thumb.save(thumb_path, "JPEG", quality=88, optimize=True)

    print(f"{page_number:03d}: {selected['width']}x{selected['height']}")
    return {"pdf_page": page_number, "selected": selected,
            "spread": spread_path.relative_to(output_dir).as_posix(),
            "thumbnail": thumb_path.relative_to(output_dir).as_posix()}


def main() -> None:
    args = parse_args()
    reader = PdfReader(args.pdf)
    end = args.end or len(reader.pages)
    if args.start < 1 or end > len(reader.pages) or args.start > end:
        raise SystemExit(f"Invalid page range {args.start}-{end}; PDF has {len(reader.pages)} pages")

    records = []
    for page_number in range(args.start, end + 1):
        record = extract_page(reader.pages[page_number - 1], page_number, args.output_dir, args.thumb_width)
        records.append(record)

    manifest_path = args.output_dir / f"extraction_{args.start:03d}_{end:03d}.json"
    manifest_path.write_text(json.dumps(records, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
