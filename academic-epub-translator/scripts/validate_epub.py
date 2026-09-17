#!/usr/bin/env python3
"""Validate EPUB structure and compare translation invariants with a source EPUB."""

from __future__ import annotations

import argparse
import collections
import posixpath
import urllib.parse
import zipfile
from pathlib import PurePosixPath
from xml.etree import ElementTree as ET


CONTAINER = "META-INF/container.xml"
XML_MEDIA = {
    "application/xhtml+xml",
    "application/x-dtbncx+xml",
    "application/oebps-package+xml",
    "application/xml",
    "image/svg+xml",
}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def resolve(base: str, href: str) -> str:
    href = urllib.parse.unquote(href.split("#", 1)[0])
    return posixpath.normpath(str(PurePosixPath(base).parent / href))


def inspect(path: str) -> tuple[list[str], dict[str, object], list[str]]:
    errors: list[str] = []
    with zipfile.ZipFile(path) as book:
        infos = book.infolist()
        names = {info.filename for info in infos}
        if not infos or infos[0].filename != "mimetype":
            errors.append("mimetype is not the first archive entry")
        elif infos[0].compress_type != zipfile.ZIP_STORED:
            errors.append("mimetype is compressed")
        if "mimetype" not in names:
            errors.append("mimetype is missing")
        elif book.read("mimetype").strip() != b"application/epub+zip":
            errors.append("mimetype content is invalid")
        if CONTAINER not in names:
            errors.append(f"{CONTAINER} is missing")
            return errors, {}, sorted(names)

        try:
            container = ET.fromstring(book.read(CONTAINER))
        except ET.ParseError as exc:
            errors.append(f"{CONTAINER} XML error: {exc}")
            return errors, {}, sorted(names)

        rootfile = next(
            (
                n.attrib.get("full-path")
                for n in container.iter()
                if local(n.tag) == "rootfile"
            ),
            None,
        )
        if not rootfile or rootfile not in names:
            errors.append("package document referenced by container is missing")
            return errors, {}, sorted(names)

        try:
            package = ET.fromstring(book.read(rootfile))
        except ET.ParseError as exc:
            errors.append(f"{rootfile} XML error: {exc}")
            return errors, {}, sorted(names)

        manifest: dict[str, dict[str, str]] = {}
        spine: list[str] = []
        for node in package.iter():
            if local(node.tag) == "item" and node.attrib.get("id"):
                manifest[node.attrib["id"]] = dict(node.attrib)
            elif local(node.tag) == "itemref" and node.attrib.get("idref"):
                spine.append(node.attrib["idref"])

        package_dir = str(PurePosixPath(rootfile).parent)
        xhtml_paths: list[str] = []
        for item_id, item in manifest.items():
            href = item.get("href")
            if not href:
                errors.append(f"manifest item {item_id} has no href")
                continue
            item_path = posixpath.normpath(posixpath.join(package_dir, href))
            if item_path not in names:
                errors.append(f"manifest target missing: {item_path}")
            if item.get("media-type") == "application/xhtml+xml":
                xhtml_paths.append(item_path)

        for item_id in spine:
            if item_id not in manifest:
                errors.append(f"spine idref is absent from manifest: {item_id}")

        all_ids: dict[str, set[str]] = {}
        image_refs: set[tuple[str, str]] = set()
        pagebreaks: set[tuple[str, str]] = set()
        structural = collections.Counter()
        parsed: dict[str, ET.Element] = {}

        for item in manifest.values():
            href = item.get("href")
            if not href:
                continue
            item_path = posixpath.normpath(posixpath.join(package_dir, href))
            media_type = item.get("media-type", "")
            if item_path not in names or media_type not in XML_MEDIA:
                continue
            try:
                parsed[item_path] = ET.fromstring(book.read(item_path))
            except ET.ParseError as exc:
                errors.append(f"{item_path} XML error: {exc}")

        for doc_path in xhtml_paths:
            root = parsed.get(doc_path)
            if root is None:
                continue
            ids: set[str] = set()
            for node in root.iter():
                tag = local(node.tag)
                structural[tag] += 1
                node_id = node.attrib.get("id")
                if node_id:
                    if node_id in ids:
                        errors.append(f"duplicate id in {doc_path}: {node_id}")
                    ids.add(node_id)
                epub_type = node.attrib.get("{http://www.idpf.org/2007/ops}type", "")
                if "pagebreak" in epub_type.split() or node.attrib.get("role") == "doc-pagebreak":
                    pagebreaks.add((doc_path, node_id or ""))
                if tag in {"img", "image"}:
                    src = node.attrib.get("src") or node.attrib.get(
                        "{http://www.w3.org/1999/xlink}href"
                    )
                    if src:
                        target = resolve(doc_path, src)
                        image_refs.add((doc_path, src))
                        if target not in names:
                            errors.append(f"image target missing from {doc_path}: {src}")
                href = node.attrib.get("href")
                if tag == "a" and href and not href.startswith(
                    ("http:", "https:", "mailto:", "tel:", "data:")
                ):
                    target = resolve(doc_path, href) if href.split("#", 1)[0] else doc_path
                    if target not in names:
                        errors.append(f"link target missing from {doc_path}: {href}")
            all_ids[doc_path] = ids

        for doc_path in xhtml_paths:
            root = parsed.get(doc_path)
            if root is None:
                continue
            for node in root.iter():
                href = node.attrib.get("href", "")
                if local(node.tag) != "a" or "#" not in href or href.startswith(
                    ("http:", "https:", "mailto:")
                ):
                    continue
                raw_path, fragment = href.split("#", 1)
                target = resolve(doc_path, raw_path) if raw_path else doc_path
                if fragment and target in all_ids and fragment not in all_ids[target]:
                    errors.append(f"link fragment missing from {doc_path}: {href}")

        data: dict[str, object] = {
            "spine": tuple(spine),
            "xhtml": tuple(sorted(xhtml_paths)),
            "ids": {key: frozenset(value) for key, value in all_ids.items()},
            "images": frozenset(image_refs),
            "pagebreaks": frozenset(pagebreaks),
            "structural": structural,
            "assets": frozenset(
                name
                for name in names
                if not name.lower().endswith((".xhtml", ".html", ".htm", ".opf", ".ncx"))
            ),
        }
        return errors, data, sorted(names)


def compare(source: dict[str, object], target: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for key in ("spine", "xhtml", "ids", "images", "pagebreaks", "assets"):
        if source.get(key) != target.get(key):
            errors.append(f"source/target invariant differs: {key}")
    source_tags = source.get("structural", {})
    target_tags = target.get("structural", {})
    for tag in ("figure", "table", "img", "image", "aside"):
        if source_tags.get(tag, 0) != target_tags.get(tag, 0):
            errors.append(
                f"source/target {tag} count differs: "
                f"{source_tags.get(tag, 0)} != {target_tags.get(tag, 0)}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub")
    parser.add_argument("--source")
    args = parser.parse_args()

    errors, target, names = inspect(args.epub)
    if args.source and target:
        source_errors, source, _ = inspect(args.source)
        if source_errors:
            errors.append("source EPUB is not valid enough for comparison")
            errors.extend(f"source: {error}" for error in source_errors)
        else:
            errors.extend(compare(source, target))

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {args.epub} ({len(names)} archive entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
