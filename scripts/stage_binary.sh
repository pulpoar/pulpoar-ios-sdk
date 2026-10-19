#!/bin/bash
# Downloads one <Module>.xcframework.zip, validates it and points the module's binaryTarget in Package.swift at it.
# Used by .github/workflows/release.yml, once per binary being released. Run from the repository root.
#
# Usage: stage_binary.sh <Module> <zip_url> [expected_checksum]
#   expected_checksum: the checksum the build recorded (build-info.json); the download must match it.
set -euo pipefail

module=${1:?usage: stage_binary.sh <Module> <zip_url> [expected_checksum]}
url=${2:?usage: stage_binary.sh <Module> <zip_url> [expected_checksum]}
expected=${3:-}
scripts=$(cd "$(dirname "$0")" && pwd)
zip="$module.xcframework.zip"
unzipped="unzipped/$module"

[[ "$module" =~ ^[A-Za-z][A-Za-z0-9_]*$ ]] || { echo "error: invalid module name $module"; exit 1; }
[[ "$url" == https://assets.pulpoar.com/vision/*/"$zip" ]] || { echo "error: zip url must be under https://assets.pulpoar.com/vision/ and end in /$zip"; exit 1; }
[[ "$url" =~ ^[A-Za-z0-9._:/-]+$ ]] || { echo "error: zip url contains unsupported characters"; exit 1; }

echo "::group::$module"
rm -rf "$zip" "$unzipped"
curl -fsSL --retry 3 --max-time 300 "$url" -o "$zip"
checksum=$(swift package compute-checksum "$zip")
if [[ -n "$expected" && "$checksum" != "$expected" ]]; then
    echo "error: $url has checksum $checksum, its build recorded $expected"; exit 1
fi
if unzip -l "$zip" | grep -qiE "dSYM|__MACOSX|\.DS_Store"; then
    echo "error: $zip contains dSYMs or macOS metadata"; exit 1
fi
mkdir -p "$unzipped"
unzip -q "$zip" -d "$unzipped"
[[ -d "$unzipped/$module.xcframework" ]] || { echo "error: $module.xcframework must be the zip's top-level entry"; exit 1; }
python3 "$scripts/check_xcframework.py" "$unzipped/$module.xcframework" "$module"
python3 "$scripts/update_manifest.py" "$module" "$url" "$checksum"
echo "$module: $url ($checksum)"
echo "::endgroup::"
