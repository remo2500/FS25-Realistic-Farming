# Current Project Authority

_Last updated: 2026-09-15_

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

### Current candidate

**V6 Engineering — TESTING**

Candidate SHA-256:

`6072d0f1e805a684bd926aa97fcbcca3d5b7ef5f9429d92c3697d59b26289651`

Project-owned compatibility source:

`scripts/compatibility/Bourgault7950FourTankCompat.lua`

Patch authority:

`equipment/bourgault_7950/PATCH_SPEC.md`

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

Untouched donor geometry produced six top opening centers, with +Z toward the tractor/front:

| Opening | Center Z | Interpretation |
|---|---:|---|
| A | +2.121 m | Front main tank opening |
| B | +0.721 m | Second main tank opening |
| C | -0.678 m | Third main tank opening |
| D | -1.792 m | Rear 410-bu main tank opening 1 |
| E | -2.442 m | Rear 410-bu main tank opening 2 |
| F | -3.606 m | FLEX region opening |

D and E are treated as two lid openings over the same rear main tank, not separate logical compartments.

### Current V6 conveyor targets

| Tank | Current discharge Z | Status |
|---|---:|---|
| Tank 1 | +1.650 m | **HOLD / runtime proof required** |
| Tank 2 | +0.493 m | TESTING; donor-range pose |
| Tank 3 | -0.769 m | TESTING; donor-range pose |
| Tank 4 | -1.792 m | TESTING; within donor articulation range |

### Known mechanical concern

Tank 1 still requires additional forward articulation beyond the original two-reservoir donor animation envelope. Approximate primary-arm positions are:

- Arm 1: ~107.99 degrees versus ~100 degrees donor maximum.
- Arm 2: ~-65.60 degrees versus ~-50 degrees donor maximum.

Do not mark the Tank 1 conveyor position LOCKED until in-game testing confirms acceptable linkage/hose behavior and reliable trigger alignment.

### Fill-volume architecture

V6 uses:

- Separate physical fill-volume envelopes for Tanks 1-3.
- One logical Tank 4 represented by two physical regions:
  - Main 410-bu region: 82%.
  - FLEX 90-bu region: 18%.

This architecture is **TESTING** visually. Logical separation is approved, but exact visual conformity to the cart walls still requires runtime validation.

### Realistic Seeder integration

**TESTING, high confidence**

- All four tanks advertise the same `seeds fertilizer` categories.
- Runtime compatibility logic synchronizes discovered crop-specific seed fill types across Tanks 1-4.
- When new supported fill types are added, the attached sowing/sprayer source caches are forced to refresh via fill-type state change.
- V6 still uses a broad `SEED` substring fallback. This remains a production-hardening item and should be versioned if changed.

### Fresh-purchase state

**TESTING, structurally approved**

The final selector state closes the `loadingPipe` animation to 1.0, preserving the original fully stowed transport endpoint on a fresh purchase.

### Static validation

Current V6 archive passes **18/18** checks in `tools/validate_candidate.py` using profile `bourgault7950-v6`.

---

## 3. Seed Hawk 660

### Current candidate

**3-Tank RS V3 — TESTING**

V3 supersedes V2 before runtime promotion. V3 changes only cleanup/compatibility behavior relative to V2:

- removes the unsupported cart-level sprayer `loadInfoIndex` attribute;
- tightens custom-seed fallback matching from any name containing `SEED` to names ending in `SEED`, excluding the generic `SEEDS` name;
- updates version/changelog text.

Candidate SHA-256:

`d052c302f3a54d0a77273dc02098185223094ca6e7971b5236eb114684edadcb`

Project-owned compatibility source:

`scripts/compatibility/SeedHawk660ThreeTankCompat.lua`

Patch authority:

`equipment/seedhawk_660/PATCH_SPEC.md`

### LOCKED compartment model

Retain the donor's three independent physical compartments:

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

### Realistic Seeder integration

**TESTING, high confidence**

- All three tanks advertise the same `seeds fertilizer` categories.
- Runtime compatibility logic synchronizes crop-specific seed types across Tanks 1-3.
- Fill-source caches are refreshed after new supported seed types are discovered.
- V3 uses an `ends in SEED` fallback rather than the broader V2 substring matcher.

### Sprayer cleanup

**RESOLVED in V3**

Cart-level sprayer authority is:

```xml
<sprayer fillUnitIndex="3" unloadInfoIndex="3">
```

The unsupported `loadInfoIndex` attribute from V2 is removed.

### Remaining seed-matcher hardening

**ACTIVE / production improvement**

The V3 suffix matcher is safer than V2 but is still heuristic. An explicit runtime allowlist based on the actual installed Realistic Seeder registered products remains preferable if reliable registration data can be captured.

### Static validation

Current V3 archive passes **16/16** checks in `tools/validate_candidate.py` using profile `seedhawk660-v3`.

---

## 4. Realistic Seeder compatibility layer

### Current architecture

**TESTING**

Purpose:

1. Start with normal seed/fertilizer categories.
2. Detect registered crop-specific seed fill types after all mods have loaded.
3. Synchronize those supported fill types across every compartment of the target air cart.
4. Trigger a fill-type state refresh so attached sowing/sprayer tools rebuild their source lists.

Current equipment scripts are intentionally separate while the two carts are still under runtime test.

### Known production improvements

- Consolidate duplicated synchronization logic into a reusable shared module once both carts pass runtime tests.
- Replace remaining heuristic seed-name detection with an explicit/proven Realistic Seeder product mapping where practical.
- Replace periodic 750 ms scanning with event-driven or one-time post-registration initialization if a reliable lifecycle hook is identified.
- Ensure multiplayer/server-client state remains deterministic after runtime supported-fill-type changes.

---

## 5. Superseded builds

### Bourgault

- V3 — superseded: incorrect selector positions and startup state behavior.
- V4 — superseded: improved state handling and Realistic Seeder concept, but still used guessed conveyor targets and transformed combined fill meshes.
- V5 — superseded: geometry-derived targets were better, but primary conveyor joints were driven beyond believable donor limits and front fill-volume segmentation was still inadequate.

### Seed Hawk

- RS V2 — superseded by V3 cleanup before promotion. Mechanical and three-tank architecture remain the same.

Do not return to superseded approaches unless specifically investigating regression history.

---

## 6. Repository development authority

Project-owned development assets now live in the repository:

- Compatibility scripts: `scripts/compatibility/`
- Equipment patch specifications: `equipment/`
- Donor-safe rebuild policy: `patches/README.md`
- Candidate checksum authority: `builds/CANDIDATE_CHECKSUMS.md`
- Static candidate validator: `tools/validate_candidate.py`

Candidate ZIPs and extracted third-party donor trees are intentionally excluded.

---

## 7. Promotion criteria

A cart may be promoted from TESTING to LOCKED/approved only after:

- Fresh purchase loads without XML/Lua errors.
- Every compartment accepts normal seeds and fertilizer.
- Every compartment accepts at least one known Realistic Seeder crop-specific seed product.
- Conveyor position aligns with the intended physical opening.
- Product heaps stay within the intended compartment walls.
- Attached drill can consume the correct product from each compartment.
- Save/reload preserves fill type, fill level, and selector/cover state.
- Multiplayer test shows no desync if the project is intended for multiplayer use.
