# Candidate Build Checksums

_Last updated: 2026-09-15_

Candidate ZIPs are intentionally not stored in this public repository. These checksums identify the exact locally generated test archives associated with the authority documents.

| Candidate | SHA-256 | ZIP entry count | Static validation |
|---|---|---:|---|
| Bourgault 3320 / 7950B V6 Engineering | `6072d0f1e805a684bd926aa97fcbcca3d5b7ef5f9429d92c3697d59b26289651` | 62 | 18/18 PASS under historical V6 profile; **HOLD after geometry audit** |
| Seed Hawk 660 3-Tank RS V3 | `d052c302f3a54d0a77273dc02098185223094ca6e7971b5236eb114684edadcb` | 56 | 16/16 PASS |
| Seed Hawk 660 3-Tank RS V2 (superseded test) | `3dcadef65f65add03d000503f6c3b457eb1d8d88875ea5fab9d9d1b61b4a4594` | 56 | superseded by V3 cleanup |

Entry-count detail for the current archives:

- Bourgault V6: **57 regular files + 5 directory entries = 62 ZIP entries**.
- Seed Hawk V3: **52 regular files + 4 directory entries = 56 ZIP entries**.

No V7 checksum is recorded yet because a V7 donor-derived archive has not been generated. Do not reuse the V6 filename or checksum for V7.

## Verification

Windows PowerShell:

```powershell
Get-FileHash .\FS25_Bourgault_3320_4Tank_V6_Engineering.zip -Algorithm SHA256
Get-FileHash .\FS25_SeedHawkPack_3Tank_RS_V3.zip -Algorithm SHA256
```

Linux/macOS:

```bash
sha256sum FS25_Bourgault_3320_4Tank_V6_Engineering.zip
sha256sum FS25_SeedHawkPack_3Tank_RS_V3.zip
```

The checksum only identifies an archive. A matching checksum and a static validator pass do not replace the engineering and in-game promotion tests in `docs/TESTING.md`.
