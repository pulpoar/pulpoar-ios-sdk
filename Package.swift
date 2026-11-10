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
            url: "https://assets.pulpoar.com/vision/pulpo-module/builds/NativePulpoModule_v0.0.30/ios/PulpoModule.xcframework.zip",
            checksum: "111ed7ee1cbeb6b3ba345e5a715b0ec205efed8bf5614312c0c33403221e272d"
        ),
        .binaryTarget(
            name: "PulpoTryOnKit",
            url: "https://assets.pulpoar.com/vision/pulpo-sdk/ios/tryon/0.2.1/PulpoTryOnKit.xcframework.zip",
            checksum: "64e9fa5c1d1534fcf7ffaafa4ad5083c4a956791efd91424d5649b6f7378b729"
        ),
        .binaryTarget(
            name: "PulpoTryOnUI",
            url: "https://assets.pulpoar.com/vision/pulpo-sdk/ios/tryon/0.2.1/PulpoTryOnUI.xcframework.zip",
            checksum: "9c18c428a11f0aeeee62af084568e7c26dcc919854a5fa56e1f10657af26cc2d"
        )
    ]
)
