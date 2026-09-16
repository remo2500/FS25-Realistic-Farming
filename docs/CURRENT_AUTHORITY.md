# Current Project Authority

_Last updated: 2026-09-16_

This file is the governing coordination document for the FS25 Realistic Farming project.

Status labels:

- **LOCKED** — validated design decision; do not reopen without a direct conflict.
- **ACTIVE** — current development work.
- **TESTING** — structurally ready, awaiting runtime validation.
- **HOLD** — known issue prevents promotion.
- **SUPERSEDED** — retained only for historical reference.

---

## 1. Global project rules

### LOCKED

- Multi-compartment air carts should model each physical main tank as an independent logical fill unit wherever practical.
- Tank numbering for custom work is **front-to-back**.
- Physical loading equipment should select the destination compartment. Avoid artificial keyboard tank-switching unless runtime constraints make it necessary.
- Seed and fertilizer should both be valid compartment categories where the real cart permits flexible product use.
- Precision Farming remains the soil/agronomy authority. This project should complement it rather than duplicate soil simulation.
- Third-party donor assets are not to be redistributed in this public repository unless licensing explicitly permits it.
- Candidate ZIPs must be versioned; do not silently replace a previously distributed candidate with different contents under the same version label.

---

## 2. Bourgault 3320 / 7950B

### Current status

**V6 Engineering — HOLD**

V6 archive SHA-256:

`6072d0f1e805a684bd926aa97fcbcca3d5b7ef5f9429d92c3697d59b26289651`

V6 remains a historical engineering artifact. It passes its original 18/18 validator checks, but a deeper geometry audit proved that the physical Tank 3 hatch is closed at the Tank 3 selector stop. **Do not promote or spend the next runtime test cycle on V6 unchanged.**

**V7 — ACTIVE engineering target**

V7 is a new versioned target, not an in-place replacement of V6. No V7 candidate checksum exists yet.

Project-owned compatibility source:

`scripts/compatibility/Bourgault7950FourTankCompat.lua`

Patch authority:

`equipment/bourgault_7950/PATCH_SPEC.md`

Tank 1 engineering authorities:

- `equipment/bourgault_7950/TANK1_CONVEYOR_ENGINEERING.md`
- `equipment/bourgault_7950/V7_KINEMATIC_SOLVE.md`

Donor-safe V3 reference snapshot:

`equipment/bourgault_7950/reference/`

The V3 snapshot was captured from user-supplied archive SHA-256 `30eebabb116e1932a53f25b78feb41c37fdda66260933d05c560302db5f9d69a`. The archive itself is not stored in the public repository because it identifies author **Hispano** and contains no explicit redistribution license. The reference directory preserves the required animation, mapping, pivot, fill-root, fill-volume, outlet/effect, and hydraulic engineering data so this exact V3 ZIP should not need to be re-uploaded for future geometry work.

### LOCKED capacity model

Custom logical numbering is front-to-back:

| Logical tank | Physical factory region | Capacity |
|---|---|---:|
| Tank 1 | Factory Tank 4 | 9,691 L |
| Tank 2 | Factory Tank 3 | 1,938 L |
| Tank 3 | Factory Tank 2 | 4,228 L |
| Tank 4 | Factory Tank 1A + FLEX/Tank 1B | 17,618 L |

**Total: 33,475 L**

### LOCKED physical opening map

Untouched donor geometry produced six top openings, with +Z toward the tractor/front:

| Opening | Center Z | Approximate Z span | Interpretation | Flap group |
|---|---:|---:|---|---|
| A | +2.121 m | +1.590 to +2.652 | Front main tank opening | `tankFlapsFront` |
| B | +0.721 m | +0.190 to +1.252 | Second main tank opening | `tankFlapsFront` |
| C | -0.678 m | -1.209 to -0.147 | Third main tank opening | `tankFlapsBack` |
| D | -1.792 m | rear region | Rear 410-bu main opening 1 | `tankFlapsBack` |
| E | -2.442 m | rear region | Rear 410-bu main opening 2 | `tankFlapsBack` |
| F | -3.606 m | FLEX region | FLEX opening | `tankFlapsBack` |

