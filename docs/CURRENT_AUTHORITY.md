# Current Project Authority

_Last updated: 2026-09-16_

This file is the governing coordination document for the FS25 Realistic Farming project.

Status labels:

- **LOCKED** — validated design decision; do not reopen without a direct conflict.
- **ACTIVE** — current development work.
- **TEST READY** — static engineering is complete enough for the next runtime test cycle.
- **TESTING** — runtime validation in progress.
- **HOLD** — known issue prevents promotion.
- **SUPERSEDED** — retained only for historical/reference use.

---

## 1. Global project rules

### LOCKED

- Multi-compartment air carts should model each physical main tank as an independent logical fill unit wherever practical.
- Tank numbering for custom work is **front-to-back**.
- Physical loading equipment should select the destination compartment. Avoid artificial keyboard tank switching unless runtime constraints make it necessary.
- Seed and fertilizer should both be valid compartment categories where the real cart permits flexible product use.
- Precision Farming remains the soil/agronomy authority. This project should complement it rather than duplicate soil simulation.
- Third-party donor assets are not to be redistributed in this public repository unless licensing explicitly permits it.
- Candidate ZIPs must be versioned; do not silently replace a previously distributed candidate with different contents under the same version label.

---

## 2. Bourgault 3320 / 7950B

### Current status

**V7 Engineering — TEST READY / runtime validation pending**

Current candidate:

`FS25_Bourgault_3320_4Tank_V7_Engineering.zip`

SHA-256:

`190b358ed1f21b411a11eb2d4cd0fc1d59f6f6cd293f93f9e7e239b307a17e2d`

ZIP entries: **61**

Static status: **30/30 donor-aware engineering checks PASS**.

The V7 archive is generated locally from the verified user-supplied V3 donor using the project rebuild tool. It is intentionally not committed to this public repository because the donor archive identifies author **Hispano** and contains no explicit redistribution license.

Rebuild authority:

`tools/build_bourgault_v7_from_v3.py`

The rebuild tool:

- accepts the verified V3 source SHA-256 `30eebabb116e1932a53f25b78feb41c37fdda66260933d05c560302db5f9d69a`;
- refuses an unknown donor by default;
- applies the project-owned V7 compatibility script;
- uses deterministic ZIP metadata for the added Lua file;
- produced byte-identical output in two independent rebuilds from the same inputs.

### Historical V6 status

**V6 Engineering — HOLD**

V6 SHA-256:

`6072d0f1e805a684bd926aa97fcbcca3d5b7ef5f9429d92c3697d59b26289651`

V6 remains historical only. Its deeper geometry audit proved that Tank 3 belongs to `tankFlapsBack` while V6 leaves that group closed at selector stop 0.400. Its Tank 1 special-reach pose also concentrates more overtravel in Arms 1-2 than the V7 distributed solution. Do not use V6 for the next promotion test.

### Project-owned / donor-safe authorities

- Compatibility source: `scripts/compatibility/Bourgault7950FourTankCompat.lua`
- Patch specification: `equipment/bourgault_7950/PATCH_SPEC.md`
- Tank 1 engineering note: `equipment/bourgault_7950/TANK1_CONVEYOR_ENGINEERING.md`
- V7 kinematic solve: `equipment/bourgault_7950/V7_KINEMATIC_SOLVE.md`
- V3 engineering reference: `equipment/bourgault_7950/reference/`
- Forward-kinematics helper: `tools/bourgault7950_forward_kinematics.py`
- Animation inspection helper: `tools/extract_i3d_animation.py`
- Candidate validator: `tools/validate_candidate.py`

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

Untouched donor geometry establishes the following top openings, with +Z toward the tractor/front:

| Opening | Center Z | Approximate Z span | Logical use | Flap group |
|---|---:|---:|---|---|
| A | +2.121 m | +1.590 to +2.652 | Tank 1 | `tankFlapsFront` |
| B | +0.721 m | +0.190 to +1.252 | Tank 2 | `tankFlapsFront` |
| C | -0.678 m | -1.209 to -0.147 | Tank 3 | `tankFlapsBack` |
| D | -1.792 m | rear region | Tank 4 main opening 1 | `tankFlapsBack` |
| E | -2.442 m | rear region | Tank 4 main opening 2 | `tankFlapsBack` |
| F | -3.606 m | FLEX region | Tank 4 FLEX opening | `tankFlapsBack` |

D and E are two lid openings over the same rear main tank, not separate logical compartments.

### V7 fill-volume architecture

Static geometry remains **PASS / high confidence**:

