import hashlib
import tempfile
import unittest
from pathlib import Path

from generator.dragon import build_dragon


class DragonGeneratorTests(unittest.TestCase):
    def _sha256(self, file_path: Path) -> str:
        digest = hashlib.sha256()
        with file_path.open("rb") as f:
            digest.update(f.read())
        return digest.hexdigest()

    def test_same_seed_produces_same_png(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path_a = Path(tmp) / "a.png"
            path_b = Path(tmp) / "b.png"

            build_dragon(42, 256, 192).image.write_png(str(path_a))
            build_dragon(42, 256, 192).image.write_png(str(path_b))

            self.assertEqual(self._sha256(path_a), self._sha256(path_b))

    def test_different_seed_changes_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path_a = Path(tmp) / "a.png"
            path_b = Path(tmp) / "b.png"

            build_dragon(42, 256, 192).image.write_png(str(path_a))
            build_dragon(43, 256, 192).image.write_png(str(path_b))

            self.assertNotEqual(self._sha256(path_a), self._sha256(path_b))

    def test_jpeg_export_requires_pillow_or_writes_jpeg(self) -> None:
        dragon = build_dragon(42, 128, 96)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "dragon.jpg"
            try:
                dragon.image.write_jpeg(str(out))
            except RuntimeError as exc:
                self.assertIn("JPEG export requires Pillow", str(exc))
            else:
                self.assertTrue(out.exists())
                self.assertGreater(out.stat().st_size, 0)



if __name__ == "__main__":
    unittest.main()
