#!/usr/bin/env python3
"""Inspect GIANTS vehicle animation definitions against their I3D hierarchy.

GIANTS vehicle animations such as ``loadingPipe`` are normally defined in the vehicle
XML (``<animations><animation><part .../>``). The vehicle XML's ``i3dMappings`` then
resolves symbolic part names to paths in the referenced I3D scene.

This helper reads both files from an FS25 mod ZIP or extracted mod directory and prints:

- every animation part/segment;
- the symbolic node ID used by the vehicle XML;
- the mapped I3D scene path;
- the resolved I3D node name and static transform;
- the parent scene chain;
- optional local animation-state estimates at requested times.

Primary project use::

    python tools/extract_i3d_animation.py FS25_Bourgault_3320_4Tank_V6_Engineering.zip \
        --vehicle-path xml/Series_7950B.xml \
        --i3d-path i3d/Series_7950B.i3d \
        --animation loadingPipe \
        --times 0,2,4,6,10

The tool is read-only. It does not calculate a promoted world-space conveyor solution;
it exposes the exact donor/candidate animation and hierarchy required before doing that
kinematic work.
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


@dataclass
class SceneNode:
    path: str
    tag: str
    name: str
    attrs: dict[str, str]


def normalize_scene_path(value: str | None) -> str | None:
    """Normalize a GIANTS mapping path to the portion below the I3D <Scene> root."""
    if value is None:
        return None
    value = value.strip()
    if ">" in value:
        # For normal vehicle mappings such as 0>0|4|0, the prefix before > identifies
        # the loaded I3D/component root. The remaining path addresses the I3D scene.
        return value.split(">", 1)[1]
    return value


def read_from_source(source: pathlib.Path, member_path: str) -> bytes:
    if source.is_dir():
        target = source / pathlib.PurePosixPath(member_path)
        if not target.is_file():
            raise FileNotFoundError(f"{member_path!r} not found under {source}")
        return target.read_bytes()

    if source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source, "r") as zf:
            if member_path not in zf.namelist():
                raise FileNotFoundError(f"{member_path!r} not found in {source}")
            return zf.read(member_path)

    raise ValueError("source must be an FS25 mod ZIP or an extracted mod directory")


def parse_xml(payload: bytes) -> ET.Element:
    return ET.parse(io.BytesIO(payload)).getroot()


def build_scene_index(i3d_root: ET.Element) -> dict[str, SceneNode]:
    scene = i3d_root.find("Scene")
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


def build_mapping_index(vehicle_root: ET.Element) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Return normalized I3D-path->mapping IDs and mapping ID->normalized path."""
    by_path: dict[str, list[str]] = defaultdict(list)
    by_id: dict[str, str] = {}

    mappings = vehicle_root.find("i3dMappings")
    if mappings is None:
        mappings = vehicle_root.find(".//i3dMappings")
    if mappings is None:
        return dict(by_path), by_id

    for mapping in mappings.findall("i3dMapping"):
        mapping_id = mapping.attrib.get("id")
        path = normalize_scene_path(mapping.attrib.get("node"))
        if mapping_id and path is not None:
            by_path[path].append(mapping_id)
            by_id[mapping_id] = path

    return dict(by_path), by_id


def find_animation(vehicle_root: ET.Element, animation_name: str) -> ET.Element | None:
    animations = vehicle_root.find("animations")
    if animations is None:
        animations = vehicle_root.find(".//animations")
    if animations is None:
        return None
    for animation in animations.findall("animation"):
        if animation.attrib.get("name") == animation_name:
            return animation
    return None


def available_animations(vehicle_root: ET.Element) -> list[str]:
    animations = vehicle_root.find("animations")
    if animations is None:
        animations = vehicle_root.find(".//animations")
    if animations is None:
        return []
    return [a.attrib.get("name", "<unnamed>") for a in animations.findall("animation")]


def format_attrs(attrs: dict[str, str], skip: set[str] | None = None) -> str:
    skip = skip or set()
    return " ".join(f"{key}={value!r}" for key, value in attrs.items() if key not in skip)


def parent_path(path: str) -> str | None:
    if "|" not in path:
        return None
    return path.rsplit("|", 1)[0]


def describe_parent_chain(path: str, scene_index: dict[str, SceneNode]) -> str:
    chain: list[str] = []
    current: str | None = path
    while current is not None:
        node = scene_index.get(current)
        if node is None:
            chain.append(f"{current}:<unresolved>")
        else:
            chain.append(f"{current}:{node.name or node.tag}")
        current = parent_path(current)
    chain.reverse()
    return " -> ".join(chain)


def parse_vector(value: str | None) -> list[float] | None:
    if value is None:
        return None
    try:
        result = [float(token) for token in value.split()]
    except ValueError:
        return None
    return result if result else None


def lerp_vector(start: str | None, end: str | None, alpha: float) -> str | None:
    a = parse_vector(start)
    b = parse_vector(end)
    if a is None or b is None or len(a) != len(b):
        return None
    values = [x + (y - x) * alpha for x, y in zip(a, b)]
    return " ".join(f"{value:.6f}" for value in values)


def parse_times(value: str) -> list[float]:
    if not value.strip():
        return []
    return [float(token.strip()) for token in value.split(",") if token.strip()]


