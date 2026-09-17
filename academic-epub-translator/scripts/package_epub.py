#!/usr/bin/env python3
"""Package an EPUB work directory with a compliant mimetype entry."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workdir")
    parser.add_argument("output")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="replace the output EPUB when it is an intentionally superseded current build",
    )
    args = parser.parse_args()

    workdir = Path(args.workdir).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    mimetype = workdir / "mimetype"
    if not mimetype.is_file():
        raise SystemExit("ERROR: work directory has no mimetype file")
    if mimetype.read_bytes().strip() != b"application/epub+zip":
        raise SystemExit("ERROR: invalid mimetype content")
    if output.exists() and args.replace:
        output.unlink()
    if output.exists():
        raise SystemExit(f"ERROR: output already exists: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    files = sorted(
        path
        for path in workdir.rglob("*")
        if path.is_file()
        and path.name != "TRANSLATION_STATE.md"
        and not any(part.startswith(".") for part in path.relative_to(workdir).parts)
    )
    with zipfile.ZipFile(output, "w") as book:
        book.write(mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in files:
            if path == mimetype:
                continue
            book.write(
                path,
                path.relative_to(workdir).as_posix(),
                compress_type=zipfile.ZIP_DEFLATED,
            )

    print(f"Packaged {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
