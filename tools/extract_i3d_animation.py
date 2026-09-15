#!/usr/bin/env python3
"""Inspect an FS25 I3D animation without modifying donor assets.

This helper is intentionally generic. It can read either a raw .i3d file or an FS25
mod ZIP, list all parts/keyframes for one animation, and resolve GIANTS scene paths to
node names and i3dMapping identifiers where possible.

Primary project use:
    python tools/extract_i3d_animation.py FS25_Bourgault_3320_4Tank_V6_Engineering.zip \
        --i3d-path i3d/Series_7950B.i3d --animation loadingPipe

The tool is read-only. It does not calculate a promoted engineering solution by itself;
it provides the exact donor/candidate hierarchy and keyframes needed for that work.
"""

from __future__ import annotations

import argparse
import io
import pathlib
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


@dataclass
class SceneNode:
    path: str
    tag: str
    name: str
    attrs: dict[str, str]


def normalize_scene_path(value: str | None) -> str | None:
    """Normalize common GIANTS path spellings to the path below <Scene>.

    Examples:
        0>0|2|1 -> 0|2|1
        0|2|1   -> 0|2|1

    Numeric node IDs that are not path-like are returned unchanged so the caller can
    still display them even if they cannot be resolved through the scene hierarchy.
    """
    if value is None:
        return None
    value = value.strip()
    if value.startswith("0>"):
        return value[2:]
    return value


def read_i3d(source: pathlib.Path, i3d_path: str) -> bytes:
    if source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source, "r") as zf:
            names = zf.namelist()
            if i3d_path not in names:
                candidates = [n for n in names if n.lower().endswith(".i3d")]
                raise FileNotFoundError(
                    f"{i3d_path!r} not found in ZIP. I3D candidates: {candidates}"
                )
            return zf.read(i3d_path)
    return source.read_bytes()


def build_scene_index(root: ET.Element) -> dict[str, SceneNode]:
    scene = root.find("Scene")
    if scene is None:
        return {}

    index: dict[str, SceneNode] = {}

    def walk(element: ET.Element, path: str) -> None:
        index[path] = SceneNode(
            path=path,
            tag=element.tag,
            name=element.attrib.get("name", ""),
            attrs=dict(element.attrib),
        )
        for child_index, child in enumerate(list(element)):
            walk(child, f"{path}|{child_index}")

    for top_index, child in enumerate(list(scene)):
        walk(child, str(top_index))

    return index


