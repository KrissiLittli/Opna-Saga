# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Okkar-Saga contributors
"""End-to-end checks using synthetic coordinates and temporary input files."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "check_xyz.py"


class CheckXYZTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def run_file(self, data, name="sample.xyz"):
        path = self.folder / name
        path.write_bytes(data)
        result = self.run_cli(path)
        # Every validation path must leave even malformed sources unchanged.
        self.assertEqual(path.read_bytes(), data)
        self.assertNotIn(str(self.folder), result.stdout + result.stderr)
        return result

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), *map(str, args)],
                              capture_output=True, text=True, check=False)

    def assert_invalid(self, data, reason, line=1):
        result = self.run_file(data)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIn(f":{line}:", result.stderr)
        self.assertIn(reason, result.stderr)
        return result

    def test_valid_points_and_comments_are_counted(self):
        result = self.run_file(b"# synthetic\n\n1 2 3\n-1.5\t0\t2e3 # note\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertIn("OK", result.stdout)
        self.assertIn("2 points", result.stdout)

    def test_nonfinite_values_are_rejected(self):
        for value in (b"NaN", b"inf", b"-Infinity", b"1e9999"):
            with self.subTest(value=value):
                self.assert_invalid(b"# comment\n0 " + value + b" 1\n", "finite", 2)

    def test_wrong_dimensions_are_rejected(self):
        for row in (b"1 2\n", b"1 2 3 4\n"):
            with self.subTest(row=row):
                self.assert_invalid(row, "exactly 3")

    def test_invalid_number_does_not_echo_source(self):
        result = self.assert_invalid(b"1 secret_value 3\n", "not a number")
        self.assertNotIn("secret_value", result.stderr)

    def test_empty_or_comment_only_files_are_rejected(self):
        for data in (b"", b"\n# comments only\n"):
            with self.subTest(data=data):
                self.assert_invalid(data, "no data rows", 1 if not data else 2)

    def test_utf8_error_has_line_number_and_io_exit_code(self):
        result = self.run_file(b"1 2 3\n\xff 0 1\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn(":2: invalid UTF-8", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_missing_file_has_io_exit_code_without_parent_path(self):
        result = self.run_cli(self.folder / "missing.xyz")
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing.xyz", result.stderr)
        self.assertIn("cannot read file", result.stderr)
        self.assertNotIn(str(self.folder), result.stderr)

    def test_missing_argument_has_usage_exit_code(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stderr)

    def test_examples_match_their_labels(self):
        valid = self.run_cli(ROOT / "examples" / "valid.xyz")
        invalid = self.run_cli(ROOT / "examples" / "invalid.xyz")
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertEqual(invalid.returncode, 1, invalid.stderr)
        self.assertIn("finite", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
