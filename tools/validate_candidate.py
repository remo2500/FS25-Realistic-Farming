#!/usr/bin/env python3
"""Static validation helper for FS25 Realistic Farming candidate ZIPs.

This does not replace in-game testing. It checks archive integrity, XML/I3D parsing,
required project files, and project-authority invariants that can be proven without
running Farming Simulator.
"""

from __future__ import annotations

import argparse
import io
import sys
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""


def xml_from_zip(zf: zipfile.ZipFile, path: str) -> ET.Element:
    return ET.parse(io.BytesIO(zf.read(path))).getroot()


def text_from_zip(zf: zipfile.ZipFile, path: str) -> str:
    return zf.read(path).decode("utf-8-sig")


def validate_common(zf: zipfile.ZipFile) -> list[Check]:
    checks: list[Check] = []
    bad = zf.testzip()
    checks.append(Check("ZIP CRC/integrity", bad is None, "PASS" if bad is None else f"bad file: {bad}"))
    names = zf.namelist()
    checks.append(Check("modDesc.xml at archive root", "modDesc.xml" in names))

    parse_failures: list[str] = []
    for name in names:
        if name.lower().endswith((".xml", ".i3d")):
            try:
                xml_from_zip(zf, name)
            except Exception as exc:
                parse_failures.append(f"{name}: {exc}")
    checks.append(Check("XML/I3D parse", not parse_failures, "; ".join(parse_failures[:5])))
    return checks


def find_fill_units(root: ET.Element) -> list[ET.Element]:
    return root.findall("./fillUnit/fillUnitConfigurations/fillUnitConfiguration/fillUnits/fillUnit")


def find_named_i3d_node(root: ET.Element, name: str) -> ET.Element | None:
    for node in root.iter():
        if node.attrib.get("name") == name:
            return node
    return None


def parse_vec3(value: str | None) -> tuple[float, float, float] | None:
    if value is None:
        return None
    try:
        parts = [float(v) for v in value.split()]
    except ValueError:
        return None
    if len(parts) != 3:
        return None
    return parts[0], parts[1], parts[2]


def validate_named_node_z(i3d_root: ET.Element, expected: dict[str, float], tolerance: float = 0.005) -> Check:
    problems: list[str] = []
    found: dict[str, float] = {}
    for name, expected_z in expected.items():
        node = find_named_i3d_node(i3d_root, name)
        if node is None:
            problems.append(f"{name}: missing")
            continue
        translation = parse_vec3(node.attrib.get("translation"))
        if translation is None:
            problems.append(f"{name}: no parseable translation")
            continue
        z = translation[2]
        found[name] = z
        if abs(z - expected_z) > tolerance:
            problems.append(f"{name}: z={z:.6f}, expected {expected_z:.6f}")
    return Check("load/unload node Z authority", not problems, "; ".join(problems) if problems else str(found))


