#!/usr/bin/env python3
"""Rebuild Seed Hawk 660 3-Tank RS V3R1 Recovery from the verified uploaded base.

This tool does not redistribute donor assets. Supply the user-owned source ZIP locally.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "c248f1ec41a0c1ae5645f2fa4b61c925653ba3c5e056724a0f1be072f4460ce8"
RECOVERY_VERSION = "1.0.1.0"
RECOVERY_TITLE = "Seed Hawk Pack [3-Tank RS V3R1 Recovery]"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def patch_moddesc(data: bytes) -> bytes:
    text = data.decode("utf-8-sig")
    text = re.sub(r"<version>[^<]+</version>", f"<version>{RECOVERY_VERSION}</version>", text, count=1)
    text = text.replace(
        "<en>Seed Hawk Pack [3-Tank RS Test]</en>",
        f"<en>{RECOVERY_TITLE}</en>",
        1,
    )

    if "<extraSourceFiles>" not in text:
        marker = "    <storeItems>"
        block = (
            "    <extraSourceFiles>\n"
            '        <sourceFile filename="scripts/ThreeTankCompat.lua" />\n'
            "    </extraSourceFiles>\n\n"
        )
        if marker not in text:
            raise RuntimeError("modDesc storeItems marker not found")
        text = text.replace(marker, block + marker, 1)

    old = "Changelog 1.0.0.2:\n- Fixed no conveyor option not filling properly]]>"
    new = (
        "Changelog 1.0.0.2:\n- Fixed no conveyor option not filling properly\n\n"
        "Changelog 1.0.1.0 - 3-Tank RS V3R1 Recovery:\n"
        "- Restored project V3 three-tank seed/fertilizer category architecture\n"
        "- Restored Realistic Seeder/custom seed synchronization across all three tanks\n"
        "- Removed unsupported cart-level sprayer loadInfoIndex attribute\n"
        "- Preserved conveyor selector stops for Tanks 1/2/3 and transport]]>"
    )
    if old in text:
        text = text.replace(old, new, 1)

    return text.encode("utf-8")


def patch_vehicle(data: bytes) -> bytes:
    text = data.decode("utf-8-sig")
    text = text.replace(
        '<sprayer fillUnitIndex="3" unloadInfoIndex="3" loadInfoIndex="3">',
        '<sprayer fillUnitIndex="3" unloadInfoIndex="3">',
        1,
    )
    pattern = re.compile(
        r'(<fillUnit\s+unitTextOverride="\$l10n_unit_literShort"\s+)'
        r'fillTypes="seeds fertilizer"(\s+capacity="(?:5600|10600)")'
    )
    text, count = pattern.subn(
        r'\1fillTypeCategories="seeds fertilizer"\2',
        text,
    )
    if count != 3:
        raise RuntimeError(f"expected three Seed Hawk tank replacements, found {count}")
    return text.encode("utf-8")


def clone_zipinfo(info: zipfile.ZipInfo) -> zipfile.ZipInfo:
    out = zipfile.ZipInfo(info.filename, info.date_time)
    out.compress_type = info.compress_type
    out.comment = info.comment
    out.extra = info.extra
    out.internal_attr = info.internal_attr
    out.external_attr = info.external_attr
    out.create_system = info.create_system
    out.create_version = info.create_version
    out.extract_version = info.extract_version
    out.flag_bits = info.flag_bits
    return out


def add_entry(zf: zipfile.ZipFile, name: str, data: bytes, *, directory: bool = False) -> None:
    info = zipfile.ZipInfo(name, (2026, 9, 18, 8, 0, 0))
    info.create_system = 3
    info.external_attr = ((0o40755 if directory else 0o100644) << 16)
    info.compress_type = zipfile.ZIP_STORED if directory else zipfile.ZIP_DEFLATED
    zf.writestr(info, b"" if directory else data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("output_zip", type=Path)
    parser.add_argument(
        "--compat-script",
        type=Path,
        default=Path("scripts/compatibility/SeedHawk660ThreeTankCompat.lua"),
    )
    parser.add_argument("--allow-unknown-source", action="store_true")
    args = parser.parse_args()

    source_sha = sha256(args.source_zip)
    if source_sha != EXPECTED_SOURCE_SHA256 and not args.allow_unknown_source:
        raise SystemExit(
            f"source SHA-256 mismatch: {source_sha}\n"
            f"expected: {EXPECTED_SOURCE_SHA256}\n"
            "Refusing to patch unknown source; use --allow-unknown-source only for deliberate engineering work."
        )

    compat = args.compat_script.read_bytes()
    if args.output_zip.exists():
        args.output_zip.unlink()

    with zipfile.ZipFile(args.source_zip, "r") as source, zipfile.ZipFile(
        args.output_zip, "w", allowZip64=True
    ) as target:
        for info in source.infolist():
            data = source.read(info.filename)
            if info.filename == "modDesc.xml":
                data = patch_moddesc(data)
            elif info.filename == "seedHawk660AirCart.xml":
                data = patch_vehicle(data)
            target.writestr(clone_zipinfo(info), data)

        add_entry(target, "scripts/", b"", directory=True)
        add_entry(target, "scripts/ThreeTankCompat.lua", compat)

    print(args.output_zip)
    print("SHA-256:", sha256(args.output_zip))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
