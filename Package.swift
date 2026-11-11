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
            url: "https://assets.pulpoar.com/vision/pulpo-module/builds/NativePulpoModule_v0.0.31/ios/PulpoModule.xcframework.zip",
            checksum: "b7524b2eed1f6ad08c4f3fa2f37a7626148e927f0f2a2accfa2ea39a24a259e5"
        ),
        .binaryTarget(
            name: "PulpoTryOnKit",
            url: "https://assets.pulpoar.com/vision/pulpo-sdk/ios/tryon/0.2.2/PulpoTryOnKit.xcframework.zip",
            checksum: "16becd4d9b41da3b8cc6d0992200eb3e16e5b181cc7f609a1dd0084445d4cdfc"
        ),
        .binaryTarget(
            name: "PulpoTryOnUI",
            url: "https://assets.pulpoar.com/vision/pulpo-sdk/ios/tryon/0.2.2/PulpoTryOnUI.xcframework.zip",
            checksum: "b4d912a49fd32992bf6c338345dbeef78782176a1a334ac4eae6fd033e94ed79"
        )
    ]
)