def build_mapping_index(root: ET.Element) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Return path->mapping IDs and mapping ID->path indexes."""
    by_path: dict[str, list[str]] = defaultdict(list)
    by_id: dict[str, str] = {}

    mappings = root.find("i3dMappings")
    if mappings is None:
        return dict(by_path), by_id

    for mapping in mappings.findall("i3dMapping"):
        mapping_id = mapping.attrib.get("id")
        node = normalize_scene_path(mapping.attrib.get("node"))
        if mapping_id and node:
            by_path[node].append(mapping_id)
            by_id[mapping_id] = node

    return dict(by_path), by_id


def find_animation(root: ET.Element, animation_name: str) -> ET.Element | None:
    animations = root.find("Animations")
    if animations is None:
        return None
    for animation in animations.findall("Animation"):
        if animation.attrib.get("name") == animation_name:
            return animation
    return None


def available_animations(root: ET.Element) -> list[str]:
    animations = root.find("Animations")
    if animations is None:
        return []
    return [
        a.attrib.get("name", "<unnamed>")
        for a in animations.findall("Animation")
    ]


def iter_parts(animation: ET.Element) -> Iterable[ET.Element]:
    # GIANTS I3D files normally store Part directly under Animation. Descendant search
    # keeps the helper tolerant of an intermediate container if one is encountered.
    direct = animation.findall("Part")
    return direct if direct else animation.findall(".//Part")


def format_attrs(attrs: dict[str, str], skip: set[str] | None = None) -> str:
    skip = skip or set()
    return " ".join(f"{key}={value!r}" for key, value in attrs.items() if key not in skip)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List I3D animation parts, keyframes, scene nodes, and mappings"
    )
    parser.add_argument("source", help="raw .i3d file or FS25 mod ZIP")
    parser.add_argument(
        "--i3d-path",
        default="i3d/Series_7950B.i3d",
        help="I3D path inside a ZIP (ignored for a raw .i3d source)",
    )
    parser.add_argument("--animation", default="loadingPipe", help="animation name")
    parser.add_argument(
        "--name-filter",
        default="",
        help="optional case-insensitive substring; only print parts whose resolved node/mapping contains it",
    )
    args = parser.parse_args()

    source = pathlib.Path(args.source)
    try:
        payload = read_i3d(source, args.i3d_path)
        root = ET.parse(io.BytesIO(payload)).getroot()
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2

    scene_index = build_scene_index(root)
    mappings_by_path, mappings_by_id = build_mapping_index(root)
    animation = find_animation(root, args.animation)

    if animation is None:
        print(f"Animation {args.animation!r} not found.", file=sys.stderr)
        print("Available animations:")
        for name in available_animations(root):
            print(f"  - {name}")
        return 1

    print(f"Source: {source}")
    if source.suffix.lower() == ".zip":
        print(f"I3D: {args.i3d_path}")
    print(f"Animation: {args.animation}")
    if animation.attrib:
        print(f"Animation attributes: {format_attrs(dict(animation.attrib))}")
    print()

    printed = 0
    for part_index, part in enumerate(iter_parts(animation), start=1):
        raw_node = part.attrib.get("node", "")
        normalized = normalize_scene_path(raw_node) or raw_node

        # A Part may reference a path directly or, in some files, an i3dMapping ID.
        mapped_path = mappings_by_id.get(raw_node)
        lookup_path = mapped_path or normalized
        scene_node = scene_index.get(lookup_path)
        mapping_ids = mappings_by_path.get(lookup_path, [])

        searchable = " ".join(
            [
                raw_node,
                lookup_path,
                scene_node.name if scene_node else "",
                " ".join(mapping_ids),
            ]
        ).lower()
        if args.name_filter and args.name_filter.lower() not in searchable:
            continue

        printed += 1
        print(f"PART {part_index}")
        print(f"  raw node:       {raw_node}")
        print(f"  resolved path:  {lookup_path}")
        if scene_node is not None:
            print(f"  scene tag/name: {scene_node.tag} / {scene_node.name or '<unnamed>'}")
            static_keys = ("translation", "rotation", "scale", "visibility")
            static_attrs = {
                key: scene_node.attrs[key]
                for key in static_keys
                if key in scene_node.attrs
            }
            if static_attrs:
                print(f"  static:         {format_attrs(static_attrs)}")
        else:
            print("  scene node:     <unresolved>")
        print(f"  mappings:       {', '.join(mapping_ids) if mapping_ids else '<none>'}")

        part_extra = format_attrs(dict(part.attrib), skip={"node"})
        if part_extra:
            print(f"  part attrs:     {part_extra}")

        keyframes = part.findall("Keyframe")
        if not keyframes:
            keyframes = part.findall(".//Keyframe")
        if not keyframes:
            print("  keyframes:      <none>")
        else:
            print("  keyframes:")
            for keyframe in keyframes:
                time_value = keyframe.attrib.get("time", "?")
                rest = format_attrs(dict(keyframe.attrib), skip={"time"})
                print(f"    time={time_value!r} {rest}".rstrip())
        print()

    if printed == 0:
        if args.name_filter:
            print(f"No parts matched --name-filter {args.name_filter!r}.")
        else:
            print("Animation contains no Part elements.")
        return 1

    print(f"Printed {printed} animation part(s).")
    print(f"Scene nodes indexed: {len(scene_index)}")
    print(f"I3D mappings indexed: {len(mappings_by_id)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
