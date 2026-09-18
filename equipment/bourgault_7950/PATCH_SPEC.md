# Bourgault 3320 / 7950B Four-Tank Patch Specification

_Current engineering target: V7_

V7 supersedes V6 as the next candidate target because the V6 lid/flap animation leaves the physical Tank 3 hatch closed at the Tank 3 selector stop. V6 remains retained as a historical test artifact and must not be silently overwritten.

This file documents the project-authored changes required to convert the donor 7950B cart from its original two logical product groups into four front-to-back logical compartments while preserving donor assets.

## Donor files modified

The intended V7 donor modifications are limited to:

- `modDesc.xml`
- `xml/Series_7950B.xml`
- `i3d/Series_7950B.i3d`

Project-authored file added:

- donor path: `scripts/FourTankCompat.lua`
- repository source: `scripts/compatibility/Bourgault7950FourTankCompat.lua`

The donor `.i3d.shapes`, textures, sounds, wheels, hoses, and 3320 drill files are not intentionally changed.

## Logical tank authority

Custom numbering is front-to-back.

| Tank | Factory region | Capacity | Opening reference |
|---|---|---:|---:|
| 1 | Factory Tank 4 | 9,691 L | A, center Z +2.121 m |
| 2 | Factory Tank 3 | 1,938 L | B, center Z +0.721 m |
| 3 | Factory Tank 2 | 4,228 L | C, center Z -0.678 m |
| 4 | Factory Tank 1A + FLEX | 17,618 L | D/E main + F FLEX |

Total: **33,475 L**.

## Physical opening spans

Geometry audit of the untouched lid/opening meshes established the following longitudinal opening spans:

| Opening | Approximate Z span | Lid group |
|---|---|---|
| A | +1.590 to +2.652 m | `tankFlapsFront` |
| B | +0.190 to +1.252 m | `tankFlapsFront` |
| C | -1.209 to -0.147 m | `tankFlapsBack` |
| D/E/F | rear main + FLEX region | `tankFlapsBack` |

The critical correction from V6 is that `tankFlapsFront` covers **Tanks 1-2 only**. Tank 3 belongs to the rear flap assembly.

## Fill units

`xml/Series_7950B.xml` must define four fill units in this exact order:

1. `capacity="9691"`, `fillTypeCategories="seeds fertilizer"`, exact root `exactFillRootNodeTank1`
2. `capacity="1938"`, `fillTypeCategories="seeds fertilizer"`, exact root `exactFillRootNodeTank2`
3. `capacity="4228"`, `fillTypeCategories="seeds fertilizer"`, exact root `exactFillRootNodeTank3`
4. `capacity="17618"`, `fillTypeCategories="seeds fertilizer"`, exact root `exactFillRootNodeTank4`

Do not revert to literal `fillTypes="seeds fertilizer"` unless a confirmed runtime conflict requires it.

## Physical fill-volume mapping

Retain the V6 five-envelope architecture unless runtime evidence shows a direct problem:

- `fillVolumeTank1` -> fill unit 1
- `fillVolumeTank2` -> fill unit 2
- `fillVolumeTank3` -> fill unit 3
- `fillVolumeTank4` -> fill unit 4, factor 0.82, `useFullCapacity="false"`
- `fillVolumeTank4Flex` -> fill unit 4, factor 0.18, `useFullCapacity="false"`

Current transforms:

| Node | Translation | Scale |
|---|---|---|
| fillVolumeTank1 | `0.028885 2.65800 2.121000` | `1.50 1.44 1.28` |
| fillVolumeTank2 | `0.028885 2.65800 0.721000` | `1.50 1.44 1.28` |
| fillVolumeTank3 | `0.028885 2.65800 -0.678000` | `1.50 1.44 1.20` |
| fillVolumeTank4 | `0.028885 2.65800 -2.129500` | `1.15 1.44 1.38` |
| fillVolumeTank4Flex | `0.028885 2.65800 -3.606000` | `1.15 1.44 1.45` |

Decoded mesh extents are approximately:

- Tank 1: +1.481 to +2.761 m
- Tank 2: +0.081 to +1.361 m
- Tank 3: -1.278 to -0.078 m
- Tank 4 main: -2.820 to -1.440 m
- Tank 4 FLEX: -4.331 to -2.881 m

Logical segmentation is accepted. Exact generated heap appearance remains a runtime visual test item.

## Load/unload info nodes

The donor two-group load/unload architecture is replaced with four front-to-back positions:

| Tank | Z |
|---|---:|
| 1 | +2.121 m |
| 2 | +0.721 m |
| 3 | -0.678 m |
| 4 | -1.792 m |

Each tank has both a `loadInfoTankN` and `unloadInfoTankN` node.

## Exact fill roots

Four receiving roots must exist and be mapped:

- `exactFillRootNodeTank1`
- `exactFillRootNodeTank2`
- `exactFillRootNodeTank3`
- `exactFillRootNodeTank4`

