from __future__ import annotations

import csv
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SIGNAL = load("signal2content_score")
OUTLIER = load("outlier_score")


class ToolTests(unittest.TestCase):
    def run_tool(self, name: str, path: Path, *args: str):
        return subprocess.run(
            [sys.executable, str(ROOT / "tools" / f"{name}.py"), str(path), *args],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=10,
        )

    def test_bundled_signal_result_is_stable(self):
        result = self.run_tool(
            "signal2content_score",
            ROOT / "examples" / "signal2content-opportunities.csv",
            "--top", "3",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        rows = list(csv.reader(io.StringIO(result.stdout)))
        self.assertEqual(["1", "Pinterest seasonal visual series", "83.05"], rows[1])
        self.assertEqual(["2", "AI before-after workflow", "79.00"], rows[2])

    def test_bundled_outlier_result_is_stable(self):
        result = self.run_tool(
            "outlier_score",
            ROOT / "examples" / "social-outlier-posts.csv",
            "--top", "3",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        rows = list(csv.reader(io.StringIO(result.stdout)))
        self.assertEqual(["1", "instagram", "reel-004", "6.73", "3.94", "8.91"], rows[1])

    def test_validate_only_is_read_only(self):
        for tool, sample in (
            ("signal2content_score", "signal2content-opportunities.csv"),
            ("outlier_score", "social-outlier-posts.csv"),
        ):
            path = ROOT / "examples" / sample
            before = path.read_bytes()
            result = self.run_tool(tool, path, "--validate-only")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(before, path.read_bytes())

    def test_signal_rejects_missing_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text("name\nExample\n", encoding="utf-8")
            result = self.run_tool("signal2content_score", path)
            self.assertEqual(2, result.returncode)
            self.assertIn("Missing columns", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_outlier_rejects_invalid_metric(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text(
                "platform,post_id,views,likes,comments,shares,saves\n"
                "instagram,001,N/A,10,2,3,4\n",
                encoding="utf-8",
            )
            result = self.run_tool("outlier_score", path)
            self.assertEqual(2, result.returncode)
            self.assertIn("views", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_bom_and_leading_zero_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "posts.csv"
            path.write_text(
                "platform,post_id,views,likes,comments,shares,saves\n"
                "instagram,001,100,10,2,3,4\n",
                encoding="utf-8-sig",
            )
            rows = OUTLIER.load_rows(path)
            self.assertEqual("001", rows[0]["post_id"])

    def test_signal_score_is_bounded(self):
        row = {
            "name": "x",
            "evidence_strength": "100",
            "audience_fit": "100",
            "freshness": "100",
            "repeatability": "100",
            "production_ease": "100",
            "saturation": "0",
        }
        self.assertEqual(100.0, SIGNAL.score_row(row))


if __name__ == "__main__":
    unittest.main()
