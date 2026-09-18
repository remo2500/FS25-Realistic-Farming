# FS25 Realistic Farming Roadmap

_Last updated: 2026-09-16_

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

#### Historical foundation

Completed through V6:

- Four front-to-back logical tanks established at 9,691 / 1,938 / 4,228 / 17,618 L.
- Verified physical opening map documented.
- Four load/unload positions and exact-fill roots established.
- Tank 4 represented as one logical unit across 410-bu main + 90-bu FLEX physical regions.
- Separate physical fill-volume envelopes established with high-confidence static geometry.
- V6 compatibility bridge and initial validator created.

V6 remains **HOLD** because Tank 3 belongs to `tankFlapsBack` while V6 leaves that group closed at selector stop 0.400. V6 also retains an over-broad compatibility matcher and a superseded Tank 1 reach strategy.

#### V7 static engineering — COMPLETE for first runtime cycle

Completed:

1. Captured donor-safe engineering reference from the user-supplied Hispano V3 archive.
2. Recovered the actual four-arm conveyor hierarchy and donor loading transforms.
3. Built a forward-kinematics model and independently reproduced V6 Tank 1 Z +1.650 m within about 1.5 mm.
4. Proved that no pose confined to the observed donor animation ranges can reach the new front Tank 1 opening.
5. Calculated a distributed Tank 1 reach solution targeting Z +1.900 m with lower modeled Arm-1/Arm-2 hydraulic penalty than V6.
6. Corrected flap authority: Tanks 1-2 front group; Tanks 3-4 rear group.
7. Implemented the 2-4 s front-to-rear flap transition so Tank 3 has rear open/front closed at 0.400.
8. Hardened compatibility to normal `seeds fertilizer` category authority plus the narrower crop-specific `SEED` suffix fallback.
9. Removed V6's arbitrary supported-product union behavior.
10. Expanded the V7 validator to sample actual flap animation states and reconstruct Tank 1 pipe kinematics.
11. Added a donor-SHA-guarded deterministic rebuild tool: `tools/build_bourgault_v7_from_v3.py`.
12. Generated the reproducible V7 engineering candidate:
    - `FS25_Bourgault_3320_4Tank_V7_Engineering.zip`
    - SHA-256 `190b358ed1f21b411a11eb2d4cd0fc1d59f6f6cd293f93f9e7e239b307a17e2d`
    - 61 ZIP entries
13. Completed a donor-aware static engineering audit: **30/30 PASS**.
14. Verified V7 introduces no new I3D `nodeId` collisions beyond the donor's existing TransformGroup/UserAttribute pairings.
15. Verified two independent rebuilds produce byte-identical V7 ZIPs.

#### Next — V7 runtime validation

When testing is available:

1. Install only the V7 development copy; disable older Bourgault variants.
2. Buy a fresh cart and review `log.txt` immediately.
3. Verify fresh-purchase transport/stow state.
4. Cycle Tank 1 -> Tank 2 -> Tank 3 -> Tank 4 -> transport.
5. Capture overhead and side views of every selector state.
6. Verify the intended flap group at every stop, especially Tank 3 rear-open/front-closed.
7. Inspect Tank 1's distributed reach pose for Arm-3 linkage, hose stretch, collision, lid clearance, downspout insertion, and visual plausibility.
8. Verify each exact-fill trigger fills only its selected compartment.
9. Test crop-specific Realistic Seeder seed acceptance in all four tanks.
10. Test normal and expected custom dry fertilizers in all four tanks.
11. Inspect heap separation and Tank 4 main/FLEX presentation.
12. Verify attached drill consumption from all compartments.
13. Save/reload with different products in all four tanks.
14. Multiplayer test if required.
15. Promote only after all Must Fix runtime items pass.

If Tank 1's Z +1.900 m position lacks sufficient trigger or visual margin, evaluate the precomputed distributed center solution at Z +2.121 m before revisiting the older V6-style two-joint strategy.

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
- Bourgault V3 donor-safe reference snapshot added.
- Bourgault forward-kinematics and animation-inspection tools added.
- Deterministic, source-guarded V7 rebuild tool added.
- Reproducible V7 candidate generated and statically audited.

Remaining:

1. Record runtime test logs and known-good game/mod versions after the next user test cycle.
2. Add release notes for approved project components.
3. Keep `CURRENT_AUTHORITY.md` as the single project-wide status source.
4. Merge/promote the V7 static-hardening branch only after runtime evidence supports promotion.