All are normally parked vertically out of range and the `loadingPipe` animation activates only the selected root near the appropriate selector stop.

## Manufacturer conveyor-motion authority

Bourgault 7000-series operating documentation defines three separate operator-facing conveyor positioning functions:

- **Inner Arm Swing** — In / Out
- **Outer Arm Swing** — In / Out
- **Conveyor Height** — Up / Down

The manufacturer procedure for changing tank openings is to raise the spout clear with Conveyor Height, use Inner and Outer Arm Swing to move over the desired opening, then lower the spout into the opening.

The recovered FS25 7950 reference confirms that the actual game hierarchy contains a nested four-arm mechanism:

- `overloadingArm01`
- `overloadingArm02`
- `overloadingArm03`
- `overloadingArm04`

Recovered donor loading pose:

- Arm 1 = +100 degrees Y
- Arm 2 = -50 degrees Y
- Arm 3 = -135 degrees Y
- Arm 4 = +21 degrees X
- Arm 4 translation = `0 0.28 -0.074`

The Bourgault Model 7950 product authority confirms that the 7950 was available with a load/unload conveyor using a 10-inch tube and 15-inch belt. Bourgault support also lists model-specific instruction `0252-41-01`, **Downspout Installation - 7950 A/C with a Conveyor**. The contents/dimensions of that EzParts document have not yet been recovered, so do not infer unpublished dimensions from its title.

Detailed Tank 1 authorities:

- `equipment/bourgault_7950/TANK1_CONVEYOR_ENGINEERING.md`
- `equipment/bourgault_7950/V7_KINEMATIC_SOLVE.md`

Reproducible forward model:

`tools/bourgault7950_forward_kinematics.py`

## Conveyor selector states

`coverConfiguration` selector stops:

| Tank | Normalized stop | 10-second animation time |
|---|---:|---:|
| 1 | 0.000 | 0 s |
| 2 | 0.200 | 2 s |
| 3 | 0.400 | 4 s |
| 4 | 0.600 | 6 s |
| Closed/transport | 1.000 | 10 s |

The last cover state must explicitly define:

- `closeAnimation="loadingPipe"`
- `closeAnimationStopTime="1.000"`

## Required V7 lid/flap timing

V6 is wrong at Tank 3 because the rear flap group is still closed at 4 s.

The recovered V3 animation confirms that the physical flap transforms use approximately **-100 degrees Z for open** and **0 degrees Z for closed**. V7 must implement the two-group sequence below:

- `tankFlapsFront`
  - open (`0 0 -100`) for Tanks 1 and 2;
  - remain open through the Tank 2 stop at 2 s;
  - close during the 2-4 s transition;
  - be fully closed (`0 0 0`) at the Tank 3 stop and thereafter.
- `tankFlapsBack`
  - remain closed (`0 0 0`) through the Tank 2 stop at 2 s;
  - open during the 2-4 s transition;
  - be fully open (`0 0 -100`) at the Tank 3 stop at 4 s;
  - remain open through Tank 4 at 6 s;
  - close during the transport/stow portion of the animation.

Static acceptance invariant: at selector stop 0.400, `tankFlapsBack` must be fully open and `tankFlapsFront` must be fully closed.

## Current discharge positions

These are discharge positions, not necessarily opening centers:

| Tank | Current/historical discharge Z | Physical containment | Status |
|---|---:|---|---|
| 1 | V6 +1.650 m | inside A by only ~0.06 m at rear edge | HOLD: insufficient margin / concentrated overtravel |
| 2 | +0.493 m | inside B | donor-range pose |
| 3 | -0.769 m | inside C | donor-range pose |
| 4 | -1.792 m | centered on D | donor-range pose |

The forward-kinematics reconstruction independently reproduces the V6 Tank 1 result. Using Arm 1 = 107.99 degrees and Arm 2 = -65.60 degrees with the recovered downstream donor pose produces pipe-effect Z **+1.651514 m**, within about 1.5 mm of the historical +1.650 m audit value.

This validates the recovered hierarchy/rotation convention strongly enough to use it for V7 static engineering.

## Tank 1 V7 kinematic recommendation

Opening A:

- rear edge Z +1.590 m
- center Z +2.121 m
- front edge Z +2.652 m

The project provisional acceptance band remains **Z +1.790 to +2.452 m** (0.20 m inside either edge). Numerical search of the actual recovered V3 articulation ranges proves that a donor-range-only solution cannot reach opening A at all; some controlled overtravel is unavoidable unless the physical conveyor geometry itself is remodeled.

### Recommended first V7 stop — Z +1.900 m

Use this as the first engineering candidate, pending visual/runtime review:

- Arm 1 = **+105.164095 degrees**
- Arm 2 = **-59.356622 degrees**
- Arm 3 = **-145.314298 degrees**
- Arm 4 = **+21 degrees**
- Arm 4 translation = **`0 0.28 -0.074`**

