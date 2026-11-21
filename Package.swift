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
        .library(name: "PulpoTryOnUI", targets: ["PulpoTryOnUI", "PulpoTryOnKit", "PulpoModule"]),
        .library(name: "PulpoSkinAIKit", targets: ["PulpoSkinAIKit", "PulpoSkinAI"])
    ],
    targets: [
        .binaryTarget(
            name: "PulpoModule",
            url: "https://assets.pulpoar.com/vision/pulpo-module/builds/NativePulpoModule_v0.0.32/ios/PulpoModule.xcframework.zip",
            checksum: "9ba379bf2ac95bd31df51ab1f883250b8156e615b5f9cdd5b146341e4219431d"
        ),
        .binaryTarget(
            name: "PulpoTryOnKit",
            url: "https://assets.pulpoar.com/vision/pulpo-sdk/ios/tryon/0.3.0/PulpoTryOnKit.xcframework.zip",
            checksum: "278c465095f778bcc3a2d93c357ff1f059412af2d321389e2b3231bf2ed0a18f"
        ),
        .binaryTarget(
            name: "PulpoTryOnUI",
            url: "https://assets.pulpoar.com/vision/pulpo-sdk/ios/tryon/0.3.0/PulpoTryOnUI.xcframework.zip",
            checksum: "ce622dca1f40525a4a958642aa0b8265b2b0db3e5bb6dd355d3f535c9a55de2b"
        ),
        .binaryTarget(
            name: "PulpoSkinAI",
            url: "https://assets.pulpoar.com/vision/pulpo-skinai/builds/NativePulpoSkinAI_v0.1.0/ios/PulpoSkinAI.xcframework.zip",
            checksum: "e8a31e3487323a58f92e0b44c66a239339279cdcbab7eafdeef8722c72e4c229"
        ),
        .binaryTarget(
            name: "PulpoSkinAIKit",
            url: "https://assets.pulpoar.com/vision/pulpo-sdk/ios/skinai/0.3.0/PulpoSkinAIKit.xcframework.zip",
            checksum: "0850d3b095a37dd6acd473312bbaf0ec36d25f6b9c24dbf03d5f1deb8bb7de06"
        )
    ]
)
