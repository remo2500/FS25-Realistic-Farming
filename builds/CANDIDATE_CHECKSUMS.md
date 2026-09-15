# Candidate Build Checksums

_Last updated: 2026-09-15_

Candidate ZIPs are intentionally not stored in this public repository. These checksums identify the exact locally generated test archives associated with the current authority documents.

| Candidate | SHA-256 | Archive file count | Static validation |
|---|---|---:|---|
| Bourgault 3320 / 7950B V6 Engineering | `6072d0f1e805a684bd926aa97fcbcca3d5b7ef5f9429d92c3697d59b26289651` | 62 | 18/18 PASS |
| Seed Hawk 660 3-Tank RS V3 | `d052c302f3a54d0a77273dc02098185223094ca6e7971b5236eb114684edadcb` | 56 | 16/16 PASS |
| Seed Hawk 660 3-Tank RS V2 (superseded test) | `3dcadef65f65add03d000503f6c3b457eb1d8d88875ea5fab9d9d1b61b4a4594` | 56 | superseded by V3 cleanup |

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

The checksum only identifies the archive. Passing the checksum does not replace the in-game promotion tests in `docs/TESTING.md`.