D and E are two lid openings over the same rear main tank, not separate logical compartments.

### V7 flap authority

**LOCKED physical assignment; ACTIVE animation implementation**

The earlier assumption that the front flap group serves Tanks 1-3 is disproven.

Required selector/flap relationship:

- Tanks 1-2 -> `tankFlapsFront` open.
- Tanks 3-4 -> `tankFlapsBack` open.
- At Tank 3 selector stop **0.400 / 4 s**, the rear flap group must be fully open and the front group fully closed.

Recovered donor animation establishes the flap transforms:

- open: approximately `0 0 -100`
- closed: approximately `0 0 0`

Required transition:

- Front group open through 2 s, closes 2-4 s, remains closed afterward.
- Rear group closed through 2 s, opens 2-4 s, remains open through Tank 4, then closes during transport/stow.

The V7 validator now samples the actual `loadingPipe` animation and verifies the Tank 2 / Tank 3 / Tank 4 / transport flap states. Node presence alone is no longer considered sufficient.

### Current conveyor positions

| Tank | Current/historical discharge Z | Physical containment | Status |
|---|---:|---|---|
| Tank 1 | V6 +1.650 m | inside A by only about 0.06 m at rear edge | **HOLD / superseded Tank 1 pose** |
| Tank 2 | +0.493 m | inside B | TESTING; donor-derived pose |
| Tank 3 | -0.769 m | inside C | TESTING; donor-derived pose |
| Tank 4 | -1.792 m | centered on D | TESTING; donor-range pose |

### Tank 1 mechanical authority

**ACTIVE — donor-validated kinematic solve completed; runtime visual/trigger proof still required**

The uploaded V3 reference directly verifies the loading pose and full nested conveyor hierarchy:

- Arm 1: +100 degrees Y
- Arm 2: -50 degrees Y
- Arm 3: -135 degrees Y
- Arm 4: +21 degrees X
- Arm 4 translation: `0 0.28 -0.074`

A donor-safe forward model is stored at:

`tools/bourgault7950_forward_kinematics.py`

The model independently reproduces the historical V6 Tank 1 result: applying Arm 1 = 107.99 degrees and Arm 2 = -65.60 degrees gives pipe-effect Z **+1.651514 m**, within about 1.5 mm of the earlier +1.650 m geometry audit. This validates the recovered transform convention strongly enough for static engineering.

A numerical search across the complete observed V3 articulation ranges found no donor-range-only pose capable of reaching opening A. With the existing conveyor geometry, some controlled overtravel is therefore unavoidable for the new front Tank 1.

#### Recommended first V7 Tank 1 pose

Target pipe position: **Z +1.900 m**.

Recommended animation state:

- Arm 1 = **+105.164095 degrees**
- Arm 2 = **-59.356622 degrees**
- Arm 3 = **-145.314298 degrees**
- Arm 4 = **+21 degrees**
- Arm 4 translation = **`0 0.28 -0.074`**

Forward-model pipe result:

- X approximately 0.000 m
- Y approximately +4.027 m
- Z approximately +1.900 m

Opening-A margin:

- 0.310 m inside the rear edge
- 0.752 m inside the front edge
- 0.221 m rearward of opening center

Modeled Arm-1/Arm-2 hydraulic extension versus donor loading pose:

- Arm 1: +1.722%
- Arm 2: +4.432%

Compared with V6, this reduces excess hydraulic extension by approximately **34.4% on Arm 1** and **40.6% on Arm 2** while increasing the physical opening margin substantially.

The exact opening-center solution at Z +2.121 m remains a valid secondary option:

- Arm 1 = +106.584529 degrees
- Arm 2 = -60.997442 degrees
- Arm 3 = -146.992740 degrees
- Arm 4 = +21 degrees

Do not use that larger articulation unless the +1.900 m runtime trigger/visual test shows insufficient margin.

An Arm-3-only solution was evaluated and rejected as the primary approach because it would require approximately -155.356 degrees at Z +1.900 m or -158.663 degrees at the opening center, concentrating too much overtravel into one joint without visual collision proof.

### Tank 2 / Tank 3 donor-state confirmation