def segment_state(part: ET.Element, time_value: float) -> list[str]:
    """Return local transform estimates for one active animation segment.

    This is simple linear interpolation of the XML segment endpoints. It is useful for
    selector-stop auditing, but it is intentionally not called a world-space kinematic
    solution.
    """
    try:
        start_time = float(part.attrib.get("startTime", "0"))
        end_time = float(part.attrib.get("endTime", str(start_time)))
    except ValueError:
        return []

    eps = 1e-6
    if time_value < start_time - eps or time_value > end_time + eps:
        return []

    if abs(end_time - start_time) <= eps:
        alpha = 1.0
    else:
        alpha = min(1.0, max(0.0, (time_value - start_time) / (end_time - start_time)))

    states: list[str] = []
    for label, start_key, end_key in (
        ("rot", "startRot", "endRot"),
        ("trans", "startTrans", "endTrans"),
        ("scale", "startScale", "endScale"),
    ):
        start_value = part.attrib.get(start_key)
        end_value = part.attrib.get(end_key)
        if start_value is None and end_value is None:
            continue
        if start_value is None:
            start_value = end_value
        if end_value is None:
            end_value = start_value
        interpolated = lerp_vector(start_value, end_value, alpha)
        states.append(f"{label}={interpolated or end_value}")

    if "startVisibility" in part.attrib or "endVisibility" in part.attrib:
        # Visibility is discrete; report endpoints and alpha instead of guessing GIANTS'
        # exact switching rule.
        states.append(
            "visibility="
            f"{part.attrib.get('startVisibility', '?')}->{part.attrib.get('endVisibility', '?')}"
            f" alpha={alpha:.3f}"
        )

    return states


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect a vehicle XML animation and resolve its nodes into the I3D scene"
    )
    parser.add_argument("source", help="FS25 mod ZIP or extracted mod directory")
    parser.add_argument(
        "--vehicle-path",
        default="xml/Series_7950B.xml",
        help="vehicle XML path inside the mod",
    )
    parser.add_argument(
        "--i3d-path",
        default="i3d/Series_7950B.i3d",
        help="I3D path inside the mod",
    )
    parser.add_argument("--animation", default="loadingPipe", help="vehicle animation name")
    parser.add_argument(
        "--name-filter",
        default="",
        help="optional case-insensitive substring applied to mapping ID/path/resolved node name",
    )
    parser.add_argument(
        "--times",
        default="",
        help="optional comma-separated animation times (seconds), e.g. 0,2,4,6,10",
    )
    args = parser.parse_args()

    source = pathlib.Path(args.source)
    try:
        vehicle_root = parse_xml(read_from_source(source, args.vehicle_path))
        i3d_root = parse_xml(read_from_source(source, args.i3d_path))
        requested_times = parse_times(args.times)
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2

    scene_index = build_scene_index(i3d_root)
    mappings_by_path, mappings_by_id = build_mapping_index(vehicle_root)
    animation = find_animation(vehicle_root, args.animation)

    if animation is None:
        print(f"Animation {args.animation!r} not found in {args.vehicle_path}.", file=sys.stderr)
        print("Available animations:")
        for name in available_animations(vehicle_root):
            print(f"  - {name}")
        return 1

    print(f"Source: {source}")
    print(f"Vehicle XML: {args.vehicle_path}")
    print(f"I3D: {args.i3d_path}")
    print(f"Animation: {args.animation}")
    print(f"Animation attributes: {format_attrs(dict(animation.attrib))}")
    print()

    selected_parts: list[ET.Element] = []
    for part in animation.findall("part"):
        mapping_id = part.attrib.get("node", "")
        path = mappings_by_id.get(mapping_id, normalize_scene_path(mapping_id) or mapping_id)
        scene_node = scene_index.get(path)
        searchable = " ".join(
            [mapping_id, path, scene_node.name if scene_node is not None else ""]
        ).lower()
        if args.name_filter and args.name_filter.lower() not in searchable:
            continue
        selected_parts.append(part)

    if not selected_parts:
        print("No animation parts matched the requested filter." if args.name_filter else "Animation has no part elements.")
        return 1

    for part_index, part in enumerate(selected_parts, start=1):
        mapping_id = part.attrib.get("node", "")
        path = mappings_by_id.get(mapping_id, normalize_scene_path(mapping_id) or mapping_id)
        scene_node = scene_index.get(path)
        other_ids = mappings_by_path.get(path, [])

        print(f"PART {part_index}")
        print(f"  animation node: {mapping_id}")
        print(f"  I3D path:       {path}")
        if scene_node is not None:
            print(f"  scene tag/name: {scene_node.tag} / {scene_node.name or '<unnamed>'}")
            static_attrs = {
                key: scene_node.attrs[key]
                for key in ("translation", "rotation", "scale", "visibility")
                if key in scene_node.attrs
            }
            if static_attrs:
                print(f"  static:         {format_attrs(static_attrs)}")
            print(f"  parent chain:   {describe_parent_chain(path, scene_index)}")
        else:
            print("  scene node:     <unresolved>")
        print(f"  mapping IDs:    {', '.join(other_ids) if other_ids else '<none>'}")
        print(f"  segment:        {format_attrs(dict(part.attrib), skip={'node'})}")
        print()

    if requested_times:
        print("LOCAL ANIMATION STATE ESTIMATES")
        print("(linear interpolation of vehicle-XML segment endpoints; not world-space kinematics)")
        for time_value in requested_times:
            print(f"\n  t={time_value:g} s")
            any_state = False
            for part in selected_parts:
                states = segment_state(part, time_value)
                if not states:
                    continue
                any_state = True
                mapping_id = part.attrib.get("node", "<unnamed>")
                print(f"    {mapping_id}: {'; '.join(states) if states else '<active segment>'}")
            if not any_state:
                print("    <no selected part segment active at this exact time>")

    print()
    print(f"Printed {len(selected_parts)} animation part segment(s).")
    print(f"Scene nodes indexed: {len(scene_index)}")
    print(f"Vehicle i3dMappings indexed: {len(mappings_by_id)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
