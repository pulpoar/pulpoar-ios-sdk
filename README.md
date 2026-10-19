# PulpoAR iOS SDK

Native iOS SDK for PulpoAR (face makeup try-on), distributed with Swift Package Manager as a pre-built xcframework.

## Requirements

- Xcode 16+
- iOS 15.6+ deployment target
- A physical iPhone for camera use. The xcframework has an `arm64` device slice and an `x86_64` simulator slice only; there is no `arm64` simulator slice yet.

## Modules

| Product | Import | What it is |
| --- | --- | --- |
| `PulpoModule` | `import PulpoModule` | Face makeup try-on |

More modules (for example skin analysis) will be added as separate products of this same package. You only download and link the ones you add to your target.

## Install

**Xcode:** File → Add Package Dependencies… → enter this repository's URL → pick a version rule (for example "Up to Next Major" from `0.0.24`) → add the product(s) you need (see Modules) to your app target.

**Package.swift:**
```swift
dependencies: [
    .package(url: "https://github.com/pulpoar/pulpoar-ios-sdk", from: "0.0.24")
],
targets: [
    .target(name: "YourApp", dependencies: [
        .product(name: "PulpoModule", package: "pulpoar-ios-sdk")
    ])
]
```

Then `import PulpoModule`. Add `NSCameraUsageDescription` to your app's Info.plist if you use the camera.

## Update

Xcode: File → Packages → Update to Latest Package Versions (or `swift package update`). You never need to edit URLs or checksums.

## Releasing (maintainers)

One shared version tag covers the whole package. Binaries are uploaded to the `vision` blob container (served at `https://assets.pulpoar.com/vision/`) under a **new, never reused** path: the CDN caches for 30 days, so overwriting a path serves stale files. Then the **Release** workflow (Actions → Release → Run workflow) makes them installable. For each binary it validates the zip (layout, no debug symbols, every slice's architectures, minimum iOS no newer than `Package.swift`, an arm64 device slice, a valid signature if signed), updates its `url` and `checksum` in `Package.swift`, checks that SwiftPM resolves the package, then commits, tags `<version>` and creates a GitHub release.

**Try-On SDK (`PulpoTryOnKit`, `PulpoTryOnUI`):** built and uploaded by the *iOS Try-On Release* workflow of the private source repository, to `https://assets.pulpoar.com/vision/pulpo-sdk/ios/tryon/<version>/`, together with a `build-info.json`. Run Release with that version and that folder as the Try-On build URL; the source workflow's summary prints the command. Release requires the build to be for that version, the downloaded zips to match `build-info.json`, and the `PulpoModule` in `Package.swift` to be the one the Kit was built against (`scripts/build_info.py`). A new engine therefore reaches partners with a Kit rebuilt against it.

**Engine (`PulpoModule`):**
1. Build the xcframework and remove debug symbols: no `dSYMs/` folders, and no `DebugSymbolsPath` keys in `PulpoModule.xcframework/Info.plist` (Xcode fails the build if they point at missing folders).
2. Zip it so `PulpoModule.xcframework` is the top-level entry, without macOS metadata:
   ```
   COPYFILE_DISABLE=1 ditto -c -k --norsrc --noextattr --noqtn --keepParent PulpoModule.xcframework PulpoModule.xcframework.zip
   ```
3. Upload it to a new folder, for example `pulpo-module/builds/NativePulpoModule_v<version>/ios/PulpoModule.xcframework.zip`.
4. Run Release with the new SDK version and the zip URL as the PulpoModule zip URL.

### Adding a new module
Add a `binaryTarget` and a library product to `Package.swift` (the product lists every binary the module needs at runtime), add a row to the Modules table above, then release it as above. A module built from source with a `build-info.json` needs a release input like the Try-On one in `.github/workflows/release.yml`.

CI (`.github/workflows/ci.yml`) runs the script tests, resolves every binary and checks that binaries built from source fit together, on each PR.

## License

Proprietary. See [LICENSE](LICENSE). Use requires an agreement with PulpoAR.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
