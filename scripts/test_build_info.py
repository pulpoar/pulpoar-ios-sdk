import unittest

from build_info import BUILD_PREFIX, check, folder, plan, targets

ENGINE_URL = "https://assets.pulpoar.com/vision/pulpo-module/builds/NativePulpoModule_v0.0.28/ios/PulpoModule.xcframework.zip"
BASE = BUILD_PREFIX + "ios/tryon/0.1.0/"
OLD = BUILD_PREFIX + "ios/tryon/0.0.9/"
CS_ENGINE, CS_KIT, CS_UI, CS_OTHER = "e" * 64, "a" * 64, "b" * 64, "c" * 64


def info(version="0.1.0", engine=CS_ENGINE, kit=CS_KIT, ui=CS_UI):
    return {
        "schema": 1,
        "version": version,
        "modules": {
            "PulpoTryOnKit": {"file": "PulpoTryOnKit.xcframework.zip", "checksum": kit},
            "PulpoTryOnUI": {"file": "PulpoTryOnUI.xcframework.zip", "checksum": ui},
        },
        "engine": {"module": "PulpoModule", "package_version": "0.0.28", "url": ENGINE_URL, "checksum": engine},
    }


def manifest(*entries):
    return "targets: [\n" + "".join(
        f'    .binaryTarget(\n        name: "{name}",\n        url: "{url}",\n        checksum: "{cs}"\n    ),\n'
        for name, url, cs in entries
    ) + "]\n"


ENGINE = ("PulpoModule", ENGINE_URL, CS_ENGINE)
KIT = ("PulpoTryOnKit", BASE + "PulpoTryOnKit.xcframework.zip", CS_KIT)
UI = ("PulpoTryOnUI", BASE + "PulpoTryOnUI.xcframework.zip", CS_UI)


class Folder(unittest.TestCase):
    def test_normalizes_trailing_slash(self):
        self.assertEqual(folder(BASE.rstrip("/")), BASE)
        self.assertEqual(folder(BASE), BASE)

    def test_rejects_other_hosts_and_characters(self):
        for url in ["https://evil.example/pulpo-sdk/ios/tryon/0.1.0/",
                    "https://assets.pulpoar.com/vision/pulpo-module/builds/x/",
                    BASE + "?x=1", BASE + '"', BASE + "../../pulpo-module/"]:
            with self.assertRaises(ValueError, msg=url):
                folder(url)


class Plan(unittest.TestCase):
    def test_lists_each_binary_with_its_checksum(self):
        self.assertEqual(plan(info(), BASE, "0.1.0"), [
            ("PulpoTryOnKit", BASE + "PulpoTryOnKit.xcframework.zip", CS_KIT),
            ("PulpoTryOnUI", BASE + "PulpoTryOnUI.xcframework.zip", CS_UI),
        ])

    def test_version_must_match(self):
        with self.assertRaisesRegex(ValueError, "is for version"):
            plan(info(version="0.1.1"), BASE, "0.1.0")

    def test_rejects_malformed_build_info(self):
        bad = [
            {**info(), "schema": 2},
            {**info(), "modules": {}},
            {**info(), "modules": {"PulpoTryOnKit": {"file": "../x.zip", "checksum": CS_KIT}}},
            {**info(), "modules": {"PulpoTryOnKit": {"file": "PulpoTryOnKit.xcframework.zip", "checksum": "XYZ"}}},
            {**info(), "modules": {"Pulpo Kit": {"file": "Pulpo Kit.xcframework.zip", "checksum": CS_KIT}}},
            {**info(), "engine": {}},
        ]
        for entry in bad:
            with self.assertRaises(ValueError, msg=entry):
                plan(entry, BASE, "0.1.0")


class Check(unittest.TestCase):
    def run_check(self, entries, builds):
        def fetch(url):
            return builds[url]
        return check(manifest(*entries), fetch)

    def test_engine_only_package_needs_no_build_info(self):
        self.assertEqual(self.run_check([ENGINE], {}), [])

    def test_consistent_build_passes(self):
        self.assertEqual(self.run_check([ENGINE, KIT, UI], {BASE + "build-info.json": info()}), [])

    def test_engine_must_match_the_build(self):
        problems = self.run_check([("PulpoModule", ENGINE_URL, CS_OTHER), KIT, UI], {BASE + "build-info.json": info()})
        self.assertEqual(len(problems), 1)
        self.assertIn("was built against PulpoModule", problems[0])

    def test_missing_engine(self):
        problems = self.run_check([KIT, UI], {BASE + "build-info.json": info()})
        self.assertEqual(len(problems), 1)
        self.assertIn("not in Package.swift", problems[0])

    def test_kit_and_ui_from_different_builds(self):
        old_ui = ("PulpoTryOnUI", OLD + "PulpoTryOnUI.xcframework.zip", CS_OTHER)
        builds = {BASE + "build-info.json": info(), OLD + "build-info.json": info(version="0.0.9", ui=CS_OTHER)}
        problems = self.run_check([ENGINE, KIT, old_ui], builds)
        self.assertTrue(any("PulpoTryOnUI must come from the build at " + BASE in p for p in problems), problems)
        self.assertTrue(any("PulpoTryOnKit must come from the build at " + OLD in p for p in problems), problems)

    def test_checksum_must_match_the_build(self):
        problems = self.run_check([ENGINE, KIT, ("PulpoTryOnUI", UI[1], CS_OTHER)], {BASE + "build-info.json": info()})
        self.assertEqual(len(problems), 1)
        self.assertIn("PulpoTryOnUI must come from", problems[0])

    def test_build_missing_a_module(self):
        problems = self.run_check([ENGINE, KIT], {BASE + "build-info.json": info()})
        self.assertEqual(problems, [f"PulpoTryOnUI is part of the build at {BASE} but not in Package.swift"])

    def test_target_not_in_its_folders_build(self):
        stray = ("PulpoSkinAIKit", BASE + "PulpoSkinAIKit.xcframework.zip", CS_OTHER)
        problems = self.run_check([ENGINE, KIT, UI, stray], {BASE + "build-info.json": info()})
        self.assertEqual(len(problems), 1)
        self.assertIn("PulpoSkinAIKit", problems[0])

    def test_duplicate_target(self):
        with self.assertRaises(ValueError):
            targets(manifest(KIT, KIT))


if __name__ == "__main__":
    unittest.main()
