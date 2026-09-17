#!/usr/bin/env python3
"""Inspect an EPUB before translation using only the Python standard library."""

from __future__ import annotations

import argparse
import collections
import html
import re
import zipfile
from pathlib import PurePosixPath
from xml.etree import ElementTree as ET


CONTAINER = "META-INF/container.xml"


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def norm(base: str, href: str) -> str:
    return str(PurePosixPath(base).parent.joinpath(href))


def text_content(data: bytes) -> str:
    text = data.decode("utf-8", errors="replace")
    text = re.sub(r"<script\b.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub")
    args = parser.parse_args()

    with zipfile.ZipFile(args.epub) as book:
        names = set(book.namelist())
        if CONTAINER not in names:
            raise SystemExit("ERROR: META-INF/container.xml is missing")

        container = ET.fromstring(book.read(CONTAINER))
        rootfile = next(
            (
                node.attrib["full-path"]
                for node in container.iter()
                if local(node.tag) == "rootfile" and "full-path" in node.attrib
            ),
            None,
        )
        if not rootfile or rootfile not in names:
            raise SystemExit("ERROR: package document is missing")

        package = ET.fromstring(book.read(rootfile))
        metadata: dict[str, list[str]] = collections.defaultdict(list)
        manifest: dict[str, dict[str, str]] = {}
        spine_ids: list[str] = []

        for node in package.iter():
            tag = local(node.tag)
            if tag in {"title", "creator", "language", "publisher", "identifier"}:
                value = "".join(node.itertext()).strip()
                if value:
                    metadata[tag].append(value)
            elif tag == "item":
                item_id = node.attrib.get("id")
                if item_id:
                    manifest[item_id] = dict(node.attrib)
            elif tag == "itemref" and node.attrib.get("idref"):
                spine_ids.append(node.attrib["idref"])

        media_counts = collections.Counter(
            item.get("media-type", "unknown") for item in manifest.values()
        )
        spine_paths = [
            norm(rootfile, manifest[item_id]["href"])
            for item_id in spine_ids
            if item_id in manifest and "href" in manifest[item_id]
        ]

        tags: collections.Counter[str] = collections.Counter()
        ids = images = links = pagebreaks = words = chars = 0
        chapter_rows: list[tuple[str, int, int]] = []
        for path in spine_paths:
            if path not in names:
                chapter_rows.append((path, 0, 0))
                continue
            data = book.read(path)
            plain = text_content(data)
            chapter_rows.append((path, len(plain), len(plain.split())))
            chars += len(plain)
            words += len(plain.split())
            try:
                root = ET.fromstring(data)
            except ET.ParseError:
                continue
            for node in root.iter():
                tag = local(node.tag)
                tags[tag] += 1
                ids += int("id" in node.attrib)
                images += int(tag in {"img", "image"})
                links += int(tag == "a" and "href" in node.attrib)
                pagebreaks += int(
                    node.attrib.get("{http://www.idpf.org/2007/ops}type") == "pagebreak"
                    or node.attrib.get("role") == "doc-pagebreak"
                )

        print(f"# EPUB inspection: {args.epub}")
        print(f"- package: {rootfile}")
        for key in ("title", "creator", "publisher", "language", "identifier"):
            if metadata.get(key):
                print(f"- {key}: {'; '.join(metadata[key])}")
        print(f"- archive entries: {len(names)}")
        print(f"- manifest items: {len(manifest)}")
        print(f"- spine documents: {len(spine_paths)}")
        print(f"- text: {words:,} words; {chars:,} characters")
        print(f"- IDs: {ids}; links: {links}; images in spine: {images}")
        print(f"- pagebreak markers: {pagebreaks}")
        print("- media types:")
        for media_type, count in media_counts.most_common():
            print(f"  - {media_type}: {count}")
        print("- structural tags:")
        for tag, count in tags.most_common(20):
            print(f"  - {tag}: {count}")
        print("- spine:")
        for path, char_count, word_count in chapter_rows:
            status = "MISSING" if path not in names else f"{word_count:,} words"
            print(f"  - {path}: {status}; {char_count:,} chars")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
