# FS25 Realistic Farming

A coordination and development repository for Farming Simulator 25 realism integrations focused on realistic seed handling, multi-compartment air carts, crop-specific seed products, packaging, and future Precision Farming-compatible crop input systems.

## Project goals

The project currently focuses on:

- Realistic multi-compartment Bourgault and Seed Hawk air carts.
- Physical conveyor-selected filling of individual compartments.
- Compatibility with crop-specific seed products from Realistic Seeder.
- ProBox, pallet, and big-bag integration for realistic crop-specific seed handling.
- Support for the crop set used by SW Manitoba 4x where realistic seed packaging makes sense.
- Future fertilizer/input integration while keeping Precision Farming as the soil/agronomy authority.

## Current active work

### Bourgault 3320 / 7950B

Active test candidate: **V6 Engineering**.

Target architecture:

- Four independent logical compartments, numbered **1 through 4 front-to-back**.
- Each compartment can hold seed or fertilizer.
- Physical conveyor position selects the compartment being filled.
- Total modeled capacity remains 33,475 L.
- Rear 410 bu + 90 bu FLEX region remains one logical Tank 4 for now.
- Realistic Seeder crop-specific fill types are synchronized across all four compartments.

See [`docs/CURRENT_AUTHORITY.md`](docs/CURRENT_AUTHORITY.md) for current geometry, capacities, known risks, and locked decisions.

### Seed Hawk 660

Active test candidate: **3-Tank RS V2**.

Target architecture:

- Three independent donor compartments retained.
- 5,600 L / 5,600 L / 10,600 L.
- Physical conveyor selection retained.
- All three tanks support the same seed/fertilizer category logic.
- Realistic Seeder crop-specific seed types are synchronized across all three tanks.

A small V3 cleanup is still planned before finalization.

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
