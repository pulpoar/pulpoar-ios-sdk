# PulpoAR iOS SDK

Native iOS SDK for PulpoAR (face makeup try-on), distributed with Swift Package Manager as a pre-built xcframework.

## Requirements

- Xcode 16+
- iOS 18.4+ deployment target
- A physical iPhone for camera use. The xcframework has an `arm64` device slice and an `x86_64` simulator slice only; there is no `arm64` simulator slice yet.

## Install

**Xcode:** File → Add Package Dependencies… → enter this repository's URL → pick a version rule (for example "Up to Next Major" from `0.0.24`) → add the **PulpoModule** product to your app target.

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

1. Build the xcframework and remove debug symbols: no `dSYMs/` folders, and no `DebugSymbolsPath` keys in `PulpoModule.xcframework/Info.plist` (Xcode fails the build if they point at missing folders).
2. Zip it so `PulpoModule.xcframework` is the top-level entry, without macOS metadata:
   ```
   COPYFILE_DISABLE=1 ditto -c -k --norsrc --noextattr --noqtn --keepParent PulpoModule.xcframework PulpoModule.xcframework.zip
   ```
3. Upload to the `vision` blob container under a **new, never reused** path: `pulpo-module/builds/NativePulpoModule_v<version>/ios/PulpoModule.xcframework.zip`. The CDN caches for 30 days, so overwriting a path serves stale files.
4. Run the **Release** workflow (Actions → Release → Run workflow) with the version and the zip URL. It validates the zip, updates `Package.swift`, commits, tags `<version>`, and creates a GitHub release.
