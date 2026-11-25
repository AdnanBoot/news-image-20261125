#!/usr/bin/env python3
"""Entrypoint for the news-image-20261125 make.fun entry.

Copies the pre-rendered entry.png from the repository root to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output) after verifying its SHA-256.
Stdlib-only; no network access.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

EXPECTED_SHA256 = "a38cff2a5639c8160460d52cf817157cefef836a13718516c7df514395b850f8"


def sha256_file(path: Path) -> str:
    """Compute hex SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    src = repo_root / "entry.png"
    if not src.is_file():
        print(f"error: pre-rendered image not found at {src}", file=sys.stderr)
        return 1

    actual_sha256 = sha256_file(src)
    if actual_sha256 != EXPECTED_SHA256:
        print(
            f"error: SHA-256 mismatch for {src}: expected {EXPECTED_SHA256}, got {actual_sha256}",
            file=sys.stderr,
        )
        return 1

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    dst = output_dir / "entry.png"
    shutil.copy2(src, dst)
    print(f"wrote {dst} (sha256={actual_sha256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
