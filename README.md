# PulpoAR iOS SDK

Native iOS SDK for PulpoAR (face makeup try-on), distributed with Swift Package Manager as a pre-built xcframework.

## Requirements

- Xcode 16+
- iOS 18.4+ deployment target
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

One shared version tag covers the whole package; releasing any module bumps it. Run once per module.

1. Build the module's xcframework and remove debug symbols: no `dSYMs/` folders, and no `DebugSymbolsPath` keys in `<Module>.xcframework/Info.plist` (Xcode fails the build if they point at missing folders).
2. Zip it so `<Module>.xcframework` is the top-level entry, without macOS metadata:
   ```
   COPYFILE_DISABLE=1 ditto -c -k --norsrc --noextattr --noqtn --keepParent <Module>.xcframework <Module>.xcframework.zip
   ```
3. Upload to the `vision` blob container under a **new, never reused** path, ending in `/<Module>.xcframework.zip` (for example `pulpo-module/builds/NativePulpoModule_v<version>/ios/PulpoModule.xcframework.zip`). The CDN caches for 30 days, so overwriting a path serves stale files.
4. Run the **Release** workflow (Actions → Release → Run workflow) with the module, the new SDK version and the zip URL. It validates the zip (layout, no debug symbols, every slice's architectures, minimum iOS no newer than `Package.swift`, an arm64 device slice), updates that module's `url` and `checksum` in `Package.swift`, checks that SwiftPM resolves it, then commits, tags `<version>` and creates a GitHub release.

### Adding a new module
Add a library product and `binaryTarget` to `Package.swift`, add the name to the `module` options in `.github/workflows/release.yml`, add a row to the Modules table above, then release it as above.

CI (`.github/workflows/ci.yml`) runs the script tests and resolves every binary on each PR.

## License

Proprietary. See [LICENSE](LICENSE). Use requires an agreement with PulpoAR.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