The recovered hierarchy confirms:

- donor loading state `100 / -50 / -135 / 21` gives pipe Z approximately **+0.491 m**, effectively the V6 Tank 2 target +0.493 m;
- donor state `90 / -33 / -135 / 21` gives pipe Z approximately **-0.775 m**, effectively the V6 Tank 3 target -0.769 m.

These positions should stay close to their donor-derived states in V7. Tank 1 is the special-reach case.

### Fill-volume architecture

Static geometry audit is **PASS / high confidence**:

- Tank 1 envelope: approximately +1.481 to +2.761 m.
- Tank 2 envelope: approximately +0.081 to +1.361 m.
- Tank 3 envelope: approximately -1.278 to -0.078 m.
- Tank 4 main envelope: approximately -2.820 to -1.440 m.
- Tank 4 FLEX envelope: approximately -4.331 to -2.881 m.

The front three compartments have physical longitudinal separation rather than overlapping copies of the donor combined volume. Tank 4 remains one logical fill unit across main + FLEX physical regions at 82/18. Exact generated heap appearance remains a runtime visual test item.

### Realistic Seeder / custom-input integration

**V7 ACTIVE hardening**

V7 compatibility policy is:

1. Use normal `seeds fertilizer` category membership as primary authority.
2. Add standalone crop-specific fill types whose internal names end in `SEED`, excluding generic `SEEDS`, as a temporary compatibility fallback.
3. Mirror only that approved set to Tanks 1-4.
4. Raise `VehicleStateChange.FILLTYPE_CHANGE` after additions so attached sowing/sprayer source caches rebuild.

V7 explicitly removes V6's broad `SEED` substring search and its unrestricted union of every product supported by any single tank.

The suffix matcher remains heuristic. Explicit Realistic Seeder product registration/mapping is still preferable once reliable runtime registration data is captured.

### Static validation

- Historical V6 profile remains available as `bourgault7950-v6` for archive verification.
- V7 profile is `bourgault7950-v7` and checks compatibility hardening, load/unload node authority, selector stops, actual flap animation states, and Tank 1 forward kinematics.
- V7 Tank 1 static acceptance requires the pipe Z to remain inside **+1.790 to +2.452 m**, stay reasonably close to the tank centerline, and not worsen the V6 Arm-1/Arm-2 overtravel ceilings.
- Static kinematics do not replace visual/runtime inspection of the Arm-3 joint, hoses, collision behavior, or fill trigger.

---

## 3. Seed Hawk 660

### Current candidate

**3-Tank RS V3 — TEST READY / runtime validation pending**

V3 supersedes V2 before runtime promotion. V3 changes only cleanup/compatibility behavior relative to V2:

- removes the unsupported cart-level sprayer `loadInfoIndex` attribute;
- tightens custom-seed fallback matching from any name containing `SEED` to names ending in `SEED`, excluding generic `SEEDS`;
- updates version/changelog text.

Candidate SHA-256:

`d052c302f3a54d0a77273dc02098185223094ca6e7971b5236eb114684edadcb`

Project-owned compatibility source:

`scripts/compatibility/SeedHawk660ThreeTankCompat.lua`

Patch authority:

`equipment/seedhawk_660/PATCH_SPEC.md`

### LOCKED compartment model

| Tank | Capacity |
|---|---:|
| Tank 1 | 5,600 L |
| Tank 2 | 5,600 L |
| Tank 3 | 10,600 L |

**Total: 21,800 L**

### Mechanical architecture

**LOCKED unless runtime evidence contradicts it**

- Existing donor conveyor geometry and original fill-root positions are retained.
- No extra mechanical overtravel is intentionally introduced.
- Existing independent fill-volume meshes are retained.
- Conveyor selector stops remain 0.000 / 0.234 / 0.534 with transport endpoint 1.000.

### Realistic Seeder integration

**TESTING, high confidence**

- All three tanks advertise the same `seeds fertilizer` categories.
- V3 first preserves the union already present on the three units; this is important because Tank 3 was the previously observed working compartment for custom seed products.
- A suffix-based `SEED` fallback covers additional standalone crop-specific registrations.
- Fill-source caches are refreshed after new supported types are discovered.

