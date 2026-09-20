# Patch and Rebuild Policy

This repository does not store complete third-party donor mods unless redistribution rights are explicitly confirmed.

Instead, each equipment workstream should be reproducible from:

1. A legally obtained local donor mod.
2. The equipment `PATCH_SPEC.md` in this repository.
3. Project-owned compatibility scripts under `scripts/compatibility/`.
4. Project validation tools under `tools/`.
5. Candidate checksums under `builds/`.

## Current equipment patch specs

- `equipment/bourgault_7950/PATCH_SPEC.md`
- `equipment/seedhawk_660/PATCH_SPEC.md`

## What may be committed here

Appropriate project-owned material includes:

- Lua compatibility code written for this project.
- Coordinate tables and geometry measurements.
- XML change specifications.
- Small patch/diff files where useful for review.
- Build scripts that operate on a locally supplied donor.
- Static validation tools.
- Test reports and checksums.

Do not commit complete donor ZIPs, extracted donor texture/model trees, or savegames simply to make a build reproducible.

## Version discipline

Every test archive should have a distinct candidate version. When a patch changes behavior, update:

- the equipment patch specification,
- `docs/CURRENT_AUTHORITY.md`,
- `docs/COMPATIBILITY_MATRIX.md` if compatibility status changes,
- `builds/CANDIDATE_CHECKSUMS.md`, and
- the mod's own version/changelog.

Do not silently replace a previously distributed test ZIP with different contents under the same version name.

Bourgault V6 is retained as a historical candidate and is on HOLD. V7 must be generated as a separate archive after applying the corrected flap animation and V7 compatibility bridge.

## Static validation

Current profiles:

```bash
python tools/validate_candidate.py <zip> --profile bourgault7950-v6
python tools/validate_candidate.py <zip> --profile bourgault7950-v7
python tools/validate_candidate.py <zip> --profile seedhawk660-v3
```

The V6 profile exists for historical archive verification. The V7 profile adds compatibility hardening and load/unload-node position checks. Exact flap animation timing remains a separate mandatory engineering review until a robust I3D animation sampler is added.

Static validation confirms only the invariants it actually checks. It never overrides a known geometry defect or replaces in-game tests.
