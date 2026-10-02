#!/usr/bin/env python3
"""Set the url and checksum of one binaryTarget in Package.swift.

Usage: update_manifest.py <Module> <zip_url> <checksum> [Package.swift]

Fails (without writing) unless exactly one `.binaryTarget(name: "<Module>", ...)` block exists.
"""
import re
import sys

URL_PREFIX = "https://assets.pulpoar.com/vision/pulpo-module/builds/"


def update(source: str, module: str, url: str, checksum: str) -> str:
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", module):
        raise ValueError(f"invalid module name: {module!r}")
    if not url.startswith(URL_PREFIX) or not re.fullmatch(r"[A-Za-z0-9._:/\-]+", url):
        raise ValueError(f"url must be under {URL_PREFIX} and contain only [A-Za-z0-9._:/-]")
    if not re.fullmatch(r"[0-9a-f]{64}", checksum):
        raise ValueError("checksum must be 64 lowercase hex characters")

    pattern = re.compile(
        r'(\.binaryTarget\(\s*name:\s*"' + re.escape(module) + r'",\s*url:\s*")[^"]*("\s*,\s*checksum:\s*")[^"]*(")'
    )
    result, count = pattern.subn(lambda m: m.group(1) + url + m.group(2) + checksum + m.group(3), source)
    if count != 1:
        raise ValueError(f"expected exactly one binaryTarget named {module!r} in Package.swift, found {count}")
    return result


def main() -> int:
    if len(sys.argv) not in (4, 5):
        print(__doc__, file=sys.stderr)
        return 2
    module, url, checksum = sys.argv[1:4]
    path = sys.argv[4] if len(sys.argv) == 5 else "Package.swift"
    try:
        with open(path) as f:
            updated = update(f.read(), module, url, checksum)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    with open(path, "w") as f:
        f.write(updated)
    return 0


if __name__ == "__main__":
    sys.exit(main())
