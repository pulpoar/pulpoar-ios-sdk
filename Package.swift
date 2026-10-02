// swift-tools-version:5.7
import PackageDescription

// PulpoAR iOS SDK, distributed as pre-built binaries (xcframeworks).
// `url` and `checksum` are updated by .github/workflows/release.yml on every release.
// Partners should not edit this file; they depend on this repo by version.
let package = Package(
    name: "PulpoAR",
    platforms: [.iOS("18.4")],
    products: [
        .library(name: "PulpoModule", targets: ["PulpoModule"])
    ],
    targets: [
        .binaryTarget(
            name: "PulpoModule",
            url: "https://assets.pulpoar.com/vision/pulpo-module/builds/NativePulpoModule_v0.0.24/ios/PulpoModule.xcframework.zip",
            checksum: "fc31fc6ad3e608d94c68a1add90a4d6e686428d3ad2297c41ffe8b038d743d57"
        )
    ]
)
