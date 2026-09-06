"""Transport tests only. The Validation workflow supplies real SQL evidence."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SQLCMD = "/opt/mssql-tools18/bin/sqlcmd"
FIXTURE_PASSWORD = "Disposable fixture phrase ! with spaces"
MOCK = r'''#!/usr/bin/env python3
import hashlib, json, os, pathlib, sys
args = sys.argv[1:]
kind = pathlib.Path(sys.argv[0]).name
source = sys.stdin.buffer.read()
password_valid = None
if kind == "sqlcmd":
    password_valid = args[args.index("-P") + 1] == os.environ["KOMMIBO_SQL_PASSWORD"]
    args[args.index("-P") + 1] = "<redacted>"
args = [arg.split("=", 1)[0] + "=<redacted>" if arg.startswith(("SQLCMDPASSWORD=", "MSSQL_SA_PASSWORD=")) else arg for arg in args]
event = {"kind": kind, "args": args, "stdin_sha256": hashlib.sha256(source).hexdigest(), "password_valid": password_valid}
with open(os.environ["TRANSPORT_LOG"], "a") as output:
    output.write(json.dumps(event) + "\n")
if source and os.environ.get("FAIL_SQL") == "1":
    sys.exit(7)
'''


class SqlTransportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "tests").mkdir()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        for name in ("docker", "sqlcmd"):
            executable = self.bin / name
            executable.write_text(MOCK)
            executable.chmod(0o755)
        script = (ROOT / "tests/validate_sql.sh").read_text()
        self.assertEqual(script.count(f"readonly SQLCMD='{SQLCMD}'"), 1)
        # Substitute only the fixed executable path in a disposable script copy.
        # Production keeps its immutable client location and has no test override.
        script = script.replace(SQLCMD, str(self.bin / "sqlcmd"))
        self.script = self.root / "tests/validate_sql.sh"
        self.script.write_text(script)
        shutil.copyfile(ROOT / "SP_CreateTables.sql", self.root / "SP_CreateTables.sql")
        self.log = self.root / "calls.jsonl"

    def execute(self, settings, trace=False):
        env = {key: value for key, value in os.environ.items() if not key.startswith("KOMMIBO_SQL_")}
        env.update(PATH=f"{self.bin}{os.pathsep}{env['PATH']}", TRANSPORT_LOG=str(self.log), **settings)
        result = subprocess.run(
            ["bash", *(["-x"] if trace else []), str(self.script)],
            env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=15,
        )
        self.assertNotIn(FIXTURE_PASSWORD, result.stdout + result.stderr)
        events = [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []
        return result, events

    def test_sidecar_preserves_all_sql_checks_without_docker_or_cleanup(self):
        result, events = self.execute({
            "KOMMIBO_SQL_SERVER": "sqlserver,1433",
            "KOMMIBO_SQL_PASSWORD": FIXTURE_PASSWORD,
        }, trace=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(events), 8)  # readiness + fixture + rollback/check + two commit/check pairs
        self.assertTrue(all(event["kind"] == "sqlcmd" for event in events))
        self.assertTrue(all(event["password_valid"] for event in events))
        for event in events:
            self.assertEqual(event["args"][:7], ["-S", "sqlserver,1433", "-U", "sa", "-P", "<redacted>", "-C"])
        source = (ROOT / "SP_CreateTables.sql").read_bytes()
        commit = source.replace(b"declare @EjecutarCommit char(1) = 'N'", b"declare @EjecutarCommit char(1) = 'Y'")
        self.assertEqual(events[2]["stdin_sha256"], hashlib.sha256(source).hexdigest())
        self.assertEqual([events[index]["stdin_sha256"] for index in (4, 6)], [hashlib.sha256(commit).hexdigest()] * 2)
        self.assertIn("Rollback mode persisted REGISTER_JOIN.", events[3]["args"][-1])
        for index in (5, 7):
            query = events[index]["args"][-1]
            for expected in ("<> 9", "REG_001", "UQ_REGISTER_INTERNAL_NUM"):
                self.assertIn(expected, query)
        self.assertNotIn(FIXTURE_PASSWORD, self.log.read_text())

    def test_default_still_owns_a_pinned_docker_container(self):
        result, events = self.execute({})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(all(event["kind"] == "docker" for event in events))
        self.assertEqual(events[0]["args"][0], "run")
        self.assertTrue(events[0]["args"][-1].endswith("@sha256:ba4c8329f48fb8f02e1416be6a930ebfd71268caee78aa985f3af4315e457c89"))
        self.assertEqual(events[-1]["args"][:2], ["rm", "--force"])
        self.assertEqual(len([event for event in events if event["args"][0] == "exec"]), 8)

    def test_sidecar_failure_propagates_without_destroying_external_container(self):
        result, events = self.execute({
            "KOMMIBO_SQL_SERVER": "sqlserver,1433",
            "KOMMIBO_SQL_PASSWORD": FIXTURE_PASSWORD,
            "FAIL_SQL": "1",
        })
        self.assertEqual(result.returncode, 7)
        self.assertNotIn("validation: PASS", result.stdout)
        self.assertTrue(all(event["kind"] == "sqlcmd" for event in events))

    def test_partial_or_nonisolated_sidecar_configuration_fails_before_commands(self):
        for settings in (
            {"KOMMIBO_SQL_SERVER": "sqlserver,1433"},
            {"KOMMIBO_SQL_PASSWORD": FIXTURE_PASSWORD},
            {"KOMMIBO_SQL_SERVER": "production.example,1433", "KOMMIBO_SQL_PASSWORD": FIXTURE_PASSWORD},
            {"KOMMIBO_SQL_SERVER": "sqlserver,1433", "KOMMIBO_SQL_PASSWORD": ""},
        ):
            with self.subTest(settings=list(settings)):
                result, events = self.execute(settings)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(events, [])


if __name__ == "__main__":
    unittest.main()
