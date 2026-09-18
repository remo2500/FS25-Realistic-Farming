# Compatibility Matrix

_Last updated: 2026-09-16_

This matrix tracks known compatibility status for the active FS25 Realistic Farming components.

| Component | Base functionality | Realistic Seeder | Precision Farming | Save/reload | Multiplayer | Status |
|---|---|---|---|---|---|---|
| Seed Hawk 660 3-Tank RS V3R1 Recovery | PASS structurally; 21/21 recovery checks | TESTING / high confidence | No known conflict | TESTING | Not yet tested | **TEST READY** |
| Bourgault 7950B V6 Engineering | PASS structurally except flap timing | Matcher works structurally but over-broad | No known conflict | Not promoted | Not tested | **HOLD** |
| **Bourgault 7950B V7 Engineering** | **30/30 donor-aware static checks PASS** | Hardened category + suffix fallback; runtime pending | No known conflict | Runtime pending | Not yet tested | **TEST READY** |
| Bourgault 71300 | Not started | Planned | Planned | Planned | Planned | ROADMAP |
| Shared Realistic Seeder compatibility layer | Equipment-specific prototypes | ACTIVE | N/A | TESTING | Not yet tested | ACTIVE |
| ProBox crop-specific packaging | Not started | Planned | N/A | Planned | Planned | ROADMAP |

## Seed Hawk 660 V3R1 Recovery notes

- Three donor compartments retained: 5,600 / 5,600 / 10,600 L.
- All three tanks use the same seed/fertilizer category architecture.
- V3 preserves the union of types already present on the three donor units, important because Tank 3 was previously observed accepting the crop-specific products that Tanks 1 and 2 missed.
- V3 removes the unsupported cart-level sprayer `loadInfoIndex` attribute found during the V2 audit.
- V3 tightens custom-seed fallback matching to names ending in `SEED`, excluding generic `SEEDS`.
- Historical V3 passed 16/16 project static validation checks; V3R1 Recovery passes those plus five recovery-specific checks for a 21/21 recovery audit.
- Runtime test coverage must include both Conveyor and No Conveyor configurations plus major cart/drill attachment arrangements.

## Bourgault 7950B V6 notes

- Four logical tanks front-to-back: 9,691 / 1,938 / 4,228 / 17,618 L.
- Tank 4 represents factory Tank 1A + FLEX as one logical unit.
- Static fill-volume segmentation is high confidence.
- V6 Tank 1 conveyor reach concentrated excessive articulation in the first two primary joints.
- V6 passes its historical 18/18 static checks, but those checks did not verify physical flap assignment.
- Deeper geometry audit proved Tank 3 belongs to `tankFlapsBack`; V6 leaves that group closed at the 0.400 Tank 3 selector stop. V6 is therefore HOLD despite the historical validator pass.

## Bourgault 7950B V7 notes

Current candidate:

`FS25_Bourgault_3320_4Tank_V7_Engineering.zip`

SHA-256:

`190b358ed1f21b411a11eb2d4cd0fc1d59f6f6cd293f93f9e7e239b307a17e2d`

- Candidate is rebuilt from the verified user-supplied Hispano V3 donor archive using `tools/build_bourgault_v7_from_v3.py`; donor assets themselves are not committed publicly.
- Two independent rebuilds from the same source and project Lua produced byte-identical V7 archives.
- Donor-aware static engineering audit passes **30/30** checks.
- Required flap relationship is implemented: Tanks 1-2 front group; Tanks 3-4 rear group.
- At Tank 3 / 0.400, rear flap evaluates fully open and front flap fully closed.
- Exact-fill-root activation is exclusive at all four selector stops.
- Tank 1 uses the distributed special-reach pose targeting pipe Z approximately +1.900 m rather than V6's concentrated two-joint overtravel.
- Tank 2 and Tank 3 remain close to directly recovered donor states.
- Compatibility bridge no longer accepts arbitrary products merely because one tank already supports them.
- Primary product authority is the `seeds fertilizer` categories, including products correctly appended to those categories by other mods.
- Crop-specific standalone seed products use the narrower `ends in SEED` fallback until explicit Realistic Seeder registration data is captured.
- The V7 validator now samples the actual flap animation and reconstructs Tank 1 pipe kinematics rather than treating node presence as proof.
- Remaining work is runtime validation: visual linkage/hoses/collision, fill-trigger behavior, product heaps, drill consumption, save/reload, and multiplayer.

## Realistic Seeder notes

Current intended flow:

1. Use normal `seeds fertilizer` categories.
2. Detect additional registered crop-specific seed fill types when required.
3. Add the intended set across all relevant compartments.
4. Raise a fill-type state change so attached sowing/sprayer tools rebuild their source lists.

Production hardening still required:

- Replace heuristic seed-name matching with a verified allowlist/registration mapping where practical.
- Consolidate equipment-specific bridge logic only after both carts pass runtime tests.
- Reduce recurring polling if a reliable registration lifecycle hook is identified.
- Confirm dedicated-server/client synchronization.

## Precision Farming policy

Precision Farming remains the authority for soil and agronomy systems. Current air-cart changes alter storage, loading, and product compatibility only and are not intended to replace soil-state simulation.

## Version discipline

When a game update or dependency update occurs, move the affected row back to **TESTING** until the minimum protocol in `TESTING.md` has been rerun. A static validator pass never overrides a known physical or runtime defect.
