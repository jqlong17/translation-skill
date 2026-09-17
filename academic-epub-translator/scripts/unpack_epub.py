#!/usr/bin/env python3
"""Safely unpack an EPUB into a new translation work directory."""

from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub")
    parser.add_argument("output")
    args = parser.parse_args()

    source = Path(args.epub).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if output.exists():
        raise SystemExit(f"ERROR: output already exists: {output}")

    output.mkdir(parents=True)
    try:
        with zipfile.ZipFile(source) as book:
            for info in book.infolist():
                destination = (output / info.filename).resolve()
                if output not in destination.parents and destination != output:
                    raise ValueError(f"unsafe archive path: {info.filename}")
            book.extractall(output)
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise

    print(f"Unpacked {source} to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
