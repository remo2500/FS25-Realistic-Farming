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

## Current air-cart candidates

### Bourgault 3320 / 7950B

**V7 Engineering is TEST READY / runtime validation pending. V6 remains HOLD.**

Current V7 candidate:

`FS25_Bourgault_3320_4Tank_V7_Engineering.zip`

SHA-256:

`190b358ed1f21b411a11eb2d4cd0fc1d59f6f6cd293f93f9e7e239b307a17e2d`

Static status: **30/30 donor-aware engineering checks PASS**.

V7 architecture:

- Four independent logical compartments, numbered **1 through 4 front-to-back**.
- 9,691 / 1,938 / 4,228 / 17,618 L; total 33,475 L.
- Each compartment can hold seed or fertilizer.
- Physical conveyor position selects the compartment being filled.
- Rear 410 bu + 90 bu FLEX region remains one logical Tank 4 with an 82/18 visual fill-volume split.
- Tanks 1-2 use the front flap group; Tanks 3-4 use the rear flap group.
- Tank 3's 0.400 selector state now statically evaluates with rear flap open and front flap closed.
- Exact-fill-root activation is exclusive at the four selector stops.
- Tank 1 uses a donor-validated distributed special-reach pose targeting approximately Z +1.900 m, replacing V6's more concentrated two-joint overtravel.
- Realistic Seeder/custom seed compatibility uses category authority plus a narrowed crop-seed fallback rather than propagating arbitrary products from one tank to all tanks.

V7 is rebuilt locally from the verified user-supplied V3 donor using `tools/build_bourgault_v7_from_v3.py`. The donor archive/model assets are not redistributed in this public repository.

See [`docs/CURRENT_AUTHORITY.md`](docs/CURRENT_AUTHORITY.md) for the full geometry, kinematic solve, statuses, and promotion blockers.

### Seed Hawk 660

Active test candidate: **3-Tank RS V3R1 Recovery — TEST READY / runtime validation pending**.

Architecture:

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

Bourgault engineering/rebuild assets:

- [`equipment/bourgault_7950/PATCH_SPEC.md`](equipment/bourgault_7950/PATCH_SPEC.md)
- [`equipment/bourgault_7950/V7_KINEMATIC_SOLVE.md`](equipment/bourgault_7950/V7_KINEMATIC_SOLVE.md)
- [`equipment/bourgault_7950/reference/`](equipment/bourgault_7950/reference/)
- [`tools/build_bourgault_v7_from_v3.py`](tools/build_bourgault_v7_from_v3.py)
- [`tools/bourgault7950_forward_kinematics.py`](tools/bourgault7950_forward_kinematics.py)
- [`tools/extract_i3d_animation.py`](tools/extract_i3d_animation.py)

Other rebuild/validation authority:

- [`equipment/seedhawk_660/PATCH_SPEC.md`](equipment/seedhawk_660/PATCH_SPEC.md)
- [`patches/README.md`](patches/README.md)
- [`tools/validate_candidate.py`](tools/validate_candidate.py)
- [`builds/CANDIDATE_CHECKSUMS.md`](builds/CANDIDATE_CHECKSUMS.md)

## Repository policy

This repository is intended to contain project-authored code, patches, configuration, documentation, test reports, coordinate data, compatibility logic, and donor-safe derived engineering references.

Third-party mods should **not** be redistributed here unless their license explicitly permits redistribution. Donor ZIPs and other third-party assets remain outside the public repository unless licensing has been reviewed.

## Project documents

- [`docs/CURRENT_AUTHORITY.md`](docs/CURRENT_AUTHORITY.md) — governing project status and locked decisions.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — ordered development plan.
- [`docs/COMPATIBILITY_MATRIX.md`](docs/COMPATIBILITY_MATRIX.md) — mod/system compatibility status.
- [`docs/TESTING.md`](docs/TESTING.md) — required runtime test procedure.

## Development rule

Do not reopen a system marked **LOCKED** in `CURRENT_AUTHORITY.md` unless a direct runtime conflict is found. Report the conflict first, then revise the authority deliberately rather than silently changing a previously validated design.
