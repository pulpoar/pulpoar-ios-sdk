# PulpoAR iOS SDK

Native iOS SDK for PulpoAR (face makeup try-on), distributed with Swift Package Manager as pre-built xcframeworks.

## Requirements

- Xcode 26+ for `PulpoTryOnKit` and `PulpoTryOnUI` (built with Swift 6.3); Xcode 16+ for `PulpoModule` alone
- iOS 15.6+ deployment target
- A physical iPhone for camera use. The xcframeworks have an `arm64` device slice and an `x86_64` simulator slice only; there is no `arm64` simulator slice yet.

## Modules

| Product | Import | What it is |
| --- | --- | --- |
| `PulpoTryOnUI` | `import PulpoTryOnUI` | Ready-made try-on screens (camera, catalog, looks), themeable. Includes `PulpoTryOnKit` |
| `PulpoTryOnKit` | `import PulpoTryOnKit` | Try-On SDK without UI: session, camera view, catalog and product application, for your own screens |
| `PulpoModule` | `import PulpoModule` | Face makeup engine used by the Try-On SDK. Linked automatically by the products above; add it on its own only for an existing direct integration |

Add `PulpoTryOnUI` for the full experience, or `PulpoTryOnKit` to build your own UI. More modules (for example skin analysis) will be added as separate products of this same package. You only download and link the ones you add to your target.

## Install

**Xcode:** File → Add Package Dependencies… → enter this repository's URL → pick a version rule (for example "Up to Next Major" from `0.1.0`) → add the product(s) you need (see Modules) to your app target.

**Package.swift:**
```swift
dependencies: [
    .package(url: "https://github.com/pulpoar/pulpoar-ios-sdk", from: "0.1.0")
],
targets: [
    .target(name: "YourApp", dependencies: [
        .product(name: "PulpoTryOnUI", package: "pulpoar-ios-sdk")  // or "PulpoTryOnKit"
    ])
]
```

Then `import PulpoTryOnUI` (or `import PulpoTryOnKit`). Add `NSCameraUsageDescription` to your app's Info.plist if you use the camera.

## Update

Xcode: File → Packages → Update to Latest Package Versions (or `swift package update`). You never need to edit URLs or checksums.

## Releasing (maintainers)

Binaries are hosted on the PulpoAR CDN (`assets.pulpoar.com`), each release under a new path. The **Release** workflow (Actions → Release → Run workflow) takes the version and the new binaries (a Try-On build folder and/or a PulpoModule zip), validates them, updates `Package.swift`, and tags and publishes the release. CI runs the same checks on every pull request.

To add a module, add its `binaryTarget` and library product to `Package.swift` and a row to the Modules table above.

## License

Proprietary. See [LICENSE](LICENSE). Use requires an agreement with PulpoAR.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
