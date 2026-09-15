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

---

## 2. Bourgault 3320 / 7950B

### Current candidate

**V6 Engineering — TESTING**

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

### Fresh-purchase state

**TESTING, structurally approved**

The final selector state closes the `loadingPipe` animation to 1.0, preserving the original fully stowed transport endpoint on a fresh purchase.

---

## 3. Seed Hawk 660

### Current candidate

**3-Tank RS V2 — TESTING**

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

### Known cleanup item

**ACTIVE**

Remove unsupported `loadInfoIndex` from the cart-level `<sprayer>` element. FS25 Sprayer supports `fillUnitIndex`, `unloadInfoIndex`, and `fillVolumeIndex`; the extra `loadInfoIndex` is not part of the specialization schema and should not remain in a final build.

### Seed-type matcher hardening

**ACTIVE**

The current compatibility fallback treats fill-type names containing `SEED` as candidate crop-specific seed products. This is acceptable for testing but too broad for production. Final logic should use either:

- an explicit runtime allowlist based on actual Realistic Seeder registered products, or
- a stricter naming pattern proven against the installed Realistic Seeder version.

---

## 4. Realistic Seeder compatibility layer

### Current architecture

**TESTING**

Purpose:

1. Start with normal seed/fertilizer categories.
2. Detect registered crop-specific seed fill types after all mods have loaded.
3. Synchronize those supported fill types across every compartment of the target air cart.
4. Trigger a fill-type state refresh so attached sowing/sprayer tools rebuild their source lists.

### Known production improvements

- Replace periodic 750 ms scanning with event-driven or one-time post-registration initialization if a reliable lifecycle hook is identified.
- Replace broad `SEED` substring detection with a proven allowlist/pattern.
- Ensure multiplayer/server-client state remains deterministic after runtime supported-fill-type changes.

---

## 5. Superseded Bourgault builds

- V3 — superseded: incorrect selector positions and startup state behavior.
- V4 — superseded: improved state handling and Realistic Seeder concept, but still used guessed conveyor targets and transformed combined fill meshes.
- V5 — superseded: geometry-derived targets were better, but primary conveyor joints were driven beyond believable donor limits and front fill-volume segmentation was still inadequate.

Do not return to these approaches unless specifically investigating regression history.

---

## 6. Promotion criteria

A cart may be promoted from TESTING to LOCKED/approved only after:

- Fresh purchase loads without XML/Lua errors.
- Every compartment accepts normal seeds and fertilizer.
- Every compartment accepts at least one known Realistic Seeder crop-specific seed product.
- Conveyor position aligns with the intended physical opening.
- Product heaps stay within the intended compartment walls.
- Attached drill can consume the correct product from each compartment.
- Save/reload preserves fill type, fill level, and selector/cover state.
- Multiplayer test shows no desync if the project is intended for multiplayer use.
