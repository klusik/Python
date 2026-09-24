import tempfile
import unittest
from pathlib import Path

from src.cleaner import build_clean_plan, inspect_entry_details
from src.models import CacheEntry


class CleanPlanTests(unittest.TestCase):
    def test_plan_counts_cache_data_and_preserves_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            wasm_root = Path(temp_dir) / "WASM"
            product = wasm_root / "aircraft"
            nested = product / "module"
            settings = product / "settings"
            nested.mkdir(parents=True)
            settings.mkdir()
            (nested / "cache.bin").write_bytes(b"12345")
            (product / "index.bin").write_bytes(b"123")
            (settings / "user.json").write_bytes(b"do not count")

            entry = CacheEntry("MSFS 2024", "Steam", "aircraft", product, wasm_root, str(wasm_root))
            plan = build_clean_plan((entry,))

            self.assertEqual(plan.file_count, 2)
            self.assertEqual(plan.byte_count, 8)
            self.assertEqual(plan.directory_count, 1)
            self.assertEqual(plan.preserved_count, 1)
            self.assertEqual(plan.warnings, ())

    def test_invalid_target_is_reported_without_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            wasm_root = root / "not-wasm"
            product = wasm_root / "aircraft"
            product.mkdir(parents=True)
            entry = CacheEntry("MSFS 2020", "Steam", "aircraft", product, wasm_root, str(wasm_root))

            plan = build_clean_plan((entry,))

            self.assertEqual(plan.file_count, 0)
            self.assertTrue(plan.warnings)
            self.assertEqual(plan.items[0].warning_count, len(plan.warnings))

    def test_details_identify_wasm_and_protected_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            wasm_root = Path(temp_dir) / "WASM"
            product = wasm_root / "aircraft"
            settings = product / "settings"
            settings.mkdir(parents=True)
            (product / "module.wasm").write_bytes(b"\x00asm\x01\x00\x00\x00payload")
            (product / "cache.bin").write_bytes(b"cache")
            (settings / "user.json").write_text("{}", encoding="utf-8")
            entry = CacheEntry("MSFS 2024", "Steam", "aircraft", product, wasm_root, str(wasm_root))

            details = inspect_entry_details(entry)

            by_path = {item.relative_path: item for item in details.files}
            self.assertEqual(by_path["module.wasm"].kind, "WebAssembly module v1")
            self.assertEqual(by_path["module.wasm"].disposition, "Will clear")
            self.assertEqual(by_path["settings"].kind, "Protected folder")
            self.assertEqual(by_path["settings"].disposition, "Preserved")
            self.assertFalse(any("user.json" in relative_path for relative_path in by_path))


if __name__ == "__main__":
    unittest.main()