Forward-model result:

- X = approximately `0.000000 m`
- Y = approximately `+4.026976 m`
- Z = approximately `+1.900000 m`

Opening-A margins:

- rear-edge margin = **0.310 m**
- front-edge margin = **0.752 m**
- offset from center = **-0.221 m**

Modeled cylinder-length change versus the original loading pose:

- Arm 1 hydraulic: **+1.722%**
- Arm 2 hydraulic: **+4.432%**

Relative to V6, this reduces excess hydraulic extension by approximately 34.4% on Arm 1 and 40.6% on Arm 2 while gaining substantially more opening margin.

### Secondary option — opening center Z +2.121 m

If runtime filling/visual alignment shows that +1.900 m is not sufficient, use the distributed center solution rather than returning to V6-style two-joint overtravel:

- Arm 1 = **+106.584529 degrees**
- Arm 2 = **-60.997442 degrees**
- Arm 3 = **-146.992740 degrees**
- Arm 4 = **+21 degrees**

This reaches X approximately 0 / Y +4.026976 / Z +2.121000 m, with modeled Arm-1/Arm-2 cylinder increases of approximately +2.180% / +5.224% versus donor loading pose.

### Rejected primary approach — Arm-3-only reach

Keeping Arms 1-2 at exactly 100 / -50 degrees would require Arm 3 around:

- -153.730 degrees to reach Z +1.790 m
- -155.356 degrees to reach Z +1.900 m
- -158.663 degrees to reach Z +2.121 m

That concentrates 18.7-23.7 degrees of overtravel into one downstream joint. It remains a useful sensitivity reference but is not the preferred V7 candidate without visual collision/linkage proof.

Do not move the Tank 1 opening, fill volume, or exact-fill root simply to accommodate a poorly positioned spout.

## Tank 2 / Tank 3 donor-state confirmation

The recovered forward model explains why the later V6 positions were strong:

- donor loading state `100 / -50 / -135 / 21` gives pipe Z approximately **+0.491 m**, effectively the V6 Tank 2 target +0.493 m;
- donor state `90 / -33 / -135 / 21` gives pipe Z approximately **-0.775 m**, effectively the V6 Tank 3 target -0.769 m.

Tanks 2 and 3 should therefore stay very close to these donor-derived states while Tank 1 receives the special distributed forward-reach pose.

## Cart-level sprayer representative

Use:

```xml
<sprayer fillUnitIndex="1" unloadInfoIndex="1">
```

This is only the cart specialization's representative unit. Attached sowing/sprayer tools use their own fill-source search across compatible attached fill units.

## Realistic Seeder / custom-input compatibility

V7 changes the compatibility policy from V6.

`FourTankCompat.lua` should:

1. Add all fill types registered in the normal `seeds fertilizer` categories.
2. Add standalone crop-specific seed products whose registered names end in `SEED`, excluding generic `SEEDS`, as a compatibility fallback.
3. Mirror only that approved set to Tanks 1-4.
4. Raise `VehicleStateChange.FILLTYPE_CHANGE` when additions occur so attached tool source caches rebuild.

V7 must **not** form the desired set by taking the unrestricted union of all products already supported by any one tank. That V6 behavior can propagate unrelated products across every compartment.

The suffix matcher is still a temporary heuristic. An explicit Realistic Seeder product mapping remains the preferred release solution when reliable registration data is available.

## Required static validation

Target command once a V7 archive exists:

```bash
python tools/validate_candidate.py FS25_Bourgault_3320_4Tank_V7_Engineering.zip --profile bourgault7950-v7
```

The V7 profile must reject:

- broad `SEED` substring matching;
- unrestricted union of existing tank-supported products;
- wrong selector stops;
- missing exact-fill/load/unload nodes;
- discharge targets outside the audited physical opening spans;
- Tank 3 rear-flap timing that leaves `tankFlapsBack` closed at 0.400.

The validator must not claim that node presence alone proves acceptable Tank 1 linkage/hose geometry. The forward-model values may be checked statically, but visual/runtime promotion remains mandatory.

## Runtime promotion blockers

Before V7 can be promoted:

- Confirm Tank 1 Arm-3 joint/linkage/hose behavior at the recommended +1.900 m pose.
- Confirm Tank 1 fill-trigger reliability and visible spout alignment.
- Confirm the corrected Tank 3 rear flap is visibly open.
- Confirm each selector stop fills only its intended tank.
- Confirm all four tanks accept a known Realistic Seeder crop-specific seed.
- Confirm fertilizer products expected from the installed fertilizer stack remain available.
- Confirm product heaps remain inside intended physical compartments.
- Confirm attached drill consumption from every compartment.
- Confirm save/reload.
- Confirm multiplayer if multiplayer support is required.
