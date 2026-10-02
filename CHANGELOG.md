# Changelog

All notable changes to the PulpoAR iOS SDK are listed here. Versions follow semantic versioning.

## 0.0.24
- First release from this repository.
- xcframework slimmed to the minimum (no dSYMs); `Info.plist` no longer references removed debug symbols, fixing the Xcode "Missing path … dSYMs" build error from earlier test builds.
- Minimum iOS 18.4. Device slice `arm64`, simulator slice `x86_64` only.
