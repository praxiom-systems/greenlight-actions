"""Regression coverage for intended gates, configuration errors, and CLI diagnostics."""

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "validate-workflows.py"
spec = importlib.util.spec_from_file_location("workflow_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class WorkflowValidationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.filename = ".github/workflows/ci.yml"
        self.native = {
            "on": {"pull_request": None},
            "jobs": {
                "lint": {"runs-on": "ubuntu-latest", "steps": [{"run": "echo lint"}]},
                "integration": {"runs-on": "ubuntu-latest", "environment": "ci-approval", "steps": [{"run": "echo integration"}]},
            },
        }
        self.config = {"workflows": {self.filename: {"mode": "environment", "jobs": {"integration": "ci-approval"}}}}
        example = SCRIPT.parents[1] / "examples" / "dispatch-ci.yml"
        self.dispatch = yaml.load(example.read_text(), Loader=yaml.BaseLoader)

    def write(self, workflow):
        path = self.root / self.filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(workflow, sort_keys=False))

    def errors(self, workflow, dispatch=False):
        self.write(workflow)
        config = {"workflows": {self.filename: {"mode": "dispatch"}}} if dispatch else self.config
        return validator.check_workflows(self.root, config)

    def test_custom_environment_and_ungated_quick_jobs(self):
        self.assertEqual(self.errors(self.native), [])
        self.native["jobs"]["lint"]["environment"] = "ordinary-deployment"
        self.assertEqual(self.errors(self.native), [])

    def test_custom_environment_object_and_case_insensitive_name(self):
        self.native["jobs"]["integration"]["environment"] = {"name": "CI-Approval", "url": "https://example.com"}
        self.assertEqual(self.errors(self.native), [])

    def test_greenlight_is_not_a_hardcoded_required_name(self):
        for name in ["manual-tests", "CI Approval / Dev", "greenlight"]:
            with self.subTest(name=name):
                self.config["workflows"][self.filename]["jobs"]["integration"] = name
                self.native["jobs"]["integration"]["environment"] = name
                self.assertEqual(self.errors(self.native), [])

    def test_typo_missing_reference_and_missing_job_fail(self):
        self.native["jobs"]["integration"]["environment"] = "ci-aproval"
        self.assertIn("GL_ENV_MISMATCH", " ".join(self.errors(self.native)))
        del self.native["jobs"]["integration"]["environment"]
        self.assertIn("GL_ENV_MISMATCH", " ".join(self.errors(self.native)))
        del self.native["jobs"]["integration"]
        self.assertIn("GL_JOB_MISSING", " ".join(self.errors(self.native)))

    def test_supported_pr_conditional_and_unknown_dynamic_expression(self):
        self.native["jobs"]["integration"]["environment"] = "${{ github.event_name == 'pull_request' && 'ci-approval' || '' }}"
        self.assertEqual(self.errors(self.native), [])
        self.native["jobs"]["integration"]["environment"] = "${{ github.event_name == 'pull_request' && 'ci-aproval' || '' }}"
        self.assertIn("GL_ENV_MISMATCH", " ".join(self.errors(self.native)))
        self.native["jobs"]["integration"]["environment"] = "${{ matrix.environment }}"
        self.assertIn("GL_ENV_DYNAMIC", " ".join(self.errors(self.native)))

    def test_missing_file_and_duplicate_yaml_keys(self):
        self.assertIn("GL_WORKFLOW_MISSING", " ".join(validator.check_workflows(self.root, self.config)))
        self.write(self.native)
        (self.root / self.filename).write_text("jobs:\n  integration:\n    environment: ci-approval\n    environment: typo\n")
        self.assertIn("Duplicate", " ".join(validator.check_workflows(self.root, self.config)))

    def test_malformed_yaml_and_nonmapping_jobs(self):
        self.write(self.native)
        (self.root / self.filename).write_text("jobs: [\n")
        self.assertIn("GL_YAML", " ".join(validator.check_workflows(self.root, self.config)))
        for workflow in [None, {}, {"jobs": []}, {"jobs": {"test": "not-a-job"}}]:
            with self.subTest(workflow=workflow):
                self.assertIn("GL_JOBS", " ".join(self.errors(workflow)))

    def test_bad_config_fails_instead_of_succeeding_without_checks(self):
        for config in [None, [], {}, {"workflows": {}}, {"workflows": []}, {"workflows": {}, "extra": True}]:
            with self.subTest(config=config):
                self.assertIn("GL_CONFIG", " ".join(validator.check_workflows(self.root, config)))
        for settings in [{"mode": "automatic"}, {"mode": "environment"}, {"mode": "environment", "jobs": {}}, {"mode": "dispatch", "jobs": {}}, {"mode": "dispatch", "job": "typo"}]:
            with self.subTest(settings=settings):
                self.write(self.native)
                self.assertIn("GL_CONFIG", " ".join(validator.check_workflows(self.root, {"workflows": {self.filename: settings}})))

    def test_invalid_expected_environment_names(self):
        self.write(self.native)
        for name in [None, "", 123, "a" * 256, "bad\nname", "${{ matrix.env }}"]:
            with self.subTest(name=name):
                self.config["workflows"][self.filename]["jobs"]["integration"] = name
                self.assertIn("GL_CONFIG", " ".join(validator.check_workflows(self.root, self.config)))

    def test_workflows_cannot_escape_root_or_use_wrong_paths(self):
        for filename in ["../ci.yml", ".github/workflows/../ci.yml", "examples/ci.yml"]:
            config = {"workflows": {filename: {"mode": "dispatch"}}}
            self.assertIn("GL_CONFIG", " ".join(validator.check_workflows(self.root, config)))
        self.write(self.native)
        path = self.root / self.filename
        path.unlink()
        path.symlink_to(SCRIPT)
        self.assertIn("symlinks must stay inside", " ".join(validator.check_workflows(self.root, self.config)))

    def test_dispatch_template_passes(self):
        self.assertEqual(self.errors(self.dispatch, dispatch=True), [])

    def test_dispatch_contract_errors(self):
        mutations = [
            (lambda w: w["on"].update({"push": None}), "GL_DISPATCH_TRIGGER"),
            (lambda w: w.update({"on": "workflow_dispatch"}), "GL_DISPATCH_INPUT"),
            (lambda w: w.update({"on": [{}]}), "GL_DISPATCH_TRIGGER"),
            (lambda w: w.update({"run-name": "CI"}), "GL_DISPATCH_NAME"),
            (lambda w: w["on"]["workflow_dispatch"]["inputs"]["greenlight_sha"].update({"required": "false"}), "GL_DISPATCH_INPUT"),
            (lambda w: w["on"]["workflow_dispatch"]["inputs"].update({"unexpected": {"required": "true", "type": "string"}}), "GL_DISPATCH_INPUT"),
            (lambda w: w["on"]["workflow_dispatch"].update({"inputs": []}), "GL_DISPATCH_INPUT"),
            (lambda w: w["jobs"]["test"].update({"environment": "ci-approval"}), "GL_DISPATCH_ENVIRONMENT"),
            (lambda w: w["jobs"]["test"]["steps"][1]["with"].update({"ref": "main"}), "GL_DISPATCH_CHECKOUT"),
            (lambda w: w["jobs"]["test"]["steps"][1]["with"].update({"persist-credentials": "true"}), "GL_DISPATCH_CREDENTIALS"),
            (lambda w: w["jobs"]["test"].update({"steps": []}), "GL_DISPATCH_CHECKOUT"),
            (lambda w: w["jobs"]["test"].update({"steps": ["bad-step"]}), "GL_STEPS"),
            (lambda w: w["jobs"].update({"reused": {"uses": "org/repo/.github/workflows/ci.yml@main"}}), "GL_DISPATCH_REUSABLE"),
        ]
        for mutate, expected in mutations:
            with self.subTest(expected=expected):
                workflow = copy.deepcopy(self.dispatch)
                mutate(workflow)
                self.assertIn(expected, " ".join(self.errors(workflow, dispatch=True)))

    def test_cli_exit_status_and_actions_annotation(self):
        self.write(self.native)
        (self.root / "greenlight-workflows.json").write_text(json.dumps(self.config))
        command = [sys.executable, str(SCRIPT), "--root", str(self.root)]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.native["jobs"]["integration"]["environment"] = "typo"
        self.write(self.native)
        result = subprocess.run(command, capture_output=True, text=True, env={**os.environ, "GITHUB_ACTIONS": "true"})
        self.assertEqual(result.returncode, 1)
        self.assertIn("::error title=Greenlight workflow validation::GL_ENV_MISMATCH", result.stdout)
        (self.root / "greenlight-workflows.json").write_text("not-json")
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)


if __name__ == "__main__":
    unittest.main()
