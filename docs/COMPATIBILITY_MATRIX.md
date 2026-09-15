# Compatibility Matrix

_Last updated: 2026-09-15_

This matrix tracks known compatibility status for the active FS25 Realistic Farming components.

| Component | Base functionality | Realistic Seeder | Precision Farming | Save/reload | Multiplayer | Status |
|---|---|---|---|---|---|---|
| Seed Hawk 660 3-Tank RS V2 | PASS structurally | TESTING | No known conflict | TESTING | Not yet tested | TESTING |
| Bourgault 7950B V6 Engineering | PASS structurally | TESTING | No known conflict | TESTING | Not yet tested | TESTING |
| Bourgault 71300 | Not started | Planned | Planned | Planned | Planned | ROADMAP |
| Shared Realistic Seeder compatibility layer | Prototype works structurally | ACTIVE | N/A | TESTING | Not yet tested | ACTIVE |
| ProBox crop-specific packaging | Not started | Planned | N/A | Planned | Planned | ROADMAP |

## Seed Hawk 660 notes

- Three donor compartments retained: 5,600 / 5,600 / 10,600 L.
- All three tanks now use the same seed/fertilizer category architecture.
- Realistic Seeder synchronization is intended to make Tanks 1 and 2 behave like Tank 3.
- One cleanup remains: remove unsupported `loadInfoIndex` from the cart-level sprayer element.

## Bourgault 7950B notes

- Four logical tanks front-to-back: 9,691 / 1,938 / 4,228 / 17,618 L.
- Tank 4 represents factory Tank 1A + FLEX as one logical unit.
- Tanks 1-3 use separate physical fill-volume envelopes.
- Tank 4 uses two physical fill-volume regions with an 82/18 capacity split.
- Tank 1 conveyor reach remains the major mechanical item requiring runtime proof.

## Realistic Seeder notes

Current project compatibility logic:

1. Uses normal `seeds fertilizer` fill type categories.
2. Detects additional registered crop-specific seed fill types at runtime.
3. Adds those fill types to every relevant compartment.
4. Raises a fill-type state change so attached sowing/sprayer tools rebuild their source lists.

Production hardening still required:

- Replace broad `SEED` substring matching with a verified allowlist or stricter pattern.
- Reduce recurring polling if a reliable registration lifecycle hook is identified.
- Confirm dedicated-server/client synchronization.

## Precision Farming policy

Precision Farming remains the authority for soil and agronomy systems. Current air-cart changes only alter storage, loading, and product compatibility and are not intended to replace or duplicate Precision Farming behavior.

## Version discipline

When a game update or dependency update occurs, move the affected row back to **TESTING** until at least the minimum test suite in `TESTING.md` has been rerun.
