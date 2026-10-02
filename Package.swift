// swift-tools-version:5.7
import PackageDescription

// PulpoAR iOS SDK, distributed as pre-built binaries (xcframeworks).
// One library product per module, each backed by one binaryTarget. Partners add this package once and
// pick only the product(s) they need; SwiftPM downloads only the binaries of the products they link.
// `url` and `checksum` are rewritten by .github/workflows/release.yml (scripts/update_manifest.py),
// so keep each binaryTarget as `name`, `url`, `checksum` on separate lines. Partners never edit this file.
//
// Adding a module: add a library product and a binaryTarget here (url/checksum of its first zip),
// add the name to the `module` options in release.yml, then document it in README.md.
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