- Tank 1 envelope: approximately +1.481 to +2.761 m.
- Tank 2 envelope: approximately +0.081 to +1.361 m.
- Tank 3 envelope: approximately -1.278 to -0.078 m.
- Tank 4 main envelope: approximately -2.820 to -1.440 m.
- Tank 4 FLEX envelope: approximately -4.331 to -2.881 m.

Tank 4 remains one logical 17,618 L fill unit split across main/FLEX visual envelopes at 82/18.

### V7 selector authority

Selector stops:

| Tank/state | Normalized stop | 10 s animation time |
|---|---:|---:|
| Tank 1 | 0.000 | 0 s |
| Tank 2 | 0.200 | 2 s |
| Tank 3 | 0.400 | 4 s |
| Tank 4 | 0.600 | 6 s |
| Transport | 1.000 | 10 s |

Exact-fill-root activation is statically verified to be exclusive at all four tank stops.

### V7 flap authority

**LOCKED physical assignment; static animation PASS; runtime visual proof pending**

- Tanks 1-2 -> front flap group open.
- Tanks 3-4 -> rear flap group open.
- Transport -> both groups closed/stowed.

Recovered donor numeric convention:

- open approximately `0 0 -100`
- closed approximately `0 0 0`

Static animation sampling verifies:

- 0.200 / Tank 2: front open, rear closed.
- 0.400 / Tank 3: **front closed, rear open**.
- 0.600 / Tank 4: front closed, rear open.
- 1.000 / transport: both closed.

This resolves the confirmed V6 Tank 3 flap defect statically. Runtime screenshot/visual confirmation is still required.

### V7 conveyor / Tank 1 authority

Recovered donor loading hierarchy is a nested four-arm mechanism:

- Arm 1: +100 deg Y
- Arm 2: -50 deg Y
- Arm 3: -135 deg Y
- Arm 4: +21 deg X
- Arm 4 loading translation: `0 0.28 -0.074`

The forward model independently reproduces the historical V6 Tank 1 discharge: applying V6 Arm 1/2 values 107.99 / -65.60 deg produces pipe Z **+1.651514 m**, within about 1.5 mm of the earlier +1.650 m audit. This validates the transform convention used for V7 static engineering.

A search across the full observed donor animation ranges found no donor-range-only pose capable of reaching front opening A. Some controlled overtravel is therefore unavoidable unless the physical conveyor geometry itself is remodeled.

#### Recommended V7 Tank 1 pose — implemented in current candidate

- Arm 1 = **+105.164095 deg**
- Arm 2 = **-59.356622 deg**
- Arm 3 = **-145.314298 deg**
- Arm 4 = **+21 deg**
- Arm 4 translation = **`0 0.28 -0.074`**

Calculated pipe position:

- X approximately `0.000 m`
- Y approximately `+4.027 m`
- Z approximately **`+1.900 m`**

Opening-A margins:

- rear edge: **0.310 m**
- front edge: **0.752 m**
- 0.221 m rearward of opening center

Modeled hydraulic extension relative to donor loading pose:

- Arm 1: +1.722%
- Arm 2: +4.432%

Relative to V6, this reduces the excess modeled hydraulic extension by approximately 34.4% on Arm 1 and 40.6% on Arm 2 while improving opening margin.

#### Secondary center solution — NOT current candidate

Only if runtime evidence shows +1.900 m is insufficient:

- Arm 1 = +106.584529 deg
- Arm 2 = -60.997442 deg
- Arm 3 = -146.992740 deg
- Arm 4 = +21 deg
- target Z = +2.121 m

Do not revert first to the V6 two-joint strategy.

### Tank 2 / Tank 3 donor-state confirmation

- Donor loading state `100 / -50 / -135 / 21` yields pipe Z about **+0.491 m**, effectively the intended Tank 2 position.
- Donor state `90 / -33 / -135 / 21` yields pipe Z about **-0.775 m**, effectively the intended Tank 3 position.

These positions remain close to genuine donor states. Tank 1 is the special-reach case.

### Realistic Seeder / custom-input integration

**Static PASS / runtime pending**

V7 policy:

1. Use normal `seeds fertilizer` category membership as primary authority.
2. Add standalone crop-specific fill types whose internal names end in `SEED`, excluding generic `SEEDS`, as a temporary compatibility fallback.
3. Mirror only that approved set to Tanks 1-4.
4. Raise `VehicleStateChange.FILLTYPE_CHANGE` after additions so attached sowing/sprayer source caches rebuild.

V7 removes V6's broad `SEED` substring search and unrestricted union of products supported by any one tank.

