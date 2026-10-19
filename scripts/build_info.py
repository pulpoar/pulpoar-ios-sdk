#!/usr/bin/env python3
"""Read the build-info.json that ships with SDK binaries built from source (Try-On: PulpoTryOnKit and PulpoTryOnUI).

Such builds are uploaded together to one folder under BUILD_PREFIX, with a build-info.json listing each zip's checksum
and the PulpoModule binary they were built against.

  build_info.py plan <folder_url> <version>
      Prints "<Module> <zip_url> <checksum>" for each binary of the build, after checking that it is for <version>.

  build_info.py check [Package.swift]
      For every binaryTarget whose url is under BUILD_PREFIX: its folder's build-info.json must list it with the same
      checksum, every binary that build lists must be in Package.swift from that same folder (a Kit and a UI from
      different builds don't fit together), and Package.swift's PulpoModule must be the one the build used.
"""
import json
import re
import sys
import time
import urllib.request

BUILD_PREFIX = "https://assets.pulpoar.com/vision/pulpo-sdk/"
SAFE_URL = re.compile(r"[A-Za-z0-9._:/\-]+")
MODULE = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
CHECKSUM = re.compile(r"[0-9a-f]{64}")
VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")
TARGET = re.compile(r'\.binaryTarget\(\s*name:\s*"([^"]+)",\s*url:\s*"([^"]+)",\s*checksum:\s*"([^"]+)"')


def folder(url: str) -> str:
    """A build folder URL, normalized to end in '/'."""
    url = url if url.endswith("/") else url + "/"
    if not url.startswith(BUILD_PREFIX) or not SAFE_URL.fullmatch(url) or "/../" in url or "/./" in url:
        raise ValueError(f"build folder must be under {BUILD_PREFIX} and contain only [A-Za-z0-9._:/-]: {url!r}")
    return url


def binaries(info: dict) -> dict:
    """{module: (file, checksum)} from a build-info.json, validated."""
    if info.get("schema") != 1:
        raise ValueError(f"unsupported build-info.json schema {info.get('schema')!r}")
    modules = info.get("modules")
    if not isinstance(modules, dict) or not modules:
        raise ValueError("build-info.json lists no modules")
    result = {}
    for module, entry in modules.items():
        file, checksum = entry.get("file"), entry.get("checksum")
        if not MODULE.fullmatch(module) or file != f"{module}.xcframework.zip" or not CHECKSUM.fullmatch(checksum or ""):
            raise ValueError(f"build-info.json: invalid entry for {module!r}: {entry!r}")
        result[module] = (file, checksum)
    return result


def engine(info: dict) -> tuple:
    entry = info.get("engine") or {}
    module, checksum = entry.get("module"), entry.get("checksum")
    if not MODULE.fullmatch(module or "") or not CHECKSUM.fullmatch(checksum or ""):
        raise ValueError(f"build-info.json: invalid engine entry {entry!r}")
    return module, checksum


def plan(info: dict, base: str, version: str) -> list:
    if not VERSION.fullmatch(version):
        raise ValueError(f"version must look like 1.2.3, got {version!r}")
    if info.get("version") != version:
        raise ValueError(f"build-info.json is for version {info.get('version')!r}, not {version}")
    engine(info)
    return [(module, base + file, checksum) for module, (file, checksum) in sorted(binaries(info).items())]


def targets(manifest: str) -> dict:
    """{name: (url, checksum)} for every binaryTarget in a Package.swift."""
    found = {}
    for name, url, checksum in TARGET.findall(manifest):
        if name in found:
            raise ValueError(f"binaryTarget {name!r} appears twice in Package.swift")
        found[name] = (url, checksum)
    return found


def check(manifest: str, fetch) -> list:
    """Problems with the built-from-source binaries in a Package.swift; fetch(url) returns a build-info.json dict."""
    declared = targets(manifest)
    folders = sorted({url.rsplit("/", 1)[0] + "/" for url, _ in declared.values() if url.startswith(BUILD_PREFIX)})
    problems = []
    for base in folders:
        info = fetch(folder(base) + "build-info.json")
        listed = binaries(info)
        for name, (url, _) in sorted(declared.items()):
            if url.startswith(base) and "/" not in url[len(base):] and name not in listed:
                problems.append(f"{name}: {base} is a build of {sorted(listed)}, not of {name}")
        for module, (file, checksum) in sorted(listed.items()):
            if module not in declared:
                problems.append(f"{module} is part of the build at {base} but not in Package.swift")
            elif declared[module] != (base + file, checksum):
                problems.append(f"{module} must come from the build at {base} ({base + file}, {checksum}) "
                                f"with the other modules of that build; Package.swift has {declared[module]}")
        engine_module, engine_checksum = engine(info)
        if engine_module not in declared:
            problems.append(f"the build at {base} needs {engine_module}, which is not in Package.swift")
        elif declared[engine_module][1] != engine_checksum:
            problems.append(f"the build at {base} was built against {engine_module} with checksum {engine_checksum}; "
                            f"Package.swift has {declared[engine_module][1]}. Rebuild it against this {engine_module}")
    return problems


def fetch_json(url: str) -> dict:
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                return json.load(response)
        except OSError as e:
            if attempt == 2:
                raise ValueError(f"cannot fetch {url}: {e}") from e
            time.sleep(5 * (attempt + 1))


def main() -> int:
    args = sys.argv[1:]
    try:
        if len(args) == 3 and args[0] == "plan":
            base = folder(args[1])
            for module, url, checksum in plan(fetch_json(base + "build-info.json"), base, args[2]):
                print(module, url, checksum)
            return 0
        if len(args) in (1, 2) and args[0] == "check":
            with open(args[1] if len(args) == 2 else "Package.swift") as f:
                problems = check(f.read(), fetch_json)
            for problem in problems:
                print(f"error: {problem}", file=sys.stderr)
            return 1 if problems else 0
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