def validate_bourgault(zf: zipfile.ZipFile, *, v7: bool) -> list[Check]:
    checks: list[Check] = []
    vehicle_path = "xml/Series_7950B.xml"
    i3d_path = "i3d/Series_7950B.i3d"
    script_path = "scripts/FourTankCompat.lua"

    for path in (vehicle_path, i3d_path, script_path):
        checks.append(Check(f"required file {path}", path in zf.namelist()))
    if not all(c.ok for c in checks[-3:]):
        return checks

    vehicle = xml_from_zip(zf, vehicle_path)
    units = find_fill_units(vehicle)
    caps = [int(float(u.attrib.get("capacity", "0"))) for u in units]
    checks.append(Check("four fill units", len(units) == 4, f"found {len(units)}"))
    checks.append(Check("capacity authority", caps == [9691, 1938, 4228, 17618], f"found {caps}"))
    checks.append(Check("capacity total 33475 L", sum(caps) == 33475, f"found {sum(caps)}"))
    categories = [u.attrib.get("fillTypeCategories") for u in units]
    checks.append(Check("all tanks use seeds fertilizer categories", categories == ["seeds fertilizer"] * 4, str(categories)))

    roots = []
    for unit in units:
        node = unit.find("exactFillRootNode")
        roots.append(node.attrib.get("node") if node is not None else None)
    checks.append(Check(
        "four exact fill roots",
        roots == ["exactFillRootNodeTank1", "exactFillRootNodeTank2", "exactFillRootNodeTank3", "exactFillRootNodeTank4"],
        str(roots),
    ))

    volumes = vehicle.findall("./fillVolume/fillVolumeConfigurations/fillVolumeConfiguration/volumes/volume")
    mapping = [(v.attrib.get("node"), v.attrib.get("fillUnitIndex"), v.attrib.get("fillUnitFactor")) for v in volumes]
    required = {
        ("fillVolumeTank1", "1", None),
        ("fillVolumeTank2", "2", None),
        ("fillVolumeTank3", "3", None),
        ("fillVolumeTank4", "4", "0.82"),
        ("fillVolumeTank4Flex", "4", "0.18"),
    }
    checks.append(Check("five physical fill volumes including 82/18 Tank 4 split", required.issubset(set(mapping)), str(mapping)))

    covers = vehicle.findall("./cover/coverConfigurations/coverConfiguration/cover")
    stops = [c.attrib.get("openAnimationStopTime") for c in covers]
    checks.append(Check("four conveyor selector cover states", stops == ["0.000", "0.200", "0.400", "0.600"], str(stops)))
    if covers:
        last = covers[-1]
        checks.append(Check(
            "final state closes to transport endpoint 1.000",
            last.attrib.get("closeAnimation") == "loadingPipe" and last.attrib.get("closeAnimationStopTime") == "1.000",
            str(last.attrib),
        ))

    sprayer = vehicle.find("./sprayer")
    checks.append(Check(
        "cart sprayer representative points to Tank 1/unload 1",
        sprayer is not None and sprayer.attrib.get("fillUnitIndex") == "1" and sprayer.attrib.get("unloadInfoIndex") == "1",
        str(sprayer.attrib if sprayer is not None else None),
    ))

    i3d_root = xml_from_zip(zf, i3d_path)
    i3d = text_from_zip(zf, i3d_path)
    required_names = [
        "fillVolumeTank1", "fillVolumeTank2", "fillVolumeTank3", "fillVolumeTank4", "fillVolumeTank4Flex",
        "loadInfoTank1", "loadInfoTank2", "loadInfoTank3", "loadInfoTank4",
        "unloadInfoTank1", "unloadInfoTank2", "unloadInfoTank3", "unloadInfoTank4",
        "exactFillRootNodeTank1", "exactFillRootNodeTank2", "exactFillRootNodeTank3", "exactFillRootNodeTank4",
        "tankFlapsFront", "tankFlapsBack",
    ]
    missing = [name for name in required_names if f'name="{name}"' not in i3d]
    checks.append(Check("required I3D nodes present", not missing, f"missing {missing}"))

    expected_z = {
        "loadInfoTank1": 2.121,
        "loadInfoTank2": 0.721,
        "loadInfoTank3": -0.678,
        "loadInfoTank4": -1.792,
        "unloadInfoTank1": 2.121,
        "unloadInfoTank2": 0.721,
        "unloadInfoTank3": -0.678,
        "unloadInfoTank4": -1.792,
    }
    checks.append(validate_named_node_z(i3d_root, expected_z))

    script = text_from_zip(zf, script_path)
    checks.append(Check("compat bridge raises FILLTYPE_CHANGE", "VehicleStateChange.FILLTYPE_CHANGE" in script))
    checks.append(Check("compat bridge targets four units", "for i = 1, 4 do" in script))

    if v7:
        broad_markers = [
            'string.find(string.upper(tostring(name)), "SEED"',
            'string.find(name, "SEED"',
        ]
        checks.append(Check(
            "V7 rejects broad SEED substring matcher",
            not any(marker in script for marker in broad_markers),
        ))
        checks.append(Check(
            "V7 uses suffix seed fallback",
            'string.sub(upperName, -4) == "SEED"' in script and 'upperName ~= "SEEDS"' in script,
        ))
        checks.append(Check(
            "V7 does not union arbitrary existing tank products",
            "addSet(desired, unit.supportedFillTypes)" not in script,
        ))
        checks.append(Check(
            "V7 uses category authority",
            'getFillTypesByCategoryNames("seeds fertilizer")' in script,
        ))

        # The validator can prove that both physical flap groups exist, but the exact animation
        # keyframe semantics vary by donor I3D export. V7 therefore records flap-state review as
        # a separate mandatory engineering gate rather than pretending node presence proves timing.
        checks.append(Check(
            "V7 physical flap groups present for mandatory timing audit",
            'name="tankFlapsFront"' in i3d and 'name="tankFlapsBack"' in i3d,
            "animation timing must still be reviewed against the 0.400 Tank 3 invariant",
        ))

    return checks


