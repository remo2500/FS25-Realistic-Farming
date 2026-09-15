# Bourgault 3320 / 7950B Four-Tank Patch Specification

_Current authority target: V6 Engineering_

This file documents the project-authored changes required to convert the donor 7950B cart from its original two logical product groups into four front-to-back logical compartments while preserving the donor assets.

## Donor files modified

Only these donor files are intentionally modified in V6:

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

## Fill units

`xml/Series_7950B.xml` must define four fill units in this exact order:

1. `capacity="9691"`, `fillTypeCategories="seeds fertilizer"`, exact root `exactFillRootNodeTank1`
2. `capacity="1938"`, `fillTypeCategories="seeds fertilizer"`, exact root `exactFillRootNodeTank2`
3. `capacity="4228"`, `fillTypeCategories="seeds fertilizer"`, exact root `exactFillRootNodeTank3`
4. `capacity="17618"`, `fillTypeCategories="seeds fertilizer"`, exact root `exactFillRootNodeTank4`

Do not revert to literal `fillTypes="seeds fertilizer"` for these units unless a confirmed runtime conflict requires it.

## Physical fill-volume mapping

V6 uses five physical fill-volume envelopes for four logical tanks:

- `fillVolumeTank1` -> fill unit 1
- `fillVolumeTank2` -> fill unit 2
- `fillVolumeTank3` -> fill unit 3
- `fillVolumeTank4` -> fill unit 4, factor 0.82, `useFullCapacity="false"`
- `fillVolumeTank4Flex` -> fill unit 4, factor 0.18, `useFullCapacity="false"`

Current I3D transforms:

| Node | Translation | Scale |
|---|---|---|
| fillVolumeTank1 | `0.028885 2.65800 2.121000` | `1.50 1.44 1.28` |
| fillVolumeTank2 | `0.028885 2.65800 0.721000` | `1.50 1.44 1.28` |
| fillVolumeTank3 | `0.028885 2.65800 -0.678000` | `1.50 1.44 1.20` |
| fillVolumeTank4 | `0.028885 2.65800 -2.129500` | `1.15 1.44 1.38` |
| fillVolumeTank4Flex | `0.028885 2.65800 -3.606000` | `1.15 1.44 1.45` |

These envelopes are still **TESTING visually**. Do not promote their exact transforms to LOCKED until product heaps have been reviewed in game.

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

## Conveyor selector states

`coverConfiguration` selector stops:

| Tank | Normalized stop |
|---|---:|
| 1 | 0.000 |
| 2 | 0.200 |
| 3 | 0.400 |
| 4 | 0.600 |
| Closed/transport | 1.000 |

The last cover state must explicitly define:

- `closeAnimation="loadingPipe"`
- `closeAnimationStopTime="1.000"`

This is required so a fresh purchase initialized in cover state 0 is driven to the donor's fully stowed transport endpoint.

## Current V6 discharge targets

These are target discharge positions, not necessarily opening centers:

| Tank | Discharge Z | Status |
|---|---:|---|
| 1 | +1.650 m | HOLD: mechanical overtravel still needs runtime proof |
| 2 | +0.493 m | donor-range pose |
| 3 | -0.769 m | donor-range pose |
| 4 | -1.792 m | within donor articulation range |

Known Tank 1 primary-arm pose is approximately 107.99 degrees / -65.60 degrees versus donor loading-envelope values near 100 / -50 degrees. Do not mark this geometry LOCKED without runtime review.

## Lid/flap limitation

The donor model exposes only two movable flap groups (`tankFlapsFront` and `tankFlapsBack`). V6 therefore keeps the front group open for Tanks 1-3 and the rear group for Tank 4. This is a donor-geometry limitation and is not equivalent to four independently modeled hatch mechanisms.

## Cart-level sprayer representative

Current V6 uses:

```xml
<sprayer fillUnitIndex="1" unloadInfoIndex="1">
```

This is only the cart specialization's representative unit. Attached sowing/sprayer tools use their own fill-source search across compatible attached fill units.

## Realistic Seeder compatibility

`FourTankCompat.lua`:

1. Merges supported fill types already present on any of Tanks 1-4.
2. Adds fill types in the `seeds fertilizer` categories.
3. Adds crop-specific seed products discovered after XML load.
4. Mirrors the resulting set to all four compartments.
5. Raises `VehicleStateChange.FILLTYPE_CHANGE` when changes occur so attached tool source caches rebuild.

V6 still uses the broad `SEED` substring fallback. Production hardening remains planned; do not silently change the distributed V6 build without versioning the candidate.

## Required static validation

Run:

```bash
python tools/validate_candidate.py FS25_Bourgault_3320_4Tank_V6_Engineering.zip --profile bourgault7950-v6
```

Current expected result: **18/18 checks PASS**.

## Runtime promotion blockers

Before V6 can be promoted:

- Confirm Tank 1 conveyor linkage/hose behavior.
- Confirm each selector stop fills only its intended tank.
- Confirm all four tanks accept a known Realistic Seeder crop-specific seed.
- Confirm product heaps remain inside intended physical compartments.
- Confirm attached drill consumption from every compartment.
- Confirm save/reload.
- Confirm multiplayer if multiplayer support is required.