The suffix fallback remains heuristic. Explicit Realistic Seeder registration/mapping is preferable if reliable runtime registration data becomes available.

### V7 static validation status

The exact candidate passes **30/30 donor-aware engineering checks**, including:

- ZIP CRC/integrity;
- XML/I3D parsing;
- version/title and compatibility-script registration;
- four fill units and 33,475 L capacity authority;
- seed/fertilizer category authority;
- exact-fill roots;
- five fill-volume mappings including Tank 4 82/18 split;
- fill-volume transforms and visibility;
- four load/unload infos and Z authority;
- new I3D mappings;
- selector stops and final transport close;
- sprayer representative;
- compatibility cache refresh / four-unit targeting / narrowed seed fallback;
- actual flap animation states;
- exact-fill-root exclusivity;
- Tank 1/2/3/4 calculated pipe positions;
- no new I3D `nodeId` collisions beyond the donor's existing TransformGroup/UserAttribute pairings.

Static PASS does **not** prove visual linkage/hoses/collision behavior, fill-trigger reliability, product heaps, save/reload, or multiplayer.

---

## 3. Seed Hawk 660

### Current candidate

**3-Tank RS V3 — TEST READY / runtime validation pending**

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

**TESTING / high confidence**

- All three tanks advertise the same `seeds fertilizer` categories.
- V3 preserves the union already present on the three units because Tank 3 was the previously observed working compartment for custom seed products.
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

Required runtime coverage additionally includes the No Conveyor store configuration and major cart/drill attachment arrangements.

---

## 4. Shared compatibility-layer policy

### Current architecture

**TESTING / equipment-specific prototypes**

Purpose:

1. Start with normal seed/fertilizer categories.
2. Detect registered crop-specific seed fill types after mods load.
3. Synchronize supported types across intended compartments.
4. Trigger a fill-type state refresh so attached sowing/sprayer tools rebuild source lists.

The Bourgault and Seed Hawk scripts remain separate while their evidence bases differ.

### Known production improvements

- Replace heuristic seed-name detection with explicit/proven Realistic Seeder registration data where practical.
- Consolidate duplicated synchronization logic only after both carts pass runtime tests.
- Replace periodic 750 ms scanning with an event-driven or one-time post-registration hook if a reliable lifecycle point is identified.
- Confirm multiplayer/server-client determinism after runtime supported-fill-type changes.

---

## 5. Superseded / historical builds

### Bourgault

- V3 — superseded for candidate use, retained as the donor-derived geometry/animation reference under `equipment/bourgault_7950/reference/`.
- V4 — superseded: guessed conveyor targets and transformed combined fill meshes.
- V5 — superseded: improved geometry targets but excessive primary articulation and inadequate front fill-volume segmentation.
- V6 — **HOLD historical**: stronger architecture but confirmed Tank 3 flap defect and over-broad compatibility matcher; Tank 1 pose superseded.

### Seed Hawk

- RS V2 — superseded by V3 cleanup before promotion.

Do not return to superseded approaches except for regression/history analysis.

---

## 6. Repository development authority

Project-owned assets include:

- compatibility scripts: `scripts/compatibility/`
- equipment patch specifications: `equipment/`
- donor-safe reference data: `equipment/bourgault_7950/reference/`
- donor-safe rebuild policy: `patches/README.md`
- checksum authority: `builds/CANDIDATE_CHECKSUMS.md`
- runtime protocol: `docs/TESTING.md`
- validators / kinematic / rebuild tools: `tools/`

Candidate ZIPs and extracted third-party donor trees remain intentionally excluded from the public repository.

Current V7 work is developed on branch:

`bourgault-v7-static-hardening`

Draft PR #1 remains unmerged until runtime evidence is reviewed.

---

## 7. Promotion criteria

A cart may be promoted from TEST READY/TESTING to LOCKED/approved only after:

- fresh purchase loads without XML/Lua errors;
- every compartment accepts normal seeds and fertilizer;
- every compartment accepts at least one known Realistic Seeder crop-specific seed product;
- conveyor position aligns with the intended physical opening and the correct flap group is visibly open;
- Tank 1 Arm-3/linkage/hose/collision behavior is visually plausible at its special-reach pose;
- each selector stop fills only the intended compartment;
- product heaps stay within intended compartment walls;
- attached drill consumes the correct product from each compartment;
- save/reload preserves fill type, fill level, and selector/cover state;
- multiplayer shows no desync if multiplayer support is intended.

Existing purchased donor carts should be emptied/sold before installing a changed multi-tank architecture unless savegame migration has been explicitly validated.
