"""Offline runner checks: python -m unittest discover -s evals."""

import copy
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import eval as runner


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.record = runner.load(runner.ROOT / "results.json")
        self.cases = runner.load(runner.ROOT / "cases.json")["cases"]

    def test_published_results_and_rejected_mutations(self):
        self.assertEqual(runner.check(self.record, self.cases), [])
        for case_id, text in [
            ("T10", '{"status":"timeout","status":"timeout","detail":"Unknown."}'),
            ("T10", '["status", "detail"]'),
            ("T10", '{"detail":"Unknown.","status":"timeout"}'),
            ("T09", "word " * 26),
            ("T13", "Changed text."),
        ]:
            with self.subTest(case_id=case_id, text=text):
                altered = copy.deepcopy(self.record)
                next(row for row in altered["results"] if row["id"] == case_id)["response"] = text
                self.assertTrue(runner.check(altered, self.cases))
        for key in ["skill_sha256", "cases_sha256"]:
            altered = {**self.record, key: "stale"}
            with self.assertRaises(ValueError):
                runner.check(altered, self.cases)
        self.record["results"].pop()
        with self.assertRaises(ValueError):
            runner.check(self.record, self.cases)

    def test_command_transport_and_failure(self):
        command = [sys.executable, "-c", "import sys; sys.stdout.buffer.write(sys.stdin.buffer.read())"]
        self.assertEqual(runner.invoke(command, " precise café \n", 10), " precise café ")
        with self.assertRaises(ValueError):
            runner.invoke([sys.executable, "-c", "raise SystemExit(2)"], "", 10)
        with self.assertRaises(subprocess.TimeoutExpired):
            runner.invoke([sys.executable, "-c", "import time; time.sleep(10)"], "", 0.05)

    def test_selected_skill_and_exact_response(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evals = root / "evals"
            evals.mkdir()
            default, alternate = root / "SKILL.md", root / "preference.md"
            default.write_text("Default communication instructions.", encoding="utf-8")
            alternate.write_bytes(b"Alternative instructions.\r\nPreserve meaning.\r\n")
            suite = {"scoring": "Preserve exact text.", "cases": [
                {"id": "T29", "prompt": "Return the supplied text unchanged.",
                 "criteria": ["Exact response."], "exact_response": "Keep this text."}
            ]}
            (evals / "cases.json").write_text(json.dumps(suite), encoding="utf-8")
            with patch.object(runner, "ROOT", evals):
                for skill in [default, alternate]:
                    with self.subTest(skill=skill.name):
                        options = [] if skill == default else ["--skill", str(skill)]
                        raw, graded = root / (skill.stem + "-raw.json"), root / (skill.stem + "-graded.json")

                        def fake_model(command, prompt, timeout):
                            if prompt.startswith("Apply these communication instructions:"):
                                self.assertIn(skill.read_text(encoding="utf-8"), prompt)
                                self.assertNotIn("exact_response", prompt)
                                return "Keep this text."
                            return '{"pass": true, "reason": "Synthetic runner test."}'

                        with patch.object(runner, "invoke", side_effect=fake_model):
                            for args in [
                                ["run", "--output", str(raw), "--settings", "offline fake"] + options + ["--", "fake"],
                                ["grade", "--input", str(raw), "--output", str(graded), "--settings", "offline fake"] + options + ["--", "fake"],
                                ["check", "--input", str(graded)] + options,
                            ]:
                                with patch.object(sys, "argv", ["eval.py"] + args):
                                    self.assertEqual(runner.main(), 0)
                        record = runner.load(graded)
                        self.assertEqual(record["skill_sha256"], runner.content_hash(skill))
                        self.assertNotIn(directory, graded.read_text(encoding="utf-8"))
                        record["results"][0]["response"] = "Changed text."
                        self.assertEqual(runner.check(record, suite["cases"], skill), ["T29: Exact text changed"])
                        if skill == alternate:
                            with self.assertRaisesRegex(ValueError, "Skill differs"):
                                runner.check(runner.load(graded), suite["cases"])
                        skill.write_text("Changed instructions.", encoding="utf-8")
                        for args in [
                            ["check", "--input", str(graded)] + options,
                            ["grade", "--input", str(raw), "--output", str(root / "regrade.json"), "--settings", "offline fake"] + options + ["--", "fake"],
                        ]:
                            with patch.object(sys, "argv", ["eval.py"] + args):
                                with self.assertRaisesRegex(ValueError, "Skill differs"):
                                    runner.main()
                        self.assertFalse((root / "regrade.json").exists())

    def test_run_grade_check_and_overwrite_protection(self):
        answers = {row["id"]: row["response"] for row in self.record["results"]}

        def fake_model(command, prompt, timeout):
            if prompt.startswith("Apply these communication instructions:"):
                self.assertNotIn('"criteria":', prompt)
                case = next(case for case in self.cases if prompt.endswith(case["prompt"]))
                return answers[case["id"]]
            self.assertNotIn("# Term-Inator", prompt)
            data = json.loads(prompt.split("\n", 1)[1])
            self.assertEqual(data["response"], answers[data["case"]["id"]])
            return '{"pass": true, "reason": "Synthetic runner test, not a model evaluation."}'

        with tempfile.TemporaryDirectory() as directory, patch.object(runner, "invoke", side_effect=fake_model):
            raw, graded = Path(directory) / "raw.json", Path(directory) / "graded.json"
            for args in [
                ["run", "--output", str(raw), "--settings", "offline fake", "--", "fake"],
                ["grade", "--input", str(raw), "--output", str(graded), "--settings", "offline fake", "--", "fake"],
                ["check", "--input", str(graded)],
            ]:
                with patch.object(sys, "argv", ["eval.py"] + args):
                    self.assertEqual(runner.main(), 0)
            with patch.object(sys, "argv", ["eval.py", "run", "--output", str(raw), "--settings", "offline fake", "--", "fake"]):
                with self.assertRaises(FileExistsError):
                    runner.main()
            before = runner.load(graded)
            self.assertNotIn("date", before)
            self.assertNotIn(directory, graded.read_text(encoding="utf-8"))
            # A failed regrade must not leave old passing verdicts on unreviewed cases.
            failed = Path(directory) / "failed.json"
            with patch.object(runner, "invoke", side_effect=['{"pass": false, "reason": "Test failure"}', '{"pass": "yes", "reason": "Invalid"}']):
                with patch.object(sys, "argv", ["eval.py", "grade", "--input", str(graded), "--output", str(failed), "--settings", "offline fake", "--", "fake"]):
                    with self.assertRaises(ValueError):
                        runner.main()
            partial = runner.load(failed)
            self.assertFalse(partial["results"][0]["pass"])
            self.assertNotIn("pass", partial["results"][1])
            self.assertTrue(runner.check(partial, self.cases))

    def test_timeout_terminates_wrapper_descendant(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ready, marker = root / "ready", root / "survived"
            child = root / "child.py"
            child.write_text(
                "import pathlib, time\n"
                f"pathlib.Path({str(ready)!r}).touch()\n"
                "time.sleep(2)\n"
                f"pathlib.Path({str(marker)!r}).touch()\n", encoding="utf-8")
            if os.name == "nt":
                shim = root / "model.cmd"
                shim.write_text(f'@"{sys.executable}" "{child}"\n', encoding="utf-8")
                command = ["cmd", "/d", "/c", str(shim)]
            else:
                command = [sys.executable, "-c", "import subprocess, sys; subprocess.run(sys.argv[1:])", sys.executable, str(child)]
            with self.assertRaises(subprocess.TimeoutExpired):
                runner.invoke(command, "probe", 1)
            self.assertTrue(ready.exists(), "Probe child must start before timeout")
            time.sleep(2)
            self.assertFalse(marker.exists(), "Timed-out model descendant survived")


if __name__ == "__main__":
    unittest.main()
