# FS25 Realistic Farming Roadmap

_Last updated: 2026-09-15_

This roadmap defines the recommended order of work. Changes should be reflected in `CURRENT_AUTHORITY.md` when they alter locked architecture.

## Phase 1 — Stabilize current air carts

### 1. Seed Hawk 660

1. Remove unsupported `loadInfoIndex` from the cart-level sprayer element.
2. Harden the Realistic Seeder fill-type matcher.
3. Runtime-test crop-specific seed acceptance in Tanks 1, 2, and 3.
4. Test drill consumption from each tank independently.
5. Save/reload test with different products in all three compartments.
6. Promote to approved baseline if no regressions are found.

### 2. Bourgault 7950B

1. Runtime-test V6 fresh-purchase stow state.
2. Verify conveyor positions for Tanks 1-4 from overhead and side views.
3. Specifically evaluate Tank 1 mechanical overtravel, linkage, hose, and trigger tolerance.
4. Test crop-specific Realistic Seeder seed acceptance in all four tanks.
5. Fill all four logical tanks with distinguishable products and inspect heap separation.
6. Verify attached drill can consume from every compartment.
7. Save/reload and multiplayer test.
8. If Tank 1 remains mechanically implausible, redesign forward reach using secondary conveyor articulation rather than additional primary-arm overtravel.
9. Promote only after Tank 1 and heap geometry pass.

## Phase 2 — Shared compatibility architecture

1. Consolidate Seed Hawk and Bourgault compatibility logic into a reusable project-owned Realistic Seeder compatibility module where practical.
2. Replace broad `SEED` substring matching with an explicit or proven Realistic Seeder product mapping.
3. Identify a reliable post-mod-registration lifecycle event and reduce/remove recurring polling.
4. Document all discovered crop-specific fill type names and associated crop/seed package data.
5. Validate multiplayer synchronization behavior.

## Phase 3 — Additional Bourgault carts

### Bourgault 71300

Target architecture:

- Four independent main compartments.
- Conveyor-selected physical filling.
- Seed/fertilizer flexibility per main compartment.
- FLEX-bin behavior remains out of scope unless a later requirement justifies it.

Tasks:

1. Audit donor tank geometry and capacities.
2. Identify exact physical loading openings and conveyor animation positions.
3. Build independent fill units without changing donor total capacity.
4. Integrate the shared Realistic Seeder compatibility layer.
5. Runtime-test against the same validation protocol used for the 7950B.

## Phase 4 — Realistic seed packaging

1. Audit Realistic Seeder registered crop-specific seed products.
2. Define packaging classes:
   - small bag where appropriate,
   - big bag/tote,
   - ProBox-style rigid bulk seed container.
3. Build compatibility mappings for SW Manitoba 4x crop set.
4. Preserve realistic crop-specific naming, mass, price, and capacity relationships.
5. Ensure packaging unloads into supported cart compartments without converting back to generic seeds.

## Phase 5 — Input-system realism

1. Evaluate realistic fertilizer product separation without conflicting with Precision Farming.
2. Define nitrogen-source products only where gameplay value justifies them.
3. Explore crop-input purchase/accounting integration with AgForward Financial Co-operative systems if appropriate.
4. Avoid duplicating Precision Farming's soil-state simulation.

## Phase 6 — Documentation and release discipline

1. Maintain a compatibility matrix for every supported mod version.
2. Record test logs and known-good game/mod versions.
3. Add patch/diff instructions so public repository content does not require redistributing third-party donor assets.
4. Add release notes for approved project components.
5. Keep `CURRENT_AUTHORITY.md` as the single project-wide status source.
