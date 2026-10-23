"""Check the setup contracts users rely on when copying workflow examples."""

from pathlib import Path

import yaml


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name):
    # BaseLoader preserves GitHub's YAML key `on` instead of treating it as a bool.
    path = Path(__file__).resolve().parent.parent / "examples" / name
    return yaml.load(path.read_text(), Loader=yaml.BaseLoader)


def validate():
    dispatch = load("dispatch-ci.yml")
    require(set(dispatch["on"]) == {"workflow_dispatch"},
            "Dispatch CI must run only after an explicit workflow dispatch")
    inputs = dispatch["on"]["workflow_dispatch"]["inputs"]
    for name in ("greenlight_sha", "greenlight_pr", "greenlight_check_id"):
        require(inputs[name]["required"] == "true" and inputs[name]["type"] == "string",
                f"Dispatch input {name} must be a required string")
    require(dispatch["run-name"] == "Greenlight ${{ inputs.greenlight_check_id }}",
            "Dispatch run name must allow the App to correlate the result check")
    require(dispatch["permissions"] == {"contents": "read"},
            "Dispatch CI must request only read access to repository contents")
    checkouts = []
    for job in dispatch["jobs"].values():
        require("environment" not in job,
                "Dispatch CI must work without a protected environment")
        for step in job.get("steps", []):
            if step.get("uses", "").startswith("actions/checkout@"):
                checkouts.append(step)
                require(step["with"].get("ref") == "${{ inputs.greenlight_sha }}",
                        "Dispatch CI must check out the approved commit")
                require(step["with"].get("persist-credentials") == "false",
                        "Dispatch checkout must not persist credentials")
    require(checkouts, "Dispatch CI must check out the approved commit")

    native = load("environment-ci.yml")
    require(set(native["on"]) == {"pull_request", "push"},
            "Native CI must handle pull requests and pushes")
    for job in native["jobs"].values():
        require(job.get("environment") ==
                "${{ github.event_name == 'pull_request' && 'greenlight' || '' }}",
                "Native CI must gate pull requests on the greenlight environment")
    print("Workflow example contracts passed")


if __name__ == "__main__":
    validate()
