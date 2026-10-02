import unittest

from update_manifest import URL_PREFIX, update

CS_A, CS_B = "a" * 64, "b" * 64
URL_A = URL_PREFIX + "X_v1/ios/Alpha.xcframework.zip"
URL_B = URL_PREFIX + "Y_v2/ios/Beta.xcframework.zip"
SRC = f'''targets: [
    .binaryTarget(
        name: "Alpha",
        url: "{URL_A}",
        checksum: "{CS_A}"
    ),
    .binaryTarget(
        name: "Beta",
        url: "{URL_A}",
        checksum: "{CS_A}"
    )
]
'''


class UpdateManifest(unittest.TestCase):
    def test_updates_only_named_module(self):
        out = update(SRC, "Beta", URL_B, CS_B)
        self.assertEqual(out.count(URL_B), 1)
        self.assertEqual(out.count(CS_B), 1)
        self.assertEqual(out.count(URL_A), 1)
        self.assertLess(out.index(CS_A), out.index(CS_B))  # Alpha (first) untouched

    def test_idempotent(self):
        self.assertEqual(update(SRC, "Alpha", URL_A, CS_A), SRC)

    def test_unknown_module(self):
        with self.assertRaises(ValueError):
            update(SRC, "Gamma", URL_B, CS_B)

    def test_rejects_bad_inputs(self):
        for module, url, cs in [
            ("Alpha", "https://evil.example/x.zip", CS_B),
            ("Alpha", URL_B + '"; evil', CS_B),
            ("Alpha", URL_B + "&x", CS_B),
            ("Alpha", URL_B, "XYZ"),
            ("Alpha", URL_B, CS_B.upper()),
            ("Al.*", URL_B, CS_B),
        ]:
            with self.assertRaises(ValueError, msg=(module, url, cs)):
                update(SRC, module, url, cs)

    def test_duplicate_target_rejected(self):
        with self.assertRaises(ValueError):
            update(SRC + SRC, "Alpha", URL_B, CS_B)


if __name__ == "__main__":
    unittest.main()