Do not alter the Seed Hawk V3 candidate before runtime testing without a specific reason; its current compatibility behavior is intentionally preserved for evidence continuity.

### Sprayer cleanup

**RESOLVED in V3**

```xml
<sprayer fillUnitIndex="3" unloadInfoIndex="3">
```

### Static validation

Current V3 archive passes **16/16** checks using profile `seedhawk660-v3`.

### Required test-coverage expansion

Before release, also test:

- the **No Conveyor** store configuration with all three compartments;
- the major cart/drill attachment arrangements included in the pack;
- fresh purchase, save/reload, and multiplayer if supported.

---

## 4. Shared compatibility-layer policy

### Current architecture

**TESTING / equipment-specific prototypes**

Purpose:

1. Start with normal seed/fertilizer categories.
2. Detect registered crop-specific seed fill types after mods load.
3. Synchronize supported types across the intended compartments.
4. Trigger a fill-type state refresh so attached sowing/sprayer tools rebuild source lists.

The Bourgault and Seed Hawk scripts remain separate while their evidence bases differ.

### Known production improvements

- Replace heuristic seed-name detection with explicit/proven Realistic Seeder registration data where practical.
- Consolidate duplicated synchronization logic only after both equipment candidates pass runtime tests.
- Replace periodic 750 ms scanning with an event-driven or one-time post-registration hook if a reliable lifecycle point is identified.
- Confirm multiplayer/server-client determinism after runtime supported-fill-type changes.

---

## 5. Superseded / historical builds

### Bourgault

- V3 — superseded for candidate use, but its recovered donor-derived conveyor hierarchy is retained as a geometry/animation reference under `equipment/bourgault_7950/reference/`.
- V4 — superseded: improved state handling and Realistic Seeder concept, but guessed conveyor targets and transformed combined fill meshes.
- V5 — superseded: better geometry-derived targets, but excessive primary conveyor articulation and inadequate front fill-volume segmentation.
- V6 — **HOLD historical candidate**: stronger four-tank architecture, but confirmed Tank 3 physical hatch timing defect and broad compatibility matcher.

### Seed Hawk

- RS V2 — superseded by V3 cleanup before promotion.

Do not return to superseded approaches except for regression/history analysis.

---

## 6. Repository development authority

Project-owned assets:

- Compatibility scripts: `scripts/compatibility/`
- Equipment patch specifications: `equipment/`
- Bourgault Tank 1 engineering note: `equipment/bourgault_7950/TANK1_CONVEYOR_ENGINEERING.md`
- Bourgault V7 kinematic solve: `equipment/bourgault_7950/V7_KINEMATIC_SOLVE.md`
- Bourgault donor-safe reference snapshots: `equipment/bourgault_7950/reference/`
- Donor-safe rebuild policy: `patches/README.md`
- Candidate/reference checksum authority: `builds/CANDIDATE_CHECKSUMS.md`
- Static candidate validator: `tools/validate_candidate.py`
- I3D animation extraction helper: `tools/extract_i3d_animation.py`
- Bourgault forward-kinematics helper: `tools/bourgault7950_forward_kinematics.py`

Candidate ZIPs and extracted third-party donor trees remain intentionally excluded.

Current V7 static-hardening work is developed on branch:

`bourgault-v7-static-hardening`

---

## 7. Promotion criteria

A cart may be promoted from TESTING to LOCKED/approved only after:

- Fresh purchase loads without XML/Lua errors.
- Every compartment accepts normal seeds and fertilizer.
- Every compartment accepts at least one known Realistic Seeder crop-specific seed product.
- Conveyor position aligns with the intended physical opening and the correct lid/flap group is open.
- Tank 1 Arm-3/linkage/hose/collision behavior is visually plausible at its special-reach pose.
- Product heaps stay within intended compartment walls.
- Attached drill can consume the correct product from each compartment.
- Save/reload preserves fill type, fill level, and selector/cover state.
- Multiplayer test shows no desync if multiplayer support is intended.

Existing purchased donor carts should be emptied/sold before installing a changed multi-tank architecture unless savegame migration has been explicitly validated.
