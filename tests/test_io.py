import tempfile
import unittest
from pathlib import Path

from logictree.io import read_jsonl, save_jsonl


class JsonlTests(unittest.TestCase):
    def test_round_trip_creates_parent_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "rows.jsonl"
            rows = [{"text": "逻辑树"}, {"value": 2}]

            save_jsonl(rows, output, "w")

            self.assertEqual(read_jsonl(output), rows)
            self.assertIn("逻辑树", output.read_text(encoding="utf-8"))

    def test_read_reports_line_number(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.jsonl"
            path.write_text('{"ok": true}\nnot-json\n', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, r"broken\.jsonl:2"):
                read_jsonl(path)