def validate_seedhawk(zf: zipfile.ZipFile) -> list[Check]:
    checks: list[Check] = []
    vehicle_path = "seedHawk660AirCart.xml"
    script_path = "scripts/ThreeTankCompat.lua"

    for path in (vehicle_path, script_path):
        checks.append(Check(f"required file {path}", path in zf.namelist()))
    if not all(c.ok for c in checks[-2:]):
        return checks

    vehicle = xml_from_zip(zf, vehicle_path)
    units = find_fill_units(vehicle)
    caps = [int(float(u.attrib.get("capacity", "0"))) for u in units]
    checks.append(Check("three fill units", len(units) == 3, f"found {len(units)}"))
    checks.append(Check("capacity authority", caps == [5600, 5600, 10600], f"found {caps}"))
    checks.append(Check("capacity total 21800 L", sum(caps) == 21800, f"found {sum(caps)}"))
    categories = [u.attrib.get("fillTypeCategories") for u in units]
    checks.append(Check("all tanks use seeds fertilizer categories", categories == ["seeds fertilizer"] * 3, str(categories)))

    roots = []
    for unit in units:
        node = unit.find("exactFillRootNode")
        roots.append(node.attrib.get("node") if node is not None else None)
    checks.append(Check(
        "three exact fill roots",
        roots == ["exactFillRootNodeSeeds", "exactFillRootNodeSeedsMiddle", "exactFillRootNodeFertilizer"],
        str(roots),
    ))

    sprayer = vehicle.find("./sprayer")
    checks.append(Check(
        "sprayer has no unsupported loadInfoIndex",
        sprayer is not None and sprayer.attrib.get("fillUnitIndex") == "3" and sprayer.attrib.get("unloadInfoIndex") == "3" and "loadInfoIndex" not in sprayer.attrib,
        str(sprayer.attrib if sprayer is not None else None),
    ))

    configurations = vehicle.findall("./cover/coverConfigurations/coverConfiguration")
    conveyor = None
    for configuration in configurations:
        candidate = configuration.findall("cover")
        if len(candidate) == 3:
            conveyor = candidate
            break
    if conveyor is None:
        checks.append(Check("three-state conveyor cover configuration", False, "not found"))
    else:
        stops = [c.attrib.get("openAnimationStopTime") for c in conveyor]
        checks.append(Check("three-state conveyor cover configuration", stops == ["0", "0.234", "0.534"], str(stops)))
        last = conveyor[-1]
        checks.append(Check(
            "final conveyor state closes to 1",
            last.attrib.get("closeAnimation") == "loadingPipe" and last.attrib.get("closeAnimationStopTime") == "1",
            str(last.attrib),
        ))

    script = text_from_zip(zf, script_path)
    checks.append(Check("compat bridge raises FILLTYPE_CHANGE", "VehicleStateChange.FILLTYPE_CHANGE" in script))
    checks.append(Check("compat bridge targets three units", "for i = 1, 3 do" in script))
    checks.append(Check(
        "custom seed fallback uses SEED suffix rather than broad substring",
        'string.sub(upperName, -4) == "SEED"' in script and 'string.find(string.upper(tostring(name)), "SEED"' not in script,
    ))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("zipfile", help="candidate FS25 mod ZIP")
    parser.add_argument(
        "--profile",
        choices=["bourgault7950-v6", "bourgault7950-v7", "seedhawk660-v3"],
        required=True,
    )
    args = parser.parse_args()

    try:
        with zipfile.ZipFile(args.zipfile, "r") as zf:
            checks = validate_common(zf)
            if args.profile == "bourgault7950-v6":
                checks.extend(validate_bourgault(zf, v7=False))
            elif args.profile == "bourgault7950-v7":
                checks.extend(validate_bourgault(zf, v7=True))
            else:
                checks.extend(validate_seedhawk(zf))
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2

    failed = 0
    for check in checks:
        status = "PASS" if check.ok else "FAIL"
        suffix = f" - {check.detail}" if check.detail else ""
        print(f"[{status}] {check.name}{suffix}")
        failed += 0 if check.ok else 1

    print(f"\n{len(checks) - failed}/{len(checks)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
