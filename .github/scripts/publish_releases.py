"""Create a GitHub Release for each document whose compiled export gained a
new version in this push to master.

Detects two kinds of "publish" signals by diffing the files changed between
BEFORE_SHA and AFTER_SHA:

- A bilingual compiled export: dienstvorschriften/<series>/<doc>/bilingual/<doc>_bilingual_full_v<version>.pdf
- A single-language export: dienstvorschriften/<series>/<doc>/(en|es)/<doc>_(en|es)_v<version>.pdf

For each (series, doc, version) group found, the tag "<doc>-v<version>" is
computed. If a release with that tag does not already exist, one is created,
attaching the document's original German PDF plus whatever bilingual/en/es
PDF files currently exist at the top level of those directories.

Idempotent: re-running for a version that was already released is a no-op,
so a workflow re-run or a push that doesn't bump any document's version
does nothing.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

BILINGUAL_RE = re.compile(
    r"^dienstvorschriften/(?P<series>[^/]+)/(?P<doc>[^/]+)/bilingual/"
    r"(?P=doc)_bilingual_full_v(?P<version>[\d.]+)\.pdf$"
)
LANG_RE = re.compile(
    r"^dienstvorschriften/(?P<series>[^/]+)/(?P<doc>[^/]+)/(?P<lang>en|es)/"
    r"(?P=doc)_(?P=lang)_v(?P<version>[\d.]+)\.pdf$"
)


def changed_files(before_sha: str, after_sha: str) -> list[str]:
    if not before_sha or set(before_sha) == {"0"}:
        # First push seen on this ref (or unknown before-state): diff against
        # the empty tree so we still catch every file in the new commit.
        before_sha = subprocess.run(
            ["git", "hash-object", "-t", "tree", "/dev/null"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    result = subprocess.run(
        ["git", "diff", "--name-only", before_sha, after_sha],
        capture_output=True, text=True, check=True, cwd=REPO_ROOT,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def find_publishable_versions(paths: list[str]) -> dict[tuple[str, str, str], dict]:
    groups: dict[tuple[str, str, str], dict] = {}
    for path in paths:
        m = BILINGUAL_RE.match(path)
        if m:
            key = (m["series"], m["doc"], m["version"])
            groups.setdefault(key, {"bilingual_full": None, "en": None, "es": None})
            groups[key]["bilingual_full"] = path
            continue
        m = LANG_RE.match(path)
        if m:
            key = (m["series"], m["doc"], m["version"])
            groups.setdefault(key, {"bilingual_full": None, "en": None, "es": None})
            groups[key][m["lang"]] = path
    return groups


def tag_exists(tag: str) -> bool:
    result = subprocess.run(
        ["gh", "release", "view", tag],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    return result.returncode == 0


def parse_metadata(doc_path: Path) -> dict:
    text = (doc_path / "metadata.md").read_text(encoding="utf-8")
    fields = {}
    for key in ("Designation", "Title (DE)", "Title (EN)"):
        m = re.search(rf"\*\*{re.escape(key)}\*\*:\s*(.+)", text)
        if m:
            fields[key] = m.group(1).strip()
    return fields


def gather_assets(doc_path: Path, group: dict) -> list[Path]:
    assets: list[Path] = []
    original_dir = doc_path / "original"
    if original_dir.is_dir():
        assets.extend(sorted(p for p in original_dir.glob("*.pdf")))
    for sub in ("bilingual", "en", "es"):
        sub_dir = doc_path / sub
        if sub_dir.is_dir():
            assets.extend(sorted(p for p in sub_dir.glob("*.pdf")))
    return assets


def build_notes(fields: dict, version: str, group: dict, doc_path: Path) -> str:
    title_en = fields.get("Title (EN)", "")
    lines = [f"**{title_en}** (v{version})", ""]
    originals = sorted((doc_path / "original").glob("*.pdf")) if (doc_path / "original").is_dir() else []
    if originals:
        lines.append(f"- Original (German scan): `{originals[0].name}`")
    if group.get("bilingual_full"):
        lines.append(
            f"- Bilingual EN/ES facsimile + translation: `{Path(group['bilingual_full']).name}`"
        )
    else:
        if group.get("es"):
            lines.append(f"- Spanish translation: `{Path(group['es']).name}`")
        if group.get("en"):
            lines.append(f"- English translation: `{Path(group['en']).name}`")
    return "\n".join(lines)


def main() -> int:
    before_sha = os.environ["BEFORE_SHA"]
    after_sha = os.environ["AFTER_SHA"]

    paths = changed_files(before_sha, after_sha)
    groups = find_publishable_versions(paths)

    if not groups:
        print("No document version changes detected; nothing to release.")
        return 0

    for (series, doc, version), group in groups.items():
        tag = f"{doc}-v{version}"
        doc_path = REPO_ROOT / "dienstvorschriften" / series / doc
        if not doc_path.is_dir():
            print(f"Skipping {tag}: {doc_path} does not exist at {after_sha}.")
            continue
        if tag_exists(tag):
            print(f"Skipping {tag}: release already exists.")
            continue

        fields = parse_metadata(doc_path)
        designation = fields.get("Designation", doc)
        title_de = fields.get("Title (DE)", doc)
        title = f"{designation} — {title_de}"
        notes = build_notes(fields, version, group, doc_path)
        assets = gather_assets(doc_path, group)

        if not assets:
            print(f"Skipping {tag}: no PDF assets found under {doc_path}.")
            continue

        print(f"Creating release {tag} with {len(assets)} asset(s)...")
        subprocess.run(
            [
                "gh", "release", "create", tag,
                *[str(p) for p in assets],
                "--title", title,
                "--notes", notes,
            ],
            check=True, cwd=REPO_ROOT,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
