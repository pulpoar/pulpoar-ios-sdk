# Changelog

All notable changes to the PulpoAR iOS SDK are listed here. Versions follow semantic versioning.

## Unreleased
- Package is structured for multiple modules (one product per module); release workflow takes a `module` input and updates only that module's binary.
- CI runs script tests and resolves every binary on pull requests.
- `Package.swift` minimum platform lowered from iOS 18.4 to iOS 15.6 to match the 0.0.27 binary. Takes effect in the next tagged release.

## 0.0.27
- PulpoModule xcframework rebuilt with a minimum iOS of 15.6 (was 18.4). Device slice `arm64`, simulator slice `x86_64` only.
- Note: the `Package.swift` platform still declares iOS 18.4 in this tag; use the next release to get the 15.6 manifest.

## 0.0.24
- First release from this repository.
- xcframework slimmed to the minimum (no dSYMs); `Info.plist` no longer references removed debug symbols, fixing the Xcode "Missing path … dSYMs" build error from earlier test builds.
- Minimum iOS 18.4. Device slice `arm64`, simulator slice `x86_64` only.
