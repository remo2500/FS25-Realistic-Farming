# Candidate Build Checksums

_Last updated: 2026-09-20_

Candidate ZIPs are intentionally not stored in this public repository. These checksums identify exact locally generated or user-supplied test/reference archives associated with the authority documents.

| Candidate / reference | SHA-256 | ZIP entry count | Static validation / status |
|---|---|---:|---|
| **Bourgault 3320 / 7950B V7 Engineering** | `190b358ed1f21b411a11eb2d4cd0fc1d59f6f6cd293f93f9e7e239b307a17e2d` | 61 | **30/30 donor-aware static engineering checks PASS; TEST READY** |
| Bourgault 3320 / 7950B V6 Engineering | `6072d0f1e805a684bd926aa97fcbcca3d5b7ef5f9429d92c3697d59b26289651` | 62 | historical 18/18 PASS; **HOLD after geometry audit** |
| Bourgault uploaded 4-Tank V3 F-R reference | `30eebabb116e1932a53f25b78feb41c37fdda66260933d05c560302db5f9d69a` | 60 | donor-derived reference; not V7 authority |
| **Seed Hawk 660 3-Tank RS V3R2 Seed Fix** | `4b0306184f18750b82828598b02ebadbee847bb158c69c627899682d47ff63bc` | 56 | **26/26 seed-fix checks PASS; TEST READY** |
| Seed Hawk 660 V3R1 Recovery | `ffc66a36e95815dcdde54973c02db6dcf28e7d0621b29b96bbc2b3f33b968a14` | 56 | 21/21 static PASS, but **HOLD/superseded after runtime seed rejection** |
| Seed Hawk 660 historical V3 | `d052c302f3a54d0a77273dc02098185223094ca6e7971b5236eb114684edadcb` | 56 | historical 16/16 PASS; exact archive bytes currently unavailable |
| Seed Hawk 660 V2 | `3dcadef65f65add03d000503f6c3b457eb1d8d88875ea5fab9d9d1b61b4a4594` | 56 | superseded |

## Seed Hawk V3R2 regression authority

Runtime testing on V3R1 showed that generic seed was rejected by all three tanks. The root cause was traced to two static assumptions:

1. V3R1 changed the donor-proven XML from `fillTypes="seeds fertilizer"` to `fillTypeCategories="seeds fertilizer"`. FS25 resolves those attributes through different manager paths; registered category names are not interchangeable with fill-type names.
2. The V3R1 Lua helper treated GIANTS list-style results as boolean sets, so category lookup results were not copied by actual fill-type index.

V3R2 restores explicit `SEEDS`/`FERTILIZER` base authority in XML and hardens the Lua list/set bridge. Runtime evidence now overrides the earlier V3R1 static PASS.

Verified Seed Hawk recovery-base SHA-256:

`c248f1ec41a0c1ae5645f2fa4b61c925653ba3c5e056724a0f1be072f4460ce8`

Current V3R2 rebuild tool:

`tools/build_seedhawk_v3r2_seedfix.py`

Historical V3R1 reproducibility is preserved by:

- `tools/build_seedhawk_v3r1_from_recovery_base.py`
- `scripts/compatibility/archive/SeedHawk660ThreeTankCompat_V3R1.lua`

## Verification

Windows PowerShell:

```powershell
Get-FileHash .\FS25_Bourgault_3320_4Tank_V7_Engineering.zip -Algorithm SHA256
Get-FileHash .\FS25_SeedHawkPack_3Tank_RS_V3R2_SeedFix.zip -Algorithm SHA256
Get-FileHash .\FS25_SeedHawkPack.zip -Algorithm SHA256
```

Linux/macOS:

```bash
sha256sum FS25_Bourgault_3320_4Tank_V7_Engineering.zip
sha256sum FS25_SeedHawkPack_3Tank_RS_V3R2_SeedFix.zip
sha256sum FS25_SeedHawkPack.zip
```

A matching checksum and static validator pass do not replace the runtime promotion protocol in `docs/TESTING.md`.
