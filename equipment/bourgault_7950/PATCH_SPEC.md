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

Bourgault 7000-series operating documentation defines three separate conveyor positioning functions:

- **Inner Arm Swing** — In / Out
- **Outer Arm Swing** — In / Out
- **Conveyor Height** — Up / Down

The manufacturer procedure for changing tank openings is to raise the spout clear with Conveyor Height, use Inner and Outer Arm Swing to move over the desired opening, then lower the spout into the opening.

This matters directly to V7: the 7950 conveyor should be treated as a **three-function positioning mechanism**, not a two-joint mechanism whose first two joints must supply all additional Tank 1 reach.

The Bourgault Model 7950 product authority confirms that the 7950 was available with a load/unload conveyor using a 10-inch tube and 15-inch belt. Bourgault support also lists model-specific instruction `0252-41-01`, **Downspout Installation - 7950 A/C with a Conveyor**. The contents/dimensions of that EzParts document have not yet been recovered, so do not infer unpublished dimensions from its title.

Detailed Tank 1 engineering authority is maintained in:

`equipment/bourgault_7950/TANK1_CONVEYOR_ENGINEERING.md`

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

V7 must implement the two-group sequence below:

- `tankFlapsFront`
  - open for Tanks 1 and 2;
  - remain open through the Tank 2 stop at 2 s;
  - close during the 2-4 s transition;
  - be fully closed at the Tank 3 stop and thereafter.
- `tankFlapsBack`
  - remain closed through the Tank 2 stop at 2 s;
  - open during the 2-4 s transition;
  - be fully open at the Tank 3 stop at 4 s;
  - remain open through Tank 4 at 6 s;
  - close during the transport/stow portion of the animation.

Static acceptance invariant: at selector stop 0.400, `tankFlapsBack` must be fully open and `tankFlapsFront` must be fully closed.

## Current discharge positions and V7 target

These are discharge positions, not necessarily opening centers:

| Tank | Current discharge Z | Opening containment | Status |
|---|---:|---|---|
| 1 | +1.650 m | inside A by only ~0.06 m at rear edge | HOLD: insufficient margin / primary-arm overtravel |
| 2 | +0.493 m | inside B | donor-range pose |
| 3 | -0.769 m | inside C | donor-range pose |
| 4 | -1.792 m | centered on D | donor-range pose |

Tank 1 currently uses approximately 107.99 degrees / -65.60 degrees on the first two primary arms versus prior 7950 donor loading-envelope values near 100 / -50 degrees. V7 should reduce, not increase, that overtravel.

### Tank 1 preferred solve

Opening A center is **Z +2.121 m**. V7 should first attempt to place the discharge near this center while keeping the first two swing joints within the actual 7950 donor loading envelope and using the donor's Conveyor Height/downstream articulation for remaining positioning.

Preferred engineering target:

- Z **+2.121 m**
- initial center tolerance **+/-0.15 m**

Provisional minimum static acceptance band, using a project-defined 0.20 m edge margin until runtime trigger width is known:

- Z **+1.790 to +2.452 m**

This 0.20 m margin is a project engineering criterion, not a manufacturer dimension. Runtime trigger testing may justify changing it later.

Do not move the Tank 1 opening, fill volume, or exact-fill root simply to accommodate a poorly positioned spout.

Before writing new Tank 1 keyframes, recover the actual 7950 animation hierarchy and identify which nodes implement Inner Arm Swing, Outer Arm Swing, and Conveyor Height. Use:

```bash
python tools/extract_i3d_animation.py <candidate-or-donor.zip> \
  --i3d-path i3d/Series_7950B.i3d \
  --animation loadingPipe
```

Comparative Bourgault 71300 I3D evidence may be used only to guide hierarchy inspection. Its angles/translations are **not** valid 7950 limits.

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

The validator must not claim that node presence alone proves the Tank 1 kinematics or flap state. Those remain animation/engineering review gates until the actual keyframes are inspected.

## Runtime promotion blockers

Before V7 can be promoted:

- Confirm Tank 1 linkage/hose behavior and fill-trigger reliability.
- Confirm Tank 1 discharge has meaningful margin inside opening A.
- Confirm the corrected Tank 3 rear flap is visibly open.
- Confirm each selector stop fills only its intended tank.
- Confirm all four tanks accept a known Realistic Seeder crop-specific seed.
- Confirm fertilizer products expected from the installed fertilizer stack remain available.
- Confirm product heaps remain inside intended physical compartments.
- Confirm attached drill consumption from every compartment.
- Confirm save/reload.
- Confirm multiplayer if multiplayer support is required.
