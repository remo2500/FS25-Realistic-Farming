# FS25 Realistic Farming Roadmap

_Last updated: 2026-09-15_

This roadmap defines the recommended order of work. Changes should be reflected in `CURRENT_AUTHORITY.md` when they alter locked architecture.

## Phase 1 — Stabilize current air carts

### 1. Seed Hawk 660

Completed before runtime test:

- Removed unsupported `loadInfoIndex` from the cart-level sprayer element in V3.
- Hardened the Realistic Seeder fallback from broad substring matching to fill-type names ending in `SEED`.
- Added project-owned compatibility source and static validator coverage.
- Preserved the current V3 candidate unchanged while awaiting evidence.

Next when runtime testing is available:

1. Test crop-specific seed acceptance in Tanks 1, 2, and 3 using the same known product.
2. Test fertilizer in each compartment.
3. Test drill consumption from each tank independently.
4. Save/reload with different products in all three compartments.
5. Test the No Conveyor configuration.
6. Smoke-test major cart/drill attachment arrangements in the pack.
7. Multiplayer test if required.
8. Promote to approved baseline if no regressions are found.

### 2. Bourgault 7950B

Completed through V6:

- Four front-to-back logical tanks established at 9,691 / 1,938 / 4,228 / 17,618 L.
- Verified physical opening map documented.
- Four load/unload positions and exact-fill roots established.
- Tank 4 represented as one logical unit across 410-bu main + 90-bu FLEX physical regions.
- Separate physical fill-volume envelopes established with high-confidence static geometry.
- V6 compatibility bridge and initial validator created.

New audit result:

- V6 is **HOLD** because the Tank 3 physical opening belongs to `tankFlapsBack`, but V6 still has that flap group closed at selector stop 0.400 / 4 s.
- V6 also retains an over-broad custom-seed matcher and unrestricted product propagation.

Current work — V7 static hardening:

1. Correct flap authority: Tanks 1-2 front group; Tanks 3-4 rear group.
2. Implement transition so front closes and rear opens during 2-4 s; rear must be fully open at Tank 3.
3. Harden compatibility to category authority + crop-specific `SEED` suffix fallback.
4. Prevent arbitrary products supported by only one unit from propagating to all four tanks.
5. Expand validator coverage for V7 and retain V6 profile for historical verification.
6. Preserve the accepted fill-volume segmentation and selector/discharge coordinates unless new evidence requires change.
7. Keep Tank 1 mechanical reach as the remaining runtime engineering HOLD; if refinement is needed, seek downstream articulation before increasing primary-arm overtravel.
8. Generate a new versioned V7 candidate only from the donor/V6 engineering base; do not overwrite V6.

Next when runtime testing is available:

1. Verify V7 fresh-purchase stow state.
2. Verify correct flap group at every selector position, especially Tank 3.
3. Verify conveyor positions for Tanks 1-4 from overhead and side views.
4. Evaluate Tank 1 linkage, hose, collision, and trigger tolerance.
5. Test crop-specific Realistic Seeder seed acceptance in all four tanks.
6. Test normal and expected custom dry fertilizers in all four tanks.
7. Inspect heap separation.
8. Verify attached drill consumption.
9. Save/reload and multiplayer test.
10. Promote only after flap timing, Tank 1, and heap geometry pass.

## Phase 2 — Shared compatibility architecture

1. Capture actual installed Realistic Seeder crop-specific fill type registrations during runtime testing.
2. Replace heuristic `SEED` name matching with an explicit or proven mapping where possible.
3. Consolidate Seed Hawk and Bourgault compatibility logic only after both equipment candidates pass runtime tests.
4. Identify a reliable post-mod-registration lifecycle event and reduce/remove recurring 750 ms polling.
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
4. Integrate the shared compatibility layer after it is proven.
5. Runtime-test against the same validation protocol used for the 7950B.

## Phase 4 — Realistic seed packaging

1. Audit Realistic Seeder registered crop-specific seed products.
2. Define packaging classes: small bag where appropriate, big bag/tote, and ProBox-style rigid bulk seed container.
3. Build compatibility mappings for the intended map/crop set.
4. Preserve realistic crop-specific naming, mass, price, and capacity relationships.
5. Ensure packaging unloads into supported cart compartments without converting back to generic seeds.

## Phase 5 — Input-system realism

1. Evaluate realistic fertilizer product separation without conflicting with Precision Farming.
2. Prefer existing fertilizer category extensions from compatible input mods rather than duplicating products unnecessarily.
3. Define additional nitrogen-source products only where gameplay value justifies them.
4. Explore crop-input purchase/accounting integration with AgForward Financial Co-operative systems if appropriate.
5. Avoid duplicating Precision Farming's soil-state simulation.

## Phase 6 — Documentation and release discipline

Completed foundation:

- Compatibility matrix established.
- Current authority file established.
- Donor-safe patch/rebuild policy established.
- Per-equipment patch specifications added.
- Candidate SHA-256 records added.
- Static candidate validation tool added.
- V7 static-hardening branch established.

Remaining:

1. Produce donor-safe deterministic V7 patch/build tooling once the exact flap-animation edit is represented reliably.
2. Record runtime test logs and known-good game/mod versions after the next user test cycle.
3. Add release notes for approved project components.
4. Keep `CURRENT_AUTHORITY.md` as the single project-wide status source.
