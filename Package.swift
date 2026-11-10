// swift-tools-version:5.7
import PackageDescription

// PulpoAR iOS SDK, distributed as pre-built binaries (xcframeworks).
// One library product per module, each backed by one binaryTarget. Partners add this package once and
// pick only the product(s) they need; SwiftPM downloads only the binaries of the products they link.
// `url` and `checksum` are rewritten by .github/workflows/release.yml (scripts/update_manifest.py),
// so keep each binaryTarget as `name`, `url`, `checksum` on separate lines. Partners never edit this file.
//
// Adding a module: add a binaryTarget here (url/checksum of its first zip) and a library product listing every
// binaryTarget it needs at runtime (a binaryTarget can't declare dependencies of its own), then document it in
// README.md and, if it needs a new kind of release input, in release.yml.
let package = Package(
    name: "PulpoAR",
    platforms: [.iOS("15.6")],
    products: [
        .library(name: "PulpoModule", targets: ["PulpoModule"]),
        .library(name: "PulpoTryOnKit", targets: ["PulpoTryOnKit", "PulpoModule"]),
        .library(name: "PulpoTryOnUI", targets: ["PulpoTryOnUI", "PulpoTryOnKit", "PulpoModule"])
    ],
    targets: [
        .binaryTarget(
            name: "PulpoModule",
            url: "https://assets.pulpoar.com/vision/pulpo-module/builds/NativePulpoModule_v0.0.29/ios/PulpoModule.xcframework.zip",
            checksum: "537cc247b34cd283072b45d73c5f493a5f3482db3151d54bade6b38566a72904"
        ),
        .binaryTarget(
            name: "PulpoTryOnKit",
            url: "https://assets.pulpoar.com/vision/pulpo-sdk/ios/tryon/0.2.0/PulpoTryOnKit.xcframework.zip",
            checksum: "053f160326ffe211b0027d2b25bb2a1605e99f8b0419c836aa6b95108b32713a"
        ),
        .binaryTarget(
            name: "PulpoTryOnUI",
            url: "https://assets.pulpoar.com/vision/pulpo-sdk/ios/tryon/0.2.0/PulpoTryOnUI.xcframework.zip",
            checksum: "dd9176e6ad18c287ff471e22d4f268aaf587bb1294c05ce3c363455fc6ed759c"
        )
    ]
)
