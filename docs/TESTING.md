# Runtime Testing Protocol

_Last updated: 2026-09-16_

Use this protocol before promoting any air-cart build from TESTING to approved/LOCKED.

## General test setup

- Disable superseded versions of the same cart.
- Buy a **fresh cart** for initial startup-state testing.
- Record the FS25 game version and dependency mod versions.
- Keep `log.txt` after every failed or suspicious test.
- Where possible, use clearly different products in adjacent tanks so visual bleed is obvious.
- Do not use an old purchased development cart as proof of a changed fill-unit architecture.

## Seed Hawk 660 — required test

1. Purchase a fresh Seed Hawk cart with the **Conveyor** configuration.
2. Confirm normal initial conveyor/transport state.
3. Test the same known Realistic Seeder crop-specific seed product in Tanks 1, 2, and 3.
4. Confirm each tank accepts fertilizer as well.
5. Fill all three tanks with distinguishable products and inspect heap boundaries.
6. Attach the intended Seed Hawk drill and confirm it can source/consume the correct product from each compartment.
7. Save and reload with non-zero fill in all three tanks.
8. Verify fill types and levels are preserved.
9. Repeat a three-compartment filling smoke test with the **No Conveyor** store configuration.
10. Smoke-test each major cart/drill attachment arrangement supplied by the pack so the three-tank architecture is not validated against only one combination.
11. Review `log.txt` for XML, Lua, fill-unit, specialization, or missing-node warnings/errors.

### Seed Hawk pass criteria

- All three tanks accept the same crop-specific Realistic Seeder seed.
- No tank silently converts crop-specific seed back to generic `SEEDS`.
- Drill consumption works from all three tanks.
- No product visually appears in the wrong compartment.
- Conveyor and No Conveyor configurations retain valid filling behavior.
- Save/reload is stable.

## Bourgault 7950B — V7 required test

**Next runtime candidate:**

`FS25_Bourgault_3320_4Tank_V7_Engineering.zip`

SHA-256:

`190b358ed1f21b411a11eb2d4cd0fc1d59f6f6cd293f93f9e7e239b307a17e2d`

Pre-runtime status: **30/30 donor-aware static engineering checks PASS**.

Do **not** use V6 for the next promotion test. V6 has a confirmed Tank 3 physical-hatch timing defect and its Tank 1 pose has been superseded by the distributed V7 solve.

1. Remove/disable V3/V4/V5/V6 development copies so only the V7 mod is active.
2. Purchase a **fresh V7 cart**. Do not use an existing savegame cart as the first test.
3. Confirm no XML/Lua/specialization errors appear during purchase/load.
4. Confirm the conveyor is fully stowed/closed at purchase.
5. Cycle selector states Tank 1 -> Tank 2 -> Tank 3 -> Tank 4 -> closed/transport.
6. Capture overhead and side screenshots at every selector position.
7. Verify discharge point is physically inside the intended opening.
8. Verify flap state at each selector:
   - Tank 1: front flap group open.
   - Tank 2: front flap group open.
   - Tank 3: **rear flap group fully open and front group fully closed**.
   - Tank 4: rear flap group open.
   - Transport: both flap groups closed/stowed.
9. Inspect **Tank 1** especially closely. Static V7 engineering predicts approximately:
   - Arm 1: `+105.164095 deg`
   - Arm 2: `-59.356622 deg`
   - Arm 3: `-145.314298 deg`
   - Arm 4: `+21 deg`
   - pipe position: approximately `X 0.000 / Y +4.027 / Z +1.900 m`
   - opening-A rear-edge margin: approximately `0.310 m`
