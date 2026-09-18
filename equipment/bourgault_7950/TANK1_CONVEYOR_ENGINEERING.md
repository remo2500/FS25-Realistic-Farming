# Bourgault 7950B Tank 1 Conveyor Engineering

_Status: donor-derived static solve implemented in V7 Engineering candidate; runtime visual/trigger proof pending_

This note records the Tank 1 conveyor problem, verified donor geometry, rejected approaches, and the current V7 solution. The detailed numerical solve is in `V7_KINEMATIC_SOLVE.md`.

## 1. Problem statement

The historical V6 Tank 1 discharge point was approximately **Z +1.650 m**.

Physical Tank 1 opening A spans approximately:

- rear edge: **Z +1.590 m**
- center: **Z +2.121 m**
- front edge: **Z +2.652 m**

V6 was therefore only about **0.060 m** inside the rear edge. Its first two primary conveyor arms were approximately:

- Arm 1: **107.99 degrees**
- Arm 2: **-65.60 degrees**

That pose is retained only as a historical comparison.

## 2. Recovered 7950 donor authority

The user-supplied V3 archive provided the actual 7950 hierarchy and loading state.

Verified donor loading pose:

- Arm 1: **+100 degrees Y**
- Arm 2: **-50 degrees Y**
- Arm 3: **-135 degrees Y**
- Arm 4: **+21 degrees X**
- Arm 4 translation: **`0 0.28 -0.074`**

The conveyor is a nested four-arm chain:

1. `overloadingArm01`
2. `overloadingArm02`
3. `overloadingArm03`
4. `overloadingArm04`

Recovered pivot translations:

- Arm 1: `-1.47003 1.56863 -1.22386`
- Arm 2: `-0.173656 0.727869 -3.68031`
- Arm 3: `-0.241337 0.219075 1.66861`

Recovered pipe-effect local translation:

`-0.00384 -0.258395 -4.10928`

The donor-safe reference is stored under:

`equipment/bourgault_7950/reference/`

## 3. Manufacturer mechanical context

Bourgault 7000-series operating documentation describes three operator-facing conveyor positioning functions:

1. Inner Arm Swing — In / Out.
2. Outer Arm Swing — In / Out.
3. Conveyor Height — Up / Down.

The tank-change procedure raises the conveyor/spout clear, uses the swing functions to position it, then lowers the spout into the opening. This is consistent with the recovered multi-joint game hierarchy and supports distributing additional reach rather than forcing only the first two joints.

Bourgault's Model 7950 material confirms a load/unload conveyor option. Bourgault support also lists model-specific instruction `0252-41-01`, **Downspout Installation - 7950 A/C with a Conveyor**. No unpublished dimensions from that document are assumed because the document contents have not been recovered.

## 4. Forward-model validation

The donor-safe forward model is:

`tools/bourgault7950_forward_kinematics.py`

Using the recovered hierarchy and the historical V6 values:

- Arm 1 = 107.99 degrees
- Arm 2 = -65.60 degrees
- Arm 3 = -135 degrees
- Arm 4 = +21 degrees

produces pipe-effect Z **+1.651514 m**.

That differs from the earlier V6 geometry audit (+1.650 m) by only about **1.5 mm**. This independently validates the transform convention used for the V7 solve.

## 5. Feasibility result

Numerical search across the full articulation ranges actually observed in the V3 animation found **no donor-range-only solution capable of reaching opening A**.

Therefore, unless the physical conveyor geometry itself is remodeled, some controlled articulation outside the original V3 animation envelope is unavoidable for the new front Tank 1.

The engineering decision is where to distribute that unavoidable extra reach with the least mechanical and visual penalty.

## 6. Rejected primary approaches

### Historical V6 two-joint approach

V6 concentrated the extra reach mainly in Arms 1 and 2. It produced only ~0.060 m rear-edge margin and modeled hydraulic extensions of approximately:

- Arm 1: +2.626% versus donor loading pose
- Arm 2: +7.457% versus donor loading pose

This is superseded by V7.

### Arm-3-only approach

Holding Arms 1 and 2 at exactly 100 / -50 degrees would require approximately:

- Arm 3 -153.730 degrees for Z +1.790 m
- Arm 3 -155.356 degrees for Z +1.900 m
- Arm 3 -158.663 degrees for Z +2.121 m

That concentrates too much extra articulation into one downstream joint without visual collision/linkage proof. It remains a sensitivity reference, not the current candidate.

## 7. Current V7 Tank 1 solution

**Implemented in current V7 Engineering candidate:**

- Arm 1 = **+105.164095 degrees**
- Arm 2 = **-59.356622 degrees**
- Arm 3 = **-145.314298 degrees**
- Arm 4 = **+21 degrees**
- Arm 4 translation = **`0 0.28 -0.074`**

Calculated pipe position:

- X approximately `0.000000 m`
- Y approximately `+4.026976 m`
- Z approximately **`+1.900000 m`**

Opening-A margins:

- rear edge: **0.310 m**
- front edge: **0.752 m**
- 0.221 m rearward of opening center

Modeled hydraulic change versus donor loading pose:

- Arm 1: **+1.722%**
- Arm 2: **+4.432%**

Compared with V6, the excess modeled hydraulic extension is reduced by approximately:

- Arm 1: **34.4%**
- Arm 2: **40.6%**

This is the recommended first runtime candidate because it gains meaningful opening margin without pushing all additional reach into one joint or going all the way to the opening center before testing proves that necessary.

## 8. Secondary center solution

If runtime trigger/visual evidence shows that Z +1.900 m is insufficient, the precomputed distributed center solution is:

- Arm 1 = **+106.584529 degrees**
- Arm 2 = **-60.997442 degrees**
- Arm 3 = **-146.992740 degrees**
- Arm 4 = **+21 degrees**
- target Z = **+2.121 m**

Use this before returning to a V6-style concentrated two-joint solution.

## 9. Tank 2 / Tank 3 baseline confirmation

Recovered donor states also explain why the later Tank 2 and Tank 3 targets were strong:

- `100 / -50 / -135 / 21` gives pipe Z about **+0.491 m**, effectively Tank 2.
- `90 / -33 / -135 / 21` gives pipe Z about **-0.775 m**, effectively Tank 3.

Tanks 2 and 3 should remain close to these donor-derived states. Tank 1 is the special-reach case.

## 10. Runtime gates still open

Do **not** mark Tank 1 LOCKED until in-game review confirms:

- Arm-3 joint movement is visually believable;
- hydraulic/linkage geometry behaves acceptably;
- hoses do not stretch/intersect unrealistically;
- downspout clears the lids/tank structure;
- pipe insertion depth looks plausible;
- the exact-fill trigger reliably fills Tank 1 only;
- the +1.900 m pose provides enough practical margin.

Static kinematics are high-confidence, but they do not replace the visual/runtime test.
