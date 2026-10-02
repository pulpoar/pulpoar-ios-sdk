#!/usr/bin/env python3
"""Sanity-check an unzipped <Module>.xcframework before it is published.

Usage: check_xcframework.py <path/to/Module.xcframework> <Module> [Package.swift]

Checks, driven by the xcframework's own Info.plist (no hard-coded slice names):
- no DebugSymbolsPath keys and no dSYM folders
- an iOS device slice with arm64 exists
- every slice has the module's framework binary, containing exactly the declared architectures
- every slice's minimum OS is not newer than the iOS version declared in Package.swift
"""
import plistlib
import re
import subprocess
import sys
from pathlib import Path


def ios_minimum(package_swift: Path) -> tuple:
    m = re.search(r'\.iOS\(\s*"?([0-9]+(?:\.[0-9]+)*)"?\s*\)', package_swift.read_text())
    if not m:
        raise SystemExit(f"error: cannot find .iOS(...) platform in {package_swift}")
    return version(m.group(1))


def version(s: str) -> tuple:
    return tuple(int(p) for p in s.split("."))


def minos(binary: Path) -> tuple:
    out = subprocess.run(["vtool", "-show-build", str(binary)], capture_output=True, text=True, check=True).stdout
    m = re.search(r"\bminos\s+([0-9]+(?:\.[0-9]+)*)", out)
    if not m:
        raise SystemExit(f"error: no minos in vtool output for {binary}")
    return version(m.group(1))


def archs(binary: Path) -> set:
    out = subprocess.run(["lipo", "-archs", str(binary)], capture_output=True, text=True, check=True).stdout
    return set(out.split())


def main() -> int:
    if len(sys.argv) not in (3, 4):
        print(__doc__, file=sys.stderr)
        return 2
    root, module = Path(sys.argv[1]), sys.argv[2]
    limit = ios_minimum(Path(sys.argv[3] if len(sys.argv) == 4 else "Package.swift"))
    errors = []

    info = plistlib.loads((root / "Info.plist").read_bytes())
    libs = info.get("AvailableLibraries", [])
    if any("DebugSymbolsPath" in lib for lib in libs):
        errors.append("Info.plist references DebugSymbolsPath")
    if any(p.is_dir() and p.name.lower().endswith(".dsym") for p in root.rglob("*")):
        errors.append("contains dSYM folders")

    device_arm64 = False
    for lib in libs:
        ident = lib["LibraryIdentifier"]
        platform = lib.get("SupportedPlatform")
        declared = set(lib.get("SupportedArchitectures", []))
        binary = root / ident / lib["LibraryPath"] / module
        if not binary.is_file():
            errors.append(f"{ident}: missing binary {binary.relative_to(root)}")
            continue
        found, mo = archs(binary), minos(binary)
        print(f"{ident}: {platform} {sorted(found)} minos {'.'.join(map(str, mo))}")
        if found != declared:
            errors.append(f"{ident}: binary has {sorted(found)}, Info.plist declares {sorted(declared)}")
        if mo > limit:
            errors.append(f"{ident}: minos {mo} is newer than Package.swift iOS {limit}")
        if platform == "ios" and not lib.get("SupportedPlatformVariant") and "arm64" in found:
            device_arm64 = True
    if not libs:
        errors.append("no slices listed in Info.plist")
    elif not device_arm64:
        errors.append("no iOS device arm64 slice")

    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
