import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from logictree.processing.choice import extract_boxed_answer_enhanced, process_jsonl_file


class ProcessingTests(unittest.TestCase):
    def test_extract_boxed_answer_normalizes_choice(self):
        self.assertEqual(extract_boxed_answer_enhanced(r"Reasoning... \boxed{(b)}"), "B")
        self.assertEqual(extract_boxed_answer_enhanced(r"First \boxed{A}, finally \boxed{C}"), "C")

    def test_choice_filter_keeps_only_matching_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "responses.jsonl"
            output = Path(directory) / "filtered.jsonl"
            rows = [
                {"answer": "A", "model_answer": r"Final: \boxed{A}"},
                {"answer": "B", "model_answer": r"Final: \boxed{C}"},
            ]
            source.write_text(
                "".join(json.dumps(row) + "\n" for row in rows),
                encoding="utf-8",
            )

            with contextlib.redirect_stdout(io.StringIO()):
                report = process_jsonl_file(source, output)
            saved = json.loads(output.read_text(encoding="utf-8"))

            self.assertEqual(report["kept"], 1)
            self.assertEqual(saved["answer"], r"Final: \boxed{A}")
