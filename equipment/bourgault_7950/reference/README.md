# Bourgault 3320 / 7950B Uploaded Reference Manifest

_Captured: 2026-09-16_

This directory preserves the **engineering information needed for future Bourgault 7950 work** from the user-supplied archive `FS25_Bourgault_Series_3320.zip` without committing the complete third-party donor/candidate archive or model assets.

## Source identity

- Archive SHA-256: `30eebabb116e1932a53f25b78feb41c37fdda66260933d05c560302db5f9d69a`
- ZIP entries: **60**
- `modDesc.xml` author: **Hispano**
- `modDesc.xml` version: **2.0.0.4**
- English title: **Bourgault 3320-76 + 7950 Air Cart [4-Tank V3 F-R]**
- Classification: **working 4-Tank V3 front-to-rear build**. This is not the later V6 Engineering archive and is not V7 authority.

Relevant source-file hashes:

| File | SHA-256 | Bytes |
|---|---|---:|
| `modDesc.xml` | `1175b0acb52a119188169f5320e7fe68b7cee5856f99176e3f91d8be53120f9b` | 2244 |
| `xml/Series_7950B.xml` | `a58f8633ac5a7ae9e1f11bfb00f5beeeddadef89d619ced36494595c289d8213` | 45450 |
| `i3d/Series_7950B.i3d` | `71e848bfd4f963126107dd41e4764a1869d1f28d0e42c365cafd72cdb9d811d3` | 66538 |

## Why the full archive is not committed

The uploaded ZIP identifies the mod author as **Hispano**, but contains no explicit redistribution license or `LICENSE` file. The project repository is public and its donor policy prohibits redistributing third-party donor assets without confirmed rights. Therefore the ZIP, `.i3d.shapes`, textures, sounds, and full donor model files are intentionally **not** committed.

Instead, `V3_REFERENCE_COMPACT.json` contains the project-use engineering facts required to reconstruct and audit the relevant systems later: loading-pipe animation segments, selector states, exact-fill/fill-volume structure, relevant i3dMappings, resolved scene-node paths/static transforms, and conveyor hydraulic references.

## Important recovered V3 facts

The uploaded build's `loadingPipe` selector stops are:

- Tank 1: **0.000**
- Tank 2: **0.104**
- Tank 3: **0.257**
- Tank 4: **0.469**
- Tank 1 is active at animation start.

The primary conveyor hierarchy resolves as:

- `overloadingArm01` -> `0>0|6|0` -> I3D path `0|0|6|0`
- `overloadingArm02` -> `0>0|6|0|0` -> I3D path `0|0|6|0|0`
- `overloadingArm03` -> `0>0|6|0|0|0` -> I3D path `0|0|6|0|0|0`
- `overloadingArm04` -> `0>0|6|0|0|0|0` -> I3D path `0|0|6|0|0|0|0`

Static pivot translations recovered from the I3D:

- Arm 1: `-1.47003 1.56863 -1.22386`
- Arm 2: `-0.173656 0.727869 -3.68031`
- Arm 3: `-0.241337 0.219075 1.66861`
- Arm 4: `0 0.418 -0.045`

The V3 `loadingPipe` animation confirms that the mechanism has more than the first two rotations:

- Arm 1: 100 -> 90 -> 0 degrees about Y.
- Arm 2: -50 -> -33 -> 0 degrees about Y.
- Arm 3: -135 -> -64 -> 0 degrees about Y.
- Arm 4: 21 -> 0 degrees about X, plus downstream translation late in the animation.

This directly supports the V7 decision to solve Tank 1 using downstream/height articulation instead of forcing additional overtravel into Arms 1-2.

Flap mappings in this reference build:

- `tankFlapsBack` -> `0>0|6|2`
- `tankFlapsFront` -> `0>0|6|3`

The V3 flap animation is retained for regression/history only. V7 flap authority remains the separately documented Tanks 1-2 front / Tanks 3-4 rear strategy.

## Future-use files

- `V3_REFERENCE_COMPACT.json` — machine-readable engineering snapshot from this uploaded archive.
- `../TANK1_CONVEYOR_ENGINEERING.md` — current V7 Tank 1 design authority.
- `../../../tools/extract_i3d_animation.py` — reusable extractor for any later Bourgault candidate/donor ZIP.

With these references in Git, this exact V3 archive should not need to be re-uploaded merely to recover its animation hierarchy, selector timing, or relevant node transforms. A later V6/V7 archive is still required if we need the exact transforms unique to those builds.
