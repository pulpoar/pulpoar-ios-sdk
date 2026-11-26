# Changelog

All notable changes to the PulpoAR iOS SDK are listed here. Versions follow semantic versioning.

## 0.4.0
`PulpoTryOnKit` and `PulpoTryOnUI` 0.4.0, built against the same `PulpoModule` 0.0.32. **Breaking** for apps that call the Kit's `track*` methods; apps that only use `PulpoTryOnUI` need no changes.
- **Try-on events, as the web plugin sends them:** new `PulpoTryOnEvent` (one case per web event, with the same data and the web's event name in `key`, such as `onAddToCart`). `PulpoTryOnSession.tryOnEvents` (an `AsyncStream`) delivers every event to the app, whatever the analytics consent: the Kit's own (`ready`, `error`, `usePhoto`, `variantSelect`, `appliedVariantsChange`, `tryOn`) and those a UI tracks. Start iterating before `loadCatalog()` or `start` to get `ready`.
- **PulpoTryOnUI:** `PulpoTryOnUIConfiguration.onEvent` receives every event on the main thread, for the app's own analytics. The live camera has a mirror button, as on the web.
- **PulpoTryOnKit:** `PulpoCameraView` and `PulpoCameraUIView` gain `isMirrored` (default `true`: the front camera shows as a mirror). Display only; photos and snapshots are never flipped.
- **Removed (breaking):** `PulpoUIEvent` and the `track*` methods. Migrate with `track(_:)`:
  - `trackUIEvent(.x)` → `track(.x)` (the case names are kept)
  - `trackAddToCart(variants)` → `track(.addToCart(variants))`; likewise `trackGoToProduct`, `trackExperienceSelect`, `trackLookSelect`, `trackBrandSelect`, `trackCategorySelect` and `trackProductSelect`
  - The events the Kit sends itself are ignored by `track(_:)`, with a warning, so they aren't counted twice.
- **Analytics, matching the web's reports:** `onReady` carries `entryType: "embedded"`; hiding and showing the try-on no longer counts the restored shades and photo as new choices; a project preloaded while another runs keeps its own visit.
- **Install:** pick "Up to Next Minor Version" (below 1.0, a minor version can change the API).

## 0.3.0
- New product `PulpoSkinAIKit` 0.3.0: on-device skin analysis of a photo (`PulpoSkinAnalyzer().analyze(photo)`), with the skin health score, 12 issue scores, acne count, masks and visuals. Needs Xcode 26+. Links its own engine, `PulpoSkinAI` 0.1.0, which can sit next to `PulpoModule` in one app.
- `PulpoModule` 0.0.32: the makeup engine of PulpoAR web 1.5.20. Faster foundation and makeup blending; metallic and shimmer eyeshadow; an eyelid-following eyeliner placement, off unless a product config turns it on. `PulpoTryOnKit` and `PulpoTryOnUI` 0.3.0 rebuilt against it. No API changes.

## 0.2.1
- `PulpoModule`, `PulpoTryOnKit` and `PulpoTryOnUI` rebuilt with Xcode 26. No API changes.

## 0.2.0
- `PulpoModule` updated: adds the nail polish try-on API, plus stability and performance improvements.
- `PulpoTryOnKit` and `PulpoTryOnUI` 0.2.0, built against the new `PulpoModule`. No API changes.

## 0.1.0
- New products `PulpoTryOnUI` (ready-made try-on screens) and `PulpoTryOnKit` (Try-On SDK without UI), version 0.1.0, built with Xcode 26 against PulpoModule 0.0.28. Both need Xcode 26+. `PulpoModule` is unchanged and linked by both.
- Package is structured for multiple modules (one product per module); a release updates only the binaries it is given.
- CI runs script tests and resolves every binary on pull requests.
- Release workflow (maintainers) releases a Try-On build (PulpoTryOnKit and PulpoTryOnUI together, from their `build-info.json`) and/or a new PulpoModule in one run, under one tag. It checks that the Try-On binaries match their build and that the build used the package's PulpoModule; CI runs the same check.

## 0.0.28
- `Package.swift` minimum platform lowered from iOS 18.4 to iOS 15.6, matching the 0.0.27 binary (same binary as 0.0.27, so this is the first tag partners can use on iOS 15.6).

## 0.0.27
- PulpoModule xcframework rebuilt with a minimum iOS of 15.6 (was 18.4). Device slice `arm64`, simulator slice `x86_64` only.

## 0.0.24
- First release from this repository.
- xcframework slimmed to the minimum (no dSYMs); `Info.plist` no longer references removed debug symbols, fixing the Xcode "Missing path … dSYMs" build error from earlier test builds.
- Minimum iOS 18.4. Device slice `arm64`, simulator slice `x86_64` only.
