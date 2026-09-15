# Seed Hawk 660 Three-Tank Patch Specification

_Current authority target: 3-Tank RS V3_

This file documents the project-authored changes used to make the Seed Hawk 660 cart expose all three donor compartments consistently to normal seed/fertilizer products and Realistic Seeder crop-specific seed products.

## Donor files modified

Current V3 intentionally modifies:

- `modDesc.xml`
- `seedHawk660AirCart.xml`
- `seedHawk660AirCart.i3d`

Project-authored file added:

- donor path: `scripts/ThreeTankCompat.lua`
- repository source: `scripts/compatibility/SeedHawk660ThreeTankCompat.lua`

Other drill/cart assets remain donor files and should not be redistributed through this repository unless licensing is explicitly reviewed.

## Logical tank authority

Retain the donor's three physical compartments:

| Tank | Capacity | Exact fill root |
|---|---:|---|
| 1 | 5,600 L | `exactFillRootNodeSeeds` |
| 2 | 5,600 L | `exactFillRootNodeSeedsMiddle` |
| 3 | 10,600 L | `exactFillRootNodeFertilizer` |

Total: **21,800 L**.

## Fill units

All three units use:

```xml
fillTypeCategories="seeds fertilizer"
```

Do not leave Tanks 1/2 on literal donor seed lists while Tank 3 uses a different product architecture. The purpose of the conversion is that all three physical compartments are valid flexible storage compartments for project-supported seed/fertilizer products.

## Physical fill volumes

Retain the donor's three independent physical fill-volume meshes:

- `fillSeed` -> fill unit 1
- `fillSeedMiddle` -> fill unit 2
- `fillFert` -> fill unit 3

The Seed Hawk does not require the Bourgault-style reconstruction of combined fill-volume geometry.

## Conveyor selector states

For the conveyor configuration:

| Tank | Normalized stop |
|---|---:|
| 1 | 0.000 |
| 2 | 0.234 |
| 3 | 0.534 |
| Closed/transport | 1.000 |

The third selector state explicitly closes `loadingPipe` to 1.0 so the donor transport endpoint remains authoritative.

Tank 2 uses the added middle exact-fill root rather than sharing Tank 1 or Tank 3's receiving root.

## Cart-level sprayer element

V3 cleanup authority:

```xml
<sprayer fillUnitIndex="3" unloadInfoIndex="3">
```

The unsupported `loadInfoIndex` attribute present in V2 is removed. FS25's Sprayer specialization does not define that attribute on the cart-level `sprayer` element.

## Realistic Seeder compatibility

`ThreeTankCompat.lua`:

1. Merges fill types already registered on any of Tanks 1-3.
2. Adds the standard/mod-extended `seeds fertilizer` category contents.
3. Adds custom fill types whose internal names end in `SEED`, excluding the generic `SEEDS` name.
4. Mirrors the resulting set across all three compartments.
5. Raises `VehicleStateChange.FILLTYPE_CHANGE` when the supported set changes so attached sowing/sprayer tools rebuild their fill-source caches.

V3 deliberately tightens the V2 fallback from broad substring matching to a suffix check. A future explicit Realistic Seeder allowlist may supersede this once the actual runtime registration set is captured.

## Mechanical authority

Unlike the Bourgault 7950 front tank, Seed Hawk V3 does not intentionally push the donor conveyor beyond its original articulation envelope. The donor mechanical animation and the three physical receiving positions remain the baseline.

## Required static validation

Run:

```bash
python tools/validate_candidate.py FS25_SeedHawkPack_3Tank_RS_V3.zip --profile seedhawk660-v3
```

Current expected result: **16/16 checks PASS**.

## Runtime promotion blockers

Before V3 can be promoted:

- Load the same known Realistic Seeder crop-specific seed into Tanks 1, 2, and 3 independently.
- Confirm the conveyor selects the intended compartment at all three stops.
- Confirm only the selected exact-fill root accepts product.
- Confirm attached drill consumption from all three compartments.
- Confirm normal seed and fertilizer behavior remains intact.
- Save/reload with different products in each tank.
- Confirm multiplayer if multiplayer support is required.
