#!/usr/bin/env python3
"""Static validation helper for FS25 Realistic Farming candidate ZIPs.

This does not replace in-game testing. It checks archive integrity, XML/I3D parsing,
required project files, and project-authority invariants that can be proven without
running Farming Simulator.
"""

from __future__ import annotations

import argparse
import io
import math
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


def vec_lerp(
    a: tuple[float, float, float],
    b: tuple[float, float, float],
    alpha: float,
) -> tuple[float, float, float]:
    return tuple(x + (y - x) * alpha for x, y in zip(a, b))  # type: ignore[return-value]


def find_vehicle_animation(root: ET.Element, name: str) -> ET.Element | None:
    animations = root.find("./animations")
    if animations is None:
        return None
    for animation in animations.findall("animation"):
        if animation.attrib.get("name") == name:
            return animation
    return None


def animation_duration(animation: ET.Element) -> float:
    duration = 0.0
    for part in animation.findall("part"):
        try:
            duration = max(duration, float(part.attrib.get("endTime", "0")))
        except ValueError:
            pass
    return duration


def sample_animation_vec3(
    animation: ET.Element,
    node: str,
    normalized_time: float,
    start_attr: str,
    end_attr: str,
) -> tuple[float, float, float] | None:
    """Sample one vector property using GIANTS vehicle-animation segment semantics.

    Before the first segment, the first segment's start value is held. Between
    segments, the previous end value is held. After the final segment, the final end
    value is held. Inside a segment, endpoints are linearly interpolated.
    """
    segments: list[tuple[float, float, tuple[float, float, float], tuple[float, float, float]]] = []
    for part in animation.findall("part"):
        if part.attrib.get("node") != node:
            continue
        start_vec = parse_vec3(part.attrib.get(start_attr))
        end_vec = parse_vec3(part.attrib.get(end_attr))
        if start_vec is None and end_vec is None:
            continue
        if start_vec is None:
            start_vec = end_vec
        if end_vec is None:
            end_vec = start_vec
        if start_vec is None or end_vec is None:
            continue
        try:
            start_time = float(part.attrib.get("startTime", "0"))
            end_time = float(part.attrib.get("endTime", str(start_time)))
        except ValueError:
            continue
        segments.append((start_time, end_time, start_vec, end_vec))

    if not segments:
        return None

    segments.sort(key=lambda item: (item[0], item[1]))
    duration = animation_duration(animation)
    if duration <= 0:
        return None
    t = max(0.0, min(1.0, normalized_time)) * duration

    if t <= segments[0][0]:
        return segments[0][2]

    previous_end = segments[0][3]
    for start_time, end_time, start_vec, end_vec in segments:
        if t < start_time:
            return previous_end
        if start_time <= t <= end_time:
            if abs(end_time - start_time) < 1e-9:
                return end_vec
            alpha = (t - start_time) / (end_time - start_time)
            return vec_lerp(start_vec, end_vec, alpha)
        previous_end = end_vec

    return segments[-1][3]


def vec_close(
    actual: tuple[float, float, float] | None,
    expected: tuple[float, float, float],
    tolerance: float,
) -> bool:
    return actual is not None and all(abs(a - e) <= tolerance for a, e in zip(actual, expected))


def validate_v7_flap_animation(vehicle: ET.Element) -> Check:
    animation = find_vehicle_animation(vehicle, "loadingPipe")
    if animation is None:
        return Check("V7 flap animation timing", False, "loadingPipe animation missing")

    expected = [
        (0.200, (0.0, 0.0, -100.0), (0.0, 0.0, 0.0), "Tank 2"),
        (0.400, (0.0, 0.0, 0.0), (0.0, 0.0, -100.0), "Tank 3"),
        (0.600, (0.0, 0.0, 0.0), (0.0, 0.0, -100.0), "Tank 4"),
        (1.000, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), "transport"),
    ]

    problems: list[str] = []
    for normalized, front_expected, back_expected, label in expected:
        front = sample_animation_vec3(
            animation, "tankFlapsFront", normalized, "startRot", "endRot"
        )
        back = sample_animation_vec3(
            animation, "tankFlapsBack", normalized, "startRot", "endRot"
        )
        if not vec_close(front, front_expected, 1.0):
            problems.append(f"{label} front={front}, expected~{front_expected}")
        if not vec_close(back, back_expected, 1.0):
            problems.append(f"{label} back={back}, expected~{back_expected}")

    return Check(
        "V7 flap animation timing",
        not problems,
        "; ".join(problems) if problems else "Tank2/Tank3/Tank4/transport states verified",
    )