10. For Tank 1, inspect the Arm-3 joint, hydraulic/linkage behavior, hoses, nearby tank structure, lid clearance, collision/intersection, and downspout insertion depth. The static solve deliberately distributes reach across Arms 1-3 and still requires visual proof.
11. Verify only the selected tank presents an active exact-fill trigger. Filling Tank 1 must not fill Tanks 2-4, and repeat this isolation test for every selector stop.
12. Test the same known Realistic Seeder crop-specific seed in Tanks 1-4.
13. Confirm fertilizer is accepted in Tanks 1-4, including any expected dry fertilizer products supplied through the installed fertilizer category extensions.
14. Fill all four logical tanks with distinguishable products.
15. Capture an overhead screenshot of product heaps.
16. Confirm Tank 1/2/3 heap separation and Tank 4 main/FLEX visual behavior.
17. Attach the intended Bourgault drill and confirm consumption from every compartment.
18. Save/reload with different products and non-zero fill levels in all four tanks.
19. Verify selector/cover state and fill data survive reload.
20. Review `log.txt` for XML, Lua, fill-unit, animation, missing-node, specialization, or fill-source warnings/errors.

### Bourgault V7 pass criteria

- Fresh cart loads and purchases without XML/Lua errors.
- Fresh cart starts in transport/stowed state.
- Correct physical flap group is open at every selector position.
- Tank 3 no longer presents its fill point through a closed hatch.
- All four selector positions are mechanically believable.
- Tank 1's distributed special-reach pose does not visibly overstretch/intersect the Arm-3 linkage, hoses, or tank structure.
- Tank 1 has reliable fill-trigger margin at the approximately Z +1.900 m discharge position.
- Each selector stop fills only its intended tank.
- All four tanks accept crop-specific Realistic Seeder seed and fertilizer.
- No cross-compartment heap bleed materially misrepresents tank boundaries.
- Attached drill finds and consumes all supported products correctly.
- Save/reload is stable.

### If Tank 1 +1.900 m is insufficient

Do not return to the V6 two-joint pose as the first response.

The precomputed secondary distributed solution targets opening center Z +2.121 m:

- Arm 1 = `+106.584529 deg`
- Arm 2 = `-60.997442 deg`
- Arm 3 = `-146.992740 deg`
- Arm 4 = `+21 deg`

Only move toward this center solution if runtime trigger or visual evidence shows that the recommended +1.900 m pose lacks adequate margin.

## Realistic Seeder compatibility test

Use at least one crop-specific seed fill type known to come from Realistic Seeder rather than the base-game generic seed product.

Recommended comparison:

1. Test generic `SEEDS` first.
2. Test a crop-specific Realistic Seeder product previously known to work in a donor/working compartment.
3. Repeat with every compartment.
4. If one compartment fails, capture selected tank, product name, loading source/container, HUD display, trigger-alignment screenshot, and `log.txt`.

## Custom fertilizer regression test

Because category-based compatibility may be extended by other installed mods, record at least one expected custom dry fertilizer product if one is present in the current mod stack. Confirm that it is accepted consistently by every flexible air-cart compartment intended to carry fertilizer. Do not use liquid or otherwise physically unsuitable products as a pass/fail criterion for these dry cart tanks.

## Savegame migration warning

Neither active cart should claim transparent migration from the original donor architecture until explicitly proven.

Existing purchased donor carts should be emptied/sold before installing a changed multi-tank version unless migration has been tested. Changes to fill-unit count/index/capacity can cause saved fill-unit records to refer to different physical compartments.

A fresh purchase is mandatory for first validation of every major architecture change.

## Multiplayer test

Before calling a compatibility bridge release-ready:

1. Host or dedicated server loads the same mod set.
2. Client joins after mission load.
3. Verify all tanks expose the same intended supported fill types on server and client.
4. Fill different compartments from client and server sides.
5. Verify fill level/type synchronization.
6. Disconnect/rejoin and recheck state.
7. Review both server and client logs.

## Failure reporting template

Record:

- Build/version:
- SHA-256:
- Game version:
- Dependency versions:
- Cart:
- Store configuration:
- Tank number:
- Product/fill type:
- Expected result:
- Actual result:
- Reproducible every time: yes/no
- Fresh purchase or existing save cart:
- Screenshot filenames:
- Relevant `log.txt` excerpt:

Do not promote a build while a repeatable Must Fix issue remains unresolved.
