"""Validate explicitly declared Greenlight workflow contracts without executing YAML."""

import argparse
import json
import os
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("Install the validator dependency first: python3 -m pip install PyYAML")


class UniqueLoader(yaml.BaseLoader):
    """Preserve GitHub's `on` key and reject silently overwritten YAML keys."""

    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result:
                raise ValueError(f"Duplicate or invalid YAML key: {key!r}")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


WORKFLOW_PATH = re.compile(r"^\.github/workflows/[-\w.]+\.ya?ml$")
PR_ENVIRONMENT = re.compile(
    r"^\$\{\{\s*github\.event_name\s*==\s*'pull_request'\s*&&\s*'([^']+)'\s*\|\|\s*''\s*\}\}$"
)
INPUTS = ("greenlight_sha", "greenlight_pr", "greenlight_check_id")


def environment_name(value):
    if isinstance(value, dict):
        value = value.get("name")
    if not isinstance(value, str):
        return None
    conditional = PR_ENVIRONMENT.fullmatch(value)
    if conditional:
        return conditional[1]
    return None if "${{" in value else value


def check_workflows(root, config):
    """Return actionable errors for intended gates; other jobs are deliberately allowed."""
    errors = []
    if not isinstance(config, dict) or set(config) != {"workflows"}:
        return ["GL_CONFIG: Configure a 'workflows' object mapping workflow paths to mode/settings."]
    workflows = config["workflows"]
    if not isinstance(workflows, dict) or not workflows:
        return ["GL_CONFIG: Declare at least one intended workflow; empty validation is not a pass."]
    root = Path(root).resolve()
    for filename, settings in workflows.items():
        if not WORKFLOW_PATH.fullmatch(filename):
            errors.append(f"GL_CONFIG: {filename}: Use a filename under .github/workflows/.")
            continue
        if (not isinstance(settings, dict) or settings.get("mode") not in ("environment", "dispatch")
                or set(settings) - {"mode", "jobs"}
                or (settings.get("mode") == "dispatch" and "jobs" in settings)):
            errors.append(f"GL_CONFIG: {filename}: Choose environment mode with an explicit jobs map, or dispatch mode without jobs settings.")
            continue
        path = (root / filename).resolve()
        if not path.is_relative_to(root):
            errors.append(f"GL_CONFIG: {filename}: Workflow symlinks must stay inside the repository.")
            continue
        try:
            workflow = yaml.load(path.read_text(), Loader=UniqueLoader)
        except FileNotFoundError:
            errors.append(f"GL_WORKFLOW_MISSING: {filename}: File does not exist. Correct the configured filename or add the workflow.")
            continue
        except (OSError, UnicodeError, ValueError, yaml.YAMLError) as error:
            errors.append(f"GL_YAML: {filename}: Could not read workflow YAML: {error}")
            continue
        if not isinstance(workflow, dict) or not isinstance(workflow.get("jobs"), dict) or not workflow["jobs"]:
            errors.append(f"GL_JOBS: {filename}: Define a nonempty jobs mapping.")
            continue
        jobs = workflow["jobs"]
        if any(not isinstance(job, dict) for job in jobs.values()):
            errors.append(f"GL_JOBS: {filename}: Each job must be a mapping.")
            continue
        if settings["mode"] == "environment":
            expected = settings.get("jobs")
            if not isinstance(expected, dict) or not expected:
                errors.append(f"GL_CONFIG: {filename}: Declare the job IDs and expected environment names that must be gated.")
                continue
            for job_id, name in expected.items():
                if not isinstance(name, str) or not name or len(name) > 255 or any(c in name for c in "\r\n") or "${{" in name:
                    errors.append(f"GL_CONFIG: {filename}/{job_id}: Expected environment must be a literal name of 1-255 characters.")
                    continue
                if job_id not in jobs:
                    errors.append(f"GL_JOB_MISSING: {filename}/{job_id}: Intended gated job is missing. Correct the job ID or restore it.")
                    continue
                value = jobs[job_id].get("environment")
                actual = environment_name(value)
                if actual is None and value is not None:
                    errors.append(f"GL_ENV_DYNAMIC: {filename}/{job_id}: Cannot verify this environment expression. Use a literal name or the documented pull_request conditional; matrix/reusable-workflow expressions need separate validation.")
                elif actual is None or actual.casefold() != name.casefold():
                    errors.append(f"GL_ENV_MISMATCH: {filename}/{job_id}: Expected environment {name!r}, found {actual!r}. Fix the reference; GitHub can create a misspelled environment without protection rules. Confirm this App's rule is enabled in GitHub.")
            continue

        triggers = workflow.get("on")
        events = set(triggers) if isinstance(triggers, dict) or (isinstance(triggers, list) and all(isinstance(event, str) for event in triggers)) else {triggers} if isinstance(triggers, str) else set()
        if events != {"workflow_dispatch"}:
            errors.append(f"GL_DISPATCH_TRIGGER: {filename}: Use only workflow_dispatch; automatic triggers can run expensive work before approval.")
        dispatch = triggers.get("workflow_dispatch") if isinstance(triggers, dict) else None
        inputs = dispatch.get("inputs", {}) if isinstance(dispatch, dict) else {}
        if not isinstance(inputs, dict):
            inputs = {}
        for name in INPUTS:
            entry = inputs.get(name)
            if not isinstance(entry, dict) or entry.get("type") != "string" or str(entry.get("required")).lower() != "true":
                errors.append(f"GL_DISPATCH_INPUT: {filename}: {name} must be a required string input. Restore it from the dispatch example.")
        for name, entry in inputs.items():
            if name not in INPUTS and isinstance(entry, dict) and str(entry.get("required")).lower() == "true":
                errors.append(f"GL_DISPATCH_INPUT: {filename}: Extra required input {name!r} is not supplied by Greenlight. Make it optional or remove it.")
        if workflow.get("run-name") != "Greenlight ${{ inputs.greenlight_check_id }}":
            errors.append(f"GL_DISPATCH_NAME: {filename}: Restore run-name: Greenlight ${{{{ inputs.greenlight_check_id }}}} so results can be associated with approval.")
        checkouts = 0
        for job_id, job in jobs.items():
            if "uses" in job:
                errors.append(f"GL_DISPATCH_REUSABLE: {filename}/{job_id}: Reusable workflow jobs need separate approved-SHA validation; this validator cannot inspect the called workflow.")
            if "environment" in job:
                errors.append(f"GL_DISPATCH_ENVIRONMENT: {filename}/{job_id}: Remove the environment gate from the dispatch workflow to avoid a second approval or plan restriction.")
            steps = job.get("steps", [])
            if not isinstance(steps, list) or any(not isinstance(step, dict) for step in steps):
                errors.append(f"GL_STEPS: {filename}/{job_id}: Steps must be a list of mappings.")
                continue
            for step in steps:
                uses = step.get("uses", "")
                if not isinstance(uses, str) or not uses.startswith("actions/checkout@"):
                    continue
                checkouts += 1
                options = step.get("with", {})
                if not isinstance(options, dict):
                    options = {}
                if options.get("ref") != "${{ inputs.greenlight_sha }}":
                    errors.append(f"GL_DISPATCH_CHECKOUT: {filename}/{job_id}: Checkout must use ref: ${{{{ inputs.greenlight_sha }}}}, not the default branch or another ref.")
                if str(options.get("persist-credentials")).lower() != "false":
                    errors.append(f"GL_DISPATCH_CREDENTIALS: {filename}/{job_id}: Set persist-credentials: false on checkout.")
        if not checkouts:
            errors.append(f"GL_DISPATCH_CHECKOUT: {filename}: No approved-commit checkout found. Restore the dispatch example's checkout steps.")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository checkout directory")
    parser.add_argument("--config", type=Path, default=Path("greenlight-workflows.json"))
    args = parser.parse_args()
    try:
        config = json.loads((args.root / args.config).read_text())
        errors = check_workflows(args.root, config)
    except (OSError, UnicodeError, ValueError) as error:
        errors = [f"GL_CONFIG: Could not read validator configuration: {error}"]
    for error in errors:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            escaped = error.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            print(f"::error title=Greenlight workflow validation::{escaped}")
        else:
            print(error, file=sys.stderr)
    if errors:
        return 1
    print("Greenlight workflow contracts passed. Verify enabled protection rules, App permissions, and the deployed default-branch workflow separately.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
