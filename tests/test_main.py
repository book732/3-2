from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import main


class MainBonusTests(unittest.TestCase):
    def test_convention_is_added_without_removing_required_pr_sections(self) -> None:
        _prompt = main._build_prompt("pr", " M budget_app/service.py", "diff", "Write Korean bullets")

        self.assertIn("Write Korean bullets", _prompt)
        self.assertIn("Why, What, How to Test", _prompt)

    def test_safe_mode_masks_and_limits_untracked_diff(self) -> None:
        with TemporaryDirectory() as _directory:
            _root = Path(_directory)
            subprocess.run(("git", "init", "-q", str(_root)), check=True)
            (_root / "a.txt").write_text("api_key=sk-example-token-1234567890\n", encoding="utf-8")
            (_root / "b.txt").write_text("second file\n", encoding="utf-8")

            _previous_directory = Path.cwd()
            try:
                os.chdir(_root)
                _, _safe_diff = main._collect_git_context(False, 1, 20)
                _, _line_limited_diff = main._collect_git_context(False, 10, 5)
                _, _unsafe_diff = main._collect_git_context(True, 1, 20)
            finally:
                os.chdir(_previous_directory)

        self.assertIn("api_key=[REDACTED]", _safe_diff)
        self.assertIn("[safe-mode: 나머지 파일 diff 생략]", _safe_diff)
        self.assertNotIn("b.txt", _safe_diff)
        self.assertIn("[safe-mode: 줄 수 제한으로 나머지 diff 생략]", _line_limited_diff)
        self.assertIn("sk-example-token-1234567890", _unsafe_diff)
        self.assertIn("b.txt", _unsafe_diff)


if __name__ == "__main__":
    unittest.main()
