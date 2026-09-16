#!/usr/bin/env python3
"""Forward-kinematics checker for the Bourgault 7950 load/unload conveyor.

The constants in this file are factual transforms recovered from the user-supplied
Hispano 4-Tank V3 reference archive documented in:

    equipment/bourgault_7950/reference/README.md

The model is deliberately small and donor-safe: it stores pivot/effect coordinates,
not donor meshes or complete model files.

The rotation convention has been cross-checked against the later V6 audit. With the
reported V6 Tank-1 angles 107.99 / -65.60 / -135 / 21 degrees, the model produces
pipe-effect Z ~= +1.6515 m, matching the documented V6 result (+1.650 m) within about
1.5 mm.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from typing import Iterable

Vec3 = tuple[float, float, float]
Mat3 = tuple[Vec3, Vec3, Vec3]


# Recovered 7950 conveyor hierarchy (vehicle-local coordinates).
ARM1_PIVOT: Vec3 = (-1.47003, 1.56863, -1.22386)
ARM2_PIVOT: Vec3 = (-0.173656, 0.727869, -3.68031)
ARM3_PIVOT: Vec3 = (-0.241337, 0.219075, 1.66861)
DONOR_ARM4_TRANSLATION: Vec3 = (0.0, 0.28, -0.074)
PIPE_EFFECT_LOCAL: Vec3 = (-0.00384, -0.258395, -4.10928)

# Hydraulic-base/reference coordinates used only for relative extension comparisons.
ARM1_HYD_BASE: Vec3 = (-0.971211, 1.46645, -2.04846)
ARM1_HYD_REF: Vec3 = (0.094832, -0.101224, -0.222905)
ARM2_HYD_BASE: Vec3 = (-0.126765, 0.929425, -2.72392)
ARM2_HYD_REF: Vec3 = (-0.023452, 0.201557, 0.237692)

DONOR_LOADING_ANGLES = (100.0, -50.0, -135.0, 21.0)


@dataclass(frozen=True)
class PoseResult:
    angles: tuple[float, float, float, float]
    arm4_translation: Vec3
    pipe_effect: Vec3
    arm1_hydraulic_length: float
    arm2_hydraulic_length: float


def add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def norm(v: Vec3) -> float:
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def mat_vec(m: Mat3, v: Vec3) -> Vec3:
    return (
        m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
        m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
        m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2],
    )


def rot_y(degrees: float) -> Mat3:
    a = math.radians(degrees)
    c, s = math.cos(a), math.sin(a)
    return ((c, 0.0, s), (0.0, 1.0, 0.0), (-s, 0.0, c))


def rot_x(degrees: float) -> Mat3:
    a = math.radians(degrees)
    c, s = math.cos(a), math.sin(a)
    return ((1.0, 0.0, 0.0), (0.0, c, -s), (0.0, s, c))


def pipe_effect_position(
    arm1: float,
    arm2: float,
    arm3: float,
    arm4: float,
    arm4_translation: Vec3 = DONOR_ARM4_TRANSLATION,
) -> Vec3:
    p = add(arm4_translation, mat_vec(rot_x(arm4), PIPE_EFFECT_LOCAL))
    p = add(ARM3_PIVOT, mat_vec(rot_y(arm3), p))
    p = add(ARM2_PIVOT, mat_vec(rot_y(arm2), p))
    p = add(ARM1_PIVOT, mat_vec(rot_y(arm1), p))
    return p


def arm1_hydraulic_length(arm1: float) -> float:
    ref = add(ARM1_PIVOT, mat_vec(rot_y(arm1), ARM1_HYD_REF))
    return norm(sub(ref, ARM1_HYD_BASE))


def arm2_hydraulic_length(arm2: float) -> float:
    ref = add(ARM2_PIVOT, mat_vec(rot_y(arm2), ARM2_HYD_REF))
    return norm(sub(ref, ARM2_HYD_BASE))


def evaluate(
    angles: Iterable[float], arm4_translation: Vec3 = DONOR_ARM4_TRANSLATION
) -> PoseResult:
    a1, a2, a3, a4 = tuple(float(v) for v in angles)
    return PoseResult(
        angles=(a1, a2, a3, a4),
        arm4_translation=arm4_translation,
        pipe_effect=pipe_effect_position(a1, a2, a3, a4, arm4_translation),
        arm1_hydraulic_length=arm1_hydraulic_length(a1),
        arm2_hydraulic_length=arm2_hydraulic_length(a2),
    )


def pct_delta(value: float, baseline: float) -> float:
    return (value / baseline - 1.0) * 100.0


def named_poses() -> dict[str, tuple[float, float, float, float]]:
    return {
        "v3_donor_loading": (100.0, -50.0, -135.0, 21.0),
        "v6_tank1_audit_crosscheck": (107.99, -65.60, -135.0, 21.0),
        "v7_tank1_z1p790": (104.483805, -58.559467, -144.472086, 21.0),
        "v7_tank1_z1p900_recommended": (105.164095, -59.356622, -145.314298, 21.0),
        "v7_tank1_z2p121_center": (106.584529, -60.997442, -146.992740, 21.0),
    }


def result_dict(name: str, result: PoseResult) -> dict[str, object]:
    donor = evaluate(DONOR_LOADING_ANGLES)
    return {
        "name": name,
        "anglesDegrees": list(result.angles),
        "arm4Translation": list(result.arm4_translation),
        "pipeEffectXYZ": list(result.pipe_effect),
        "arm1HydraulicLength": result.arm1_hydraulic_length,
        "arm1HydraulicDeltaPctVsDonor": pct_delta(
            result.arm1_hydraulic_length, donor.arm1_hydraulic_length
        ),
        "arm2HydraulicLength": result.arm2_hydraulic_length,
        "arm2HydraulicDeltaPctVsDonor": pct_delta(
            result.arm2_hydraulic_length, donor.arm2_hydraulic_length
        ),
    }


def print_result(name: str, result: PoseResult) -> None:
    donor = evaluate(DONOR_LOADING_ANGLES)
    x, y, z = result.pipe_effect
    print(name)
    print("  angles [A1 A2 A3 A4]: " + " ".join(f"{v:.6f}" for v in result.angles))
    print(
        "  arm4 translation:     "
        + " ".join(f"{v:.6f}" for v in result.arm4_translation)
    )
    print(f"  pipe effect XYZ:       {x:.6f} {y:.6f} {z:.6f}")
    print(
        f"  arm1 hydraulic:        {result.arm1_hydraulic_length:.6f} m "
        f"({pct_delta(result.arm1_hydraulic_length, donor.arm1_hydraulic_length):+.3f}% vs donor)"
    )
    print(
        f"  arm2 hydraulic:        {result.arm2_hydraulic_length:.6f} m "
        f"({pct_delta(result.arm2_hydraulic_length, donor.arm2_hydraulic_length):+.3f}% vs donor)"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pose",
        nargs=4,
        type=float,
        metavar=("ARM1", "ARM2", "ARM3", "ARM4"),
        help="evaluate one custom angle set instead of the named comparison table",
    )
    parser.add_argument(
        "--arm4-translation",
        nargs=3,
        type=float,
        metavar=("X", "Y", "Z"),
        default=DONOR_ARM4_TRANSLATION,
        help="override the donor loading Arm-4 translation",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    arm4_translation = tuple(args.arm4_translation)

    if args.pose is not None:
        rows = [("custom", evaluate(args.pose, arm4_translation))]
    else:
        rows = [(name, evaluate(pose)) for name, pose in named_poses().items()]

    if args.json:
        print(json.dumps([result_dict(name, result) for name, result in rows], indent=2))
    else:
        for index, (name, result) in enumerate(rows):
            if index:
                print()
            print_result(name, result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
