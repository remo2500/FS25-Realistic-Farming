# Compatibility Matrix

_Last updated: 2026-09-15_

This matrix tracks known compatibility status for the active FS25 Realistic Farming components.

| Component | Base functionality | Realistic Seeder | Precision Farming | Save/reload | Multiplayer | Status |
|---|---|---|---|---|---|---|
| Seed Hawk 660 3-Tank RS V3 | PASS structurally | TESTING / high confidence | No known conflict | TESTING | Not yet tested | **TEST READY** |
| Bourgault 7950B V6 Engineering | PASS structurally except flap timing | Matcher works structurally but over-broad | No known conflict | Not promoted | Not tested | **HOLD** |
| Bourgault 7950B V7 | ACTIVE static hardening | Narrowed category + suffix fallback | No known conflict | Pending candidate | Pending | **ACTIVE** |
| Bourgault 71300 | Not started | Planned | Planned | Planned | Planned | ROADMAP |
| Shared Realistic Seeder compatibility layer | Equipment-specific prototypes | ACTIVE | N/A | TESTING | Not yet tested | ACTIVE |
| ProBox crop-specific packaging | Not started | Planned | N/A | Planned | Planned | ROADMAP |

## Seed Hawk 660 notes

- Three donor compartments retained: 5,600 / 5,600 / 10,600 L.
- All three tanks use the same seed/fertilizer category architecture.
- V3 preserves the union of types already present on the three donor units, important because Tank 3 was previously observed accepting the crop-specific products that Tanks 1 and 2 missed.
- V3 removes the unsupported cart-level sprayer `loadInfoIndex` attribute found during the V2 audit.
- V3 tightens custom-seed fallback matching to names ending in `SEED`, excluding generic `SEEDS`.
- Current V3 candidate passes 16/16 project static validation checks.
- Runtime test coverage must include both Conveyor and No Conveyor configurations plus major cart/drill attachment arrangements.

## Bourgault 7950B V6 notes

- Four logical tanks front-to-back: 9,691 / 1,938 / 4,228 / 17,618 L.
- Tank 4 represents factory Tank 1A + FLEX as one logical unit.
- Static fill-volume segmentation is high confidence.
- Tank 1 conveyor reach remains a mechanical HOLD item.
- V6 passes its historical 18/18 static checks, but those checks did not verify physical flap assignment.
- Deeper geometry audit proved Tank 3 belongs to `tankFlapsBack`; V6 leaves that group closed at the 0.400 Tank 3 selector stop. V6 is therefore HOLD despite the validator pass.

## Bourgault 7950B V7 notes

- V7 is a new versioned engineering target; no candidate ZIP or checksum exists yet.
- Required flap relationship: Tanks 1-2 front group; Tanks 3-4 rear group.
- At Tank 3 / 0.400, rear flap must be fully open and front flap fully closed.
- Compatibility bridge no longer accepts arbitrary products merely because one tank already supports them.
- Primary product authority is the `seeds fertilizer` categories, including products correctly appended to those categories by other mods.
- Crop-specific standalone seed products use the narrower `ends in SEED` fallback until explicit Realistic Seeder registration data is captured.
- V7 validator profile adds hardening checks and load/unload-node Z authority. Exact flap animation timing remains a separate mandatory engineering review gate.

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
