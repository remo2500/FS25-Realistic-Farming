# FS25 Realistic Farming

A coordination and development repository for Farming Simulator 25 realism integrations focused on realistic seed handling, multi-compartment air carts, crop-specific seed products, packaging, and future Precision Farming-compatible crop input systems.

## Project goals

The project currently focuses on:

- Realistic multi-compartment Bourgault and Seed Hawk air carts.
- Physical conveyor-selected filling of individual compartments.
- Compatibility with crop-specific seed products from Realistic Seeder.
- ProBox, pallet, and big-bag integration for realistic crop-specific seed handling.
- Support for the intended map/crop set where realistic seed packaging makes sense.
- Future fertilizer/input integration while keeping Precision Farming as the soil/agronomy authority.

## Current active work

### Bourgault 3320 / 7950B

**V6 Engineering is on HOLD. V7 is the active engineering target.**

The deeper geometry audit found that V6 leaves the physical Tank 3 hatch closed at the Tank 3 selector position. V7 corrects the flap authority and hardens product compatibility before the next runtime test cycle.

Target architecture:

- Four independent logical compartments, numbered **1 through 4 front-to-back**.
- Each compartment can hold seed or fertilizer.
- Physical conveyor position selects the compartment being filled.
- Total modeled capacity remains 33,475 L.
- Rear 410 bu + 90 bu FLEX region remains one logical Tank 4 for now.
- Tanks 1-2 use the front flap group; Tanks 3-4 use the rear flap group.
- Realistic Seeder/custom seed compatibility uses category authority plus a narrowed crop-seed fallback rather than propagating arbitrary products from one tank to all tanks.
- Tank 1 forward conveyor reach remains the primary runtime engineering risk.

See [`docs/CURRENT_AUTHORITY.md`](docs/CURRENT_AUTHORITY.md) for current geometry, capacities, known risks, and locked decisions.

### Seed Hawk 660

Active test candidate: **3-Tank RS V3**.

Target architecture:

- Three independent donor compartments retained.
- 5,600 L / 5,600 L / 10,600 L.
- Physical conveyor selection retained.
- All three tanks support the same seed/fertilizer category logic.
- Realistic Seeder crop-specific seed types are synchronized across all three tanks.
- V3 removes the unsupported sprayer `loadInfoIndex` attribute and tightens the custom-seed matcher to fill-type names ending in `SEED`.
- V3 is intentionally being held unchanged until runtime evidence is available.

## Development assets

Project-owned compatibility code:

- [`scripts/compatibility/Bourgault7950FourTankCompat.lua`](scripts/compatibility/Bourgault7950FourTankCompat.lua)
- [`scripts/compatibility/SeedHawk660ThreeTankCompat.lua`](scripts/compatibility/SeedHawk660ThreeTankCompat.lua)

Rebuild/patch authority:

- [`equipment/bourgault_7950/PATCH_SPEC.md`](equipment/bourgault_7950/PATCH_SPEC.md)
- [`equipment/seedhawk_660/PATCH_SPEC.md`](equipment/seedhawk_660/PATCH_SPEC.md)
- [`patches/README.md`](patches/README.md)

Static candidate validation:

- [`tools/validate_candidate.py`](tools/validate_candidate.py)
- [`builds/CANDIDATE_CHECKSUMS.md`](builds/CANDIDATE_CHECKSUMS.md)

## Repository policy

This repository is intended to contain project-authored code, patches, configuration, documentation, test reports, coordinate data, and compatibility logic.

Third-party mods should **not** be redistributed here unless their license explicitly permits redistribution. Donor ZIPs and other third-party assets should remain outside the public repository unless licensing has been reviewed.

## Project documents

- [`docs/CURRENT_AUTHORITY.md`](docs/CURRENT_AUTHORITY.md) — governing project status and locked decisions.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — ordered development plan.
- [`docs/COMPATIBILITY_MATRIX.md`](docs/COMPATIBILITY_MATRIX.md) — mod/system compatibility status.
- [`docs/TESTING.md`](docs/TESTING.md) — required runtime test procedure.

## Development rule

Do not reopen a system marked **LOCKED** in `CURRENT_AUTHORITY.md` unless a direct runtime conflict is found. Report the conflict first, then revise the authority deliberately rather than silently changing a previously validated design.