def rot_y(degrees: float) -> tuple[tuple[float, float, float], ...]:
    a = math.radians(degrees)
    c, s = math.cos(a), math.sin(a)
    return ((c, 0.0, s), (0.0, 1.0, 0.0), (-s, 0.0, c))


def rot_x(degrees: float) -> tuple[tuple[float, float, float], ...]:
    a = math.radians(degrees)
    c, s = math.cos(a), math.sin(a)
    return ((1.0, 0.0, 0.0), (0.0, c, -s), (0.0, s, c))


def mat_vec(
    matrix: tuple[tuple[float, float, float], ...],
    vector: tuple[float, float, float],
) -> tuple[float, float, float]:
    return tuple(
        sum(matrix[row][col] * vector[col] for col in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def vec_add(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> tuple[float, float, float]:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def validate_v7_tank1_kinematics(vehicle: ET.Element, i3d_root: ET.Element) -> Check:
    animation = find_vehicle_animation(vehicle, "loadingPipe")
    if animation is None:
        return Check("V7 Tank 1 pipe kinematics", False, "loadingPipe animation missing")

    rotations: dict[str, tuple[float, float, float] | None] = {
        node: sample_animation_vec3(animation, node, 0.0, "startRot", "endRot")
        for node in ("overloadingArm01", "overloadingArm02", "overloadingArm03", "overloadingArm04")
    }
    arm4_translation = sample_animation_vec3(
        animation, "overloadingArm04", 0.0, "startTrans", "endTrans"
    )

    missing = [name for name, value in rotations.items() if value is None]
    if arm4_translation is None:
        missing.append("overloadingArm04 translation")
    if missing:
        return Check("V7 Tank 1 pipe kinematics", False, f"missing animation values: {missing}")

    needed_nodes = {
        name: find_named_i3d_node(i3d_root, name)
        for name in ("overloadingArm01", "overloadingArm02", "overloadingArm03", "pipeEffect")
    }
    missing_nodes = [name for name, node in needed_nodes.items() if node is None]
    if missing_nodes:
        return Check("V7 Tank 1 pipe kinematics", False, f"missing I3D nodes: {missing_nodes}")

    arm1_pivot = parse_vec3(needed_nodes["overloadingArm01"].attrib.get("translation"))  # type: ignore[union-attr]
    arm2_pivot = parse_vec3(needed_nodes["overloadingArm02"].attrib.get("translation"))  # type: ignore[union-attr]
    arm3_pivot = parse_vec3(needed_nodes["overloadingArm03"].attrib.get("translation"))  # type: ignore[union-attr]
    pipe_local = parse_vec3(needed_nodes["pipeEffect"].attrib.get("translation"))  # type: ignore[union-attr]
    if None in (arm1_pivot, arm2_pivot, arm3_pivot, pipe_local):
        return Check("V7 Tank 1 pipe kinematics", False, "unparseable conveyor I3D translation")

    a1 = rotations["overloadingArm01"][1]  # type: ignore[index]
    a2 = rotations["overloadingArm02"][1]  # type: ignore[index]
    a3 = rotations["overloadingArm03"][1]  # type: ignore[index]
    a4 = rotations["overloadingArm04"][0]  # type: ignore[index]

    point = vec_add(arm4_translation, mat_vec(rot_x(a4), pipe_local))  # type: ignore[arg-type]
    point = vec_add(arm3_pivot, mat_vec(rot_y(a3), point))  # type: ignore[arg-type]
    point = vec_add(arm2_pivot, mat_vec(rot_y(a2), point))  # type: ignore[arg-type]
    point = vec_add(arm1_pivot, mat_vec(rot_y(a1), point))  # type: ignore[arg-type]
    x, y, z = point

    problems: list[str] = []
    if not (1.790 <= z <= 2.452):
        problems.append(f"Z={z:.6f} outside +1.790..+2.452")
    if abs(x) > 0.25:
        problems.append(f"X={x:.6f} exceeds +/-0.25 m centerline tolerance")
    if a1 > 108.1:
        problems.append(f"Arm1={a1:.3f} exceeds V6 overtravel ceiling")
    if a2 < -65.7:
        problems.append(f"Arm2={a2:.3f} exceeds V6 overtravel ceiling")

    detail = (
        f"pipe=({x:.6f},{y:.6f},{z:.6f}); "
        f"angles=({a1:.3f},{a2:.3f},{a3:.3f},{a4:.3f})"
    )
    if problems:
        detail += "; " + "; ".join(problems)
    return Check("V7 Tank 1 pipe kinematics", not problems, detail)


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
        checks.append(validate_v7_flap_animation(vehicle))
        checks.append(validate_v7_tank1_kinematics(vehicle, i3d_root))

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
