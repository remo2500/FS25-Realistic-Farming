# Compatibility Matrix

_Last updated: 2026-09-15_

This matrix tracks known compatibility status for the active FS25 Realistic Farming components.

| Component | Base functionality | Realistic Seeder | Precision Farming | Save/reload | Multiplayer | Status |
|---|---|---|---|---|---|---|
| Seed Hawk 660 3-Tank RS V3 | PASS structurally | TESTING | No known conflict | TESTING | Not yet tested | TESTING |
| Bourgault 7950B V6 Engineering | PASS structurally | TESTING | No known conflict | TESTING | Not yet tested | TESTING |
| Bourgault 71300 | Not started | Planned | Planned | Planned | Planned | ROADMAP |
| Shared Realistic Seeder compatibility layer | Equipment-specific prototypes work structurally | ACTIVE | N/A | TESTING | Not yet tested | ACTIVE |
| ProBox crop-specific packaging | Not started | Planned | N/A | Planned | Planned | ROADMAP |

## Seed Hawk 660 notes

- Three donor compartments retained: 5,600 / 5,600 / 10,600 L.
- All three tanks use the same seed/fertilizer category architecture.
- Realistic Seeder synchronization is intended to make Tanks 1 and 2 behave like Tank 3.
- V3 removes the unsupported cart-level sprayer `loadInfoIndex` attribute found during the V2 audit.
- V3 tightens custom-seed fallback matching to fill-type names ending in `SEED`, excluding the generic `SEEDS` name.
- Current V3 candidate passes 16/16 project static validation checks.

## Bourgault 7950B notes

- Four logical tanks front-to-back: 9,691 / 1,938 / 4,228 / 17,618 L.
- Tank 4 represents factory Tank 1A + FLEX as one logical unit.
- Tanks 1-3 use separate physical fill-volume envelopes.
- Tank 4 uses two physical fill-volume regions with an 82/18 capacity split.
- Tank 1 conveyor reach remains the major mechanical item requiring runtime proof.
- Current V6 candidate passes 18/18 project static validation checks.

## Realistic Seeder notes

Current project compatibility logic:

1. Uses normal `seeds fertilizer` fill type categories.
2. Detects additional registered crop-specific seed fill types at runtime.
3. Adds those fill types to every relevant compartment.
4. Raises a fill-type state change so attached sowing/sprayer tools rebuild their source lists.

Current matcher status:

- Seed Hawk V3: suffix-based `SEED` heuristic.
- Bourgault V6: broader `SEED` substring heuristic retained for candidate fidelity.

Production hardening still required:

- Replace heuristic matching with a verified allowlist or proven Realistic Seeder product mapping where practical.
- Consolidate duplicated equipment-specific bridge logic after both carts pass runtime tests.
- Reduce recurring polling if a reliable registration lifecycle hook is identified.
- Confirm dedicated-server/client synchronization.

## Precision Farming policy

Precision Farming remains the authority for soil and agronomy systems. Current air-cart changes only alter storage, loading, and product compatibility and are not intended to replace or duplicate Precision Farming behavior.

## Version discipline

When a game update or dependency update occurs, move the affected row back to **TESTING** until at least the minimum test suite in `TESTING.md` has been rerun.
