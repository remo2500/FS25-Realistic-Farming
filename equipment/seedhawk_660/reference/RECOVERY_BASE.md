# Seed Hawk 660 V3R1 Recovery Reference

_Captured: 2026-09-18_

This directory records the donor-safe identity and recovery path for the user-supplied Seed Hawk archive used to restore the current three-tank test candidate.

## Uploaded recovery base

Archive: `FS25_SeedHawkPack.zip`

SHA-256:

`c248f1ec41a0c1ae5645f2fa4b61c925653ba3c5e056724a0f1be072f4460ce8`

ZIP structure: **54 entries = 51 files + 3 directories**.

Relevant file hashes:

| File | SHA-256 | Bytes |
|---|---|---:|
| `modDesc.xml` | `657edf7e858f30ee92ad788fd5a97b7d01033ab0a2bfbb6a807a0fe408223ae9` | 5,028 |
| `seedHawk660AirCart.xml` | `97927f2b6b556eeef4390bec566662dadaefa48f88d38f52e0683729a5aee54d` | 42,948 |
| `seedHawk660AirCart.i3d` | `3e7500c95621263215feb128cbe348b67a3bef3aff3e70676f3e04297b285be6` | 36,488 |

The uploaded base already contains the three physical compartments, middle exact-fill root, independent fill-volume meshes, and the accepted conveyor selector stops. It does **not** contain the project compatibility script and still uses literal `fillTypes="seeds fertilizer"` plus the superseded cart-level `loadInfoIndex` attribute.

## Historical V3 versus recovery V3R1

The historical V3 archive remains identified by SHA-256:

`d052c302f3a54d0a77273dc02098185223094ca6e7971b5236eb114684edadcb`

Those exact bytes are no longer available. The project therefore does **not** silently regenerate a different archive under the historical V3 identity.

The recovered candidate is versioned separately as:

`FS25_SeedHawkPack_3Tank_RS_V3R1_Recovery.zip`

SHA-256:

`ffc66a36e95815dcdde54973c02db6dcf28e7d0621b29b96bbc2b3f33b968a14`

ZIP structure: **56 entries = 52 files + 4 directories**.

Static recovery audit: **21/21 PASS**. This includes the original 16 Seed Hawk V3 checks plus script registration, distinct recovery versioning, independent three-volume mapping, No Conveyor all-three-tank coverage, and required physical I3D-node presence.

## Rebuild

Use:

```bash
python tools/build_seedhawk_v3r1_from_recovery_base.py \
  FS25_SeedHawkPack.zip \
  FS25_SeedHawkPack_3Tank_RS_V3R1_Recovery.zip
```

The tool refuses an unknown source SHA by default and uses the project-owned compatibility source:

`scripts/compatibility/SeedHawk660ThreeTankCompat.lua`

Two independent local rebuilds from the verified source produced byte-identical output.

## Donor policy

The full uploaded ZIP and donor model assets are intentionally not committed to the public repository. This reference stores hashes, rebuild instructions, and project-authored recovery logic only.
