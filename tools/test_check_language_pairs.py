#!/usr/bin/env python3
"""Tests for tools/check-language-pairs."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("check-language-pairs")


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_content_root(base: Path, name: str = "example") -> Path:
    root = base / name
    root.mkdir(parents=True, exist_ok=True)
    write_file(root / "antora.yml", f"name: {name}\ntitle: Example\nversion: ~\n")
    return root


def write_page(content_root: Path, module: str, relative_path: str, lang: str | None) -> None:
    lang_line = f":lang: {lang}\n" if lang is not None else ""
    write_file(
        content_root / "modules" / module / "pages" / relative_path,
        f"= Test\n{lang_line}\nTest page.\n",
    )


class CheckLanguagePairsTest(unittest.TestCase):
    def run_script(self, *content_roots: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *(str(root) for root in content_roots)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_valid_pairs_exit_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = write_content_root(Path(tmp))
            write_page(root, "ROOT", "index.adoc", "en")
            write_page(root, "ja", "index.adoc", "ja")

            result = self.run_script(root)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertEqual(result.stderr, "")

    def test_missing_ja(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = write_content_root(Path(tmp))
            write_page(root, "ROOT", "index.adoc", "en")

            result = self.run_script(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing_ja", result.stdout)
            self.assertIn("\tROOT\tindex.adoc\t", result.stdout)

    def test_missing_en(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = write_content_root(Path(tmp))
            write_page(root, "ja", "index.adoc", "ja")

            result = self.run_script(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing_en", result.stdout)
            self.assertIn("\tja\tindex.adoc\t", result.stdout)

    def test_missing_lang(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = write_content_root(Path(tmp))
            write_page(root, "ROOT", "index.adoc", None)
            write_page(root, "ja", "index.adoc", "ja")

            result = self.run_script(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing_lang", result.stdout)
            self.assertIn("missing :lang: attribute", result.stdout)

    def test_lang_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = write_content_root(Path(tmp))
            write_page(root, "ROOT", "index.adoc", "ja")
            write_page(root, "ja", "index.adoc", "ja")

            result = self.run_script(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("lang_mismatch", result.stdout)
            self.assertIn("expected :lang: en, found ja", result.stdout)

    def test_invalid_content_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            invalid_root = Path(tmp) / "missing-antora"
            invalid_root.mkdir()

            result = self.run_script(invalid_root)

            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("invalid_content_root", result.stderr)

    def test_meta_architecture_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = write_content_root(Path(tmp), "meta-architecture")
            write_page(root, "ROOT", "index.adoc", "ja")

            result = self.run_script(root)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
