# Candidate Build Checksums

_Last updated: 2026-09-16_

Candidate ZIPs are intentionally not stored in this public repository. These checksums identify exact locally generated or user-supplied test/reference archives associated with the authority documents.

| Candidate / reference | SHA-256 | ZIP entry count | Static validation / status |
|---|---|---:|---|
| Bourgault 3320 / 7950B V6 Engineering | `6072d0f1e805a684bd926aa97fcbcca3d5b7ef5f9429d92c3697d59b26289651` | 62 | 18/18 PASS under historical V6 profile; **HOLD after geometry audit** |
| Bourgault 3320 / 7950B uploaded 4-Tank V3 F-R reference | `30eebabb116e1932a53f25b78feb41c37fdda66260933d05c560302db5f9d69a` | 60 | donor-derived reference captured 2026-09-16; engineering extract stored under `equipment/bourgault_7950/reference/`; **not V7 authority** |
| Seed Hawk 660 3-Tank RS V3 | `d052c302f3a54d0a77273dc02098185223094ca6e7971b5236eb114684edadcb` | 56 | 16/16 PASS |
| Seed Hawk 660 3-Tank RS V2 (superseded test) | `3dcadef65f65add03d000503f6c3b457eb1d8d88875ea5fab9d9d1b61b4a4594` | 56 | superseded by V3 cleanup |

Entry-count detail for the current archives:

- Bourgault V6: **57 regular files + 5 directory entries = 62 ZIP entries**.
- Uploaded Bourgault V3 reference: **60 ZIP entries**.
- Seed Hawk V3: **52 regular files + 4 directory entries = 56 ZIP entries**.

The uploaded Bourgault V3 archive identifies the author as **Hispano** and contains no explicit redistribution license. The full archive is therefore not committed to this public repository; only hashes and donor-safe derived engineering reference data are stored.

No V7 checksum is recorded yet because a V7 donor-derived archive has not been generated. Do not reuse the V6 or V3 filename/checksum for V7.

## Verification

Windows PowerShell:

```powershell
Get-FileHash .\FS25_Bourgault_3320_4Tank_V6_Engineering.zip -Algorithm SHA256
Get-FileHash .\FS25_Bourgault_Series_3320.zip -Algorithm SHA256
Get-FileHash .\FS25_SeedHawkPack_3Tank_RS_V3.zip -Algorithm SHA256
```

Linux/macOS:

```bash
sha256sum FS25_Bourgault_3320_4Tank_V6_Engineering.zip
sha256sum FS25_Bourgault_Series_3320.zip
sha256sum FS25_SeedHawkPack_3Tank_RS_V3.zip
```

The checksum only identifies an archive. A matching checksum and a static validator pass do not replace the engineering and in-game promotion tests in `docs/TESTING.md`.
