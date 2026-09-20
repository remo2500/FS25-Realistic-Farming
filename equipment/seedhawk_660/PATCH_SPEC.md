# Seed Hawk 660 Three-Tank Patch Specification

_Current authority target: 3-Tank RS V3R2 Seed Fix_

This file documents the project-authored changes used to make the Seed Hawk 660 cart expose all three donor compartments consistently to normal seed/fertilizer products and Realistic Seeder crop-specific seed products.

## Donor files modified

Current V3R2 Seed Fix intentionally modifies:

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

All three units use the donor-proven explicit base fill-type names:

```xml
fillTypes="seeds fertilizer"
```

**Runtime authority:** V3R1 changed these to `fillTypeCategories="seeds fertilizer"`. In FS25, `SEEDS` and `FERTILIZER` are fill-type names; a `fillTypeCategories` attribute is resolved through registered category names. The V3R1 static validator checked only the XML string and therefore missed that the cart could load with an empty supported-fill-type set. V3R2 restores direct base fill-type authority and forbids this regression.

Realistic Seeder and custom fertilizer expansion remains a Lua responsibility after the two base fill types are guaranteed.

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

V3R2 cleanup authority:

```xml
<sprayer fillUnitIndex="3" unloadInfoIndex="3">
```

The unsupported `loadInfoIndex` attribute present in V2 is removed. FS25's Sprayer specialization does not define that attribute on the cart-level `sprayer` element.

## Realistic Seeder compatibility

`ThreeTankCompat.lua` in V3R2:

1. Preserves the supported-fill-type union already present on Tanks 1-3.
2. Explicitly resolves generic `SEEDS` and `FERTILIZER` by **fill-type name**, not category name.
3. Handles both GIANTS list-style manager returns and set-style `FillUnit.supportedFillTypes` correctly.
4. Adds products in the native/mod-extended `FERTILIZER` category as a supplemental dry-fertilizer expansion.
5. Adds standalone crop-specific fill types whose internal names end in `SEED`, excluding generic `SEEDS`.
6. Mirrors the resulting set across all three compartments.
7. Raises `VehicleStateChange.FILLTYPE_CHANGE` when the set changes.

### V3R1 runtime regression and root cause

V3R1 is **HOLD / superseded for testing** after runtime evidence showed that no tank accepted generic seed.

Two static assumptions were wrong:

- the vehicle XML changed donor-proven `fillTypes="seeds fertilizer"` to `fillTypeCategories="seeds fertilizer"`;
- the old Lua helper treated GIANTS list returns from `getFillTypesByCategoryNames` as though they were already boolean sets keyed by fillType index.

GIANTS FS25 `FillUnit` loads `fillTypes` through `getFillTypesByNames`, while `fillTypeCategories` is resolved through registered category names. V3R2 therefore restores explicit XML base fill types and makes Lua expansion secondary rather than essential.

## Mechanical authority

Unlike the Bourgault 7950 front tank, Seed Hawk V3 does not intentionally push the donor conveyor beyond its original articulation envelope. The donor mechanical animation and the three physical receiving positions remain the baseline.

## Required static validation

Run:

```bash
python tools/validate_candidate.py FS25_SeedHawkPack_3Tank_RS_V3.zip --profile seedhawk660-v3
```

Historical V3 and V3R1 static passes are retained for history, but V3R1 is no longer test authority because runtime disproved its seed acceptance. V3R2 passes a **26/26 seed-fix audit** including explicit generic fill-type authority, absence of the invalid category regression, robust list/set Lua handling, physical volume mapping, No Conveyor coverage, and unchanged donor assets.

## Runtime promotion blockers

Before V3R2 can be promoted:

- Load the same known Realistic Seeder crop-specific seed into Tanks 1, 2, and 3 independently.
- Confirm the conveyor selects the intended compartment at all three stops.
- Confirm only the selected exact-fill root accepts product.
- Confirm attached drill consumption from all three compartments.
- Confirm normal seed and fertilizer behavior remains intact.
- Save/reload with different products in each tank.
- Confirm multiplayer if multiplayer support is required.


## Recovery provenance

The user-supplied recovery base is `FS25_SeedHawkPack.zip`, SHA-256:

`c248f1ec41a0c1ae5645f2fa4b61c925653ba3c5e056724a0f1be072f4460ce8`

It already contains the accepted three-compartment I3D/XML architecture. The donor-safe reference is:

`equipment/seedhawk_660/reference/RECOVERY_BASE.md`

Rebuild with:

```bash
python tools/build_seedhawk_v3r1_from_recovery_base.py FS25_SeedHawkPack.zip FS25_SeedHawkPack_3Tank_RS_V3R1_Recovery.zip
```

Current recovered candidate SHA-256:

`ffc66a36e95815dcdde54973c02db6dcf28e7d0621b29b96bbc2b3f33b968a14`

The historical V3 checksum remains separately recorded. Do not overwrite or relabel V3R1 as the historical V3 because the exact historical archive bytes are unavailable.


## V3R2 candidate

Current test candidate:

`FS25_SeedHawkPack_3Tank_RS_V3R2_SeedFix.zip`

SHA-256:

`4b0306184f18750b82828598b02ebadbee847bb158c69c627899682d47ff63bc`

Static seed-fix audit: **26/26 PASS**.

Rebuild with:

```bash
python tools/build_seedhawk_v3r2_seedfix.py FS25_SeedHawkPack.zip FS25_SeedHawkPack_3Tank_RS_V3R2_SeedFix.zip
```

Do not reuse V3R1 for testing. Its runtime seed-acceptance failure is now a documented regression.
