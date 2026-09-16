# Candidate Build Checksums

_Last updated: 2026-09-16_

Candidate ZIPs are intentionally not stored in this public repository. These checksums identify exact locally generated or user-supplied test/reference archives associated with the authority documents.

| Candidate / reference | SHA-256 | ZIP entry count | Static validation / status |
|---|---|---:|---|
| **Bourgault 3320 / 7950B V7 Engineering** | `190b358ed1f21b411a11eb2d4cd0fc1d59f6f6cd293f93f9e7e239b307a17e2d` | 61 | **30/30 donor-aware static engineering checks PASS; TEST READY for first runtime review** |
| Bourgault 3320 / 7950B V6 Engineering | `6072d0f1e805a684bd926aa97fcbcca3d5b7ef5f9429d92c3697d59b26289651` | 62 | 18/18 PASS under historical V6 profile; **HOLD after geometry audit** |
| Bourgault 3320 / 7950B uploaded 4-Tank V3 F-R reference | `30eebabb116e1932a53f25b78feb41c37fdda66260933d05c560302db5f9d69a` | 60 | donor-derived reference captured 2026-09-16; engineering extract stored under `equipment/bourgault_7950/reference/`; **not V7 authority** |
| Seed Hawk 660 3-Tank RS V3 | `d052c302f3a54d0a77273dc02098185223094ca6e7971b5236eb114684edadcb` | 56 | 16/16 PASS |
| Seed Hawk 660 3-Tank RS V2 (superseded test) | `3dcadef65f65add03d000503f6c3b457eb1d8d88875ea5fab9d9d1b61b4a4594` | 56 | superseded by V3 cleanup |

Entry-count detail for the current archives:

- Bourgault V7: **61 ZIP entries**.
- Bourgault V6: **57 regular files + 5 directory entries = 62 ZIP entries**.
- Uploaded Bourgault V3 reference: **60 ZIP entries**.
- Seed Hawk V3: **52 regular files + 4 directory entries = 56 ZIP entries**.

## Bourgault V7 provenance and reproducibility

The V7 candidate is rebuilt locally from the verified user-supplied V3 reference archive rather than storing third-party donor assets in this public repository.

Verified V3 source SHA-256:

`30eebabb116e1932a53f25b78feb41c37fdda66260933d05c560302db5f9d69a`

The rebuild tool is:

`tools/build_bourgault_v7_from_v3.py`

It refuses to patch an unknown source archive by default. The build also assigns deterministic ZIP metadata to the added compatibility Lua file. Two independent rebuilds from the same verified source and compatibility script produced byte-identical V7 ZIPs with SHA-256:

`190b358ed1f21b411a11eb2d4cd0fc1d59f6f6cd293f93f9e7e239b307a17e2d`

The 30/30 donor-aware static pass covers archive/XML integrity, capacities/categories, exact-fill roots, five physical fill-volume mappings, load/unload nodes, selector states, compatibility behavior, flap state at each selector stop, exact-root exclusivity, all four calculated pipe positions, and confirmation that V7 introduces no new I3D `nodeId` collisions beyond the donor's existing TransformGroup/UserAttribute pairing convention.

The uploaded Bourgault V3 archive identifies the author as **Hispano** and contains no explicit redistribution license. The full V3/V7 donor-derived archives are therefore not committed to this public repository; only hashes, rebuild instructions, project-authored scripts, and donor-safe derived engineering reference data are stored.

## Verification

Windows PowerShell:

```powershell
Get-FileHash .\FS25_Bourgault_3320_4Tank_V7_Engineering.zip -Algorithm SHA256
Get-FileHash .\FS25_Bourgault_3320_4Tank_V6_Engineering.zip -Algorithm SHA256
Get-FileHash .\FS25_Bourgault_Series_3320.zip -Algorithm SHA256
Get-FileHash .\FS25_SeedHawkPack_3Tank_RS_V3.zip -Algorithm SHA256
```

Linux/macOS:

```bash
sha256sum FS25_Bourgault_3320_4Tank_V7_Engineering.zip
sha256sum FS25_Bourgault_3320_4Tank_V6_Engineering.zip
sha256sum FS25_Bourgault_Series_3320.zip
sha256sum FS25_SeedHawkPack_3Tank_RS_V3.zip
```

The checksum only identifies an archive. A matching checksum and a static validator pass do not replace the engineering and in-game promotion tests in `docs/TESTING.md`.
