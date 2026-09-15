# Runtime Testing Protocol

_Last updated: 2026-09-15_

Use this protocol before promoting any air-cart build from TESTING to approved/LOCKED.

## General test setup

- Disable superseded versions of the same cart.
- Buy a **fresh cart** for initial startup-state testing.
- Record the FS25 game version and dependency mod versions.
- Keep `log.txt` after every failed or suspicious test.
- Where possible, use clearly different products in adjacent tanks so visual bleed is obvious.

## Seed Hawk 660 — required test

1. Purchase a fresh Seed Hawk cart.
2. Confirm normal initial conveyor/transport state.
3. Test the same known Realistic Seeder crop-specific seed product in:
   - Tank 1,
   - Tank 2,
   - Tank 3.
4. Confirm each tank accepts fertilizer as well.
5. Fill all three tanks with distinguishable products and inspect heap boundaries.
6. Attach the intended Seed Hawk drill and confirm it can source/consume the correct product from each compartment.
7. Save and reload with non-zero fill in all three tanks.
8. Verify fill types and levels are preserved.
9. Review `log.txt` for XML, Lua, fill-unit, specialization, or missing-node warnings/errors.

### Seed Hawk pass criteria

- All three tanks accept the same crop-specific Realistic Seeder seed.
- No tank silently converts crop-specific seed back to generic `SEEDS`.
- Drill consumption works from all three tanks.
- No product visually appears in the wrong compartment.
- Save/reload is stable.

## Bourgault 7950B — required test

1. Purchase a fresh cart.
2. Confirm the conveyor is fully stowed at purchase.
3. Cycle selector states Tank 1 -> Tank 2 -> Tank 3 -> Tank 4 -> closed.
4. Capture overhead and side screenshots at each tank position.
5. Verify discharge point is physically inside the intended opening.
6. Inspect Tank 1 carefully for:
   - impossible arm/linkage angles,
   - stretched or intersecting hoses,
   - collision with tank/lids,
   - unreliable fill-trigger position.
7. Test the same known Realistic Seeder crop-specific seed in Tanks 1-4.
8. Confirm fertilizer is accepted in Tanks 1-4.
9. Fill all four logical tanks with distinguishable products.
10. Capture an overhead screenshot of the product heaps.
11. Confirm Tank 1/2/3 heap separation and Tank 4 main/FLEX visual behavior.
12. Attach the intended Bourgault drill and confirm consumption from every compartment.
13. Save/reload with different products and non-zero fill levels in all four tanks.
14. Verify selector/cover state and fill data survive reload.
15. Review `log.txt`.

### Bourgault pass criteria

- Fresh cart starts in transport/stowed state.
- All four selector positions are mechanically believable.
- Tank 1 does not require visibly impossible articulation.
- All four tanks accept crop-specific Realistic Seeder seed and fertilizer.
- No cross-compartment heap bleed that materially misrepresents tank boundaries.
- Attached drill finds and consumes all supported products correctly.
- Save/reload is stable.

## Realistic Seeder compatibility test

Use at least one crop-specific seed fill type known to come from Realistic Seeder rather than the base-game generic seed product.

Recommended comparison:

1. Test generic `SEEDS` first.
2. Test a crop-specific Realistic Seeder product such as the same product previously known to work in the rear/working compartment.
3. Repeat with every compartment.
4. If one compartment fails, capture:
   - selected tank,
   - product name,
   - loading source/container,
   - HUD display,
   - screenshot of trigger alignment,
   - `log.txt`.

## Savegame migration warning

Do not use an older purchased multi-tank development cart as proof of a new build's startup behavior. Changes to fill-unit count/index/capacity can make old savegame records misleading.

A fresh purchase is mandatory for first validation of every major architecture change.

## Multiplayer test

Before calling a compatibility bridge release-ready:

1. Host or dedicated server loads the same mod set.
2. Client joins after mission load.
3. Verify all tanks expose the same supported fill types on server and client.
4. Fill different compartments from the client and server sides.
5. Verify fill level/type synchronization.
6. Disconnect/rejoin and recheck state.
7. Review both server and client logs.

## Failure reporting template

Record:

- Build/version:
- Game version:
- Dependency versions:
- Cart:
- Tank number:
- Product/fill type:
- Expected result:
- Actual result:
- Reproducible every time: yes/no
- Fresh purchase or existing save cart:
- Screenshot filenames:
- Relevant `log.txt` excerpt:

Do not promote a build while a repeatable Must Fix issue remains unresolved.
