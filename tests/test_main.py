from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import main


class TestQrCodeGenerator(unittest.TestCase):
    def test_create_directory_creates_nested_path(self):
        with TemporaryDirectory() as temp_dir:
            nested_path = Path(temp_dir) / "nested" / "qr_codes"

            main.create_directory(nested_path)

            self.assertTrue(nested_path.exists())
            self.assertTrue(nested_path.is_dir())

    def test_generate_qr_code_saves_png_for_valid_url(self):
        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_qr.png"

            main.generate_qr_code(
                "https://example.com",
                output_path,
                fill_color="black",
                back_color="white",
            )

            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)

    def test_generate_qr_code_skips_invalid_url(self):
        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "invalid_qr.png"

            with patch.object(main.logging, "error") as mock_error:
                main.generate_qr_code("not-a-url", output_path)

            self.assertFalse(output_path.exists())
            mock_error.assert_called_once()


if __name__ == "__main__":
    unittest.main()