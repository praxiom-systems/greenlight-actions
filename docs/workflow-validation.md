# Checking intended workflow gates

`environment: greenligth` is valid YAML. GitHub can create that environment
automatically without protection rules, allowing the job to run without the
approval you intended. [GitHub documents implicit environment creation](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments#creating-an-environment).

The hosted App checks metadata and does not read your workflow files. If the
correct environment exists but a job references another one, discovery alone
cannot identify that typo. A warning on a check does not stop a job that GitHub
has already started.

## Run an optional validator in your repository

Copy [validate-workflows.py](../scripts/validate-workflows.py) into your repository
at `scripts/validate-workflows.py`. It reads explicitly selected local files,
does not execute them, and makes no network requests. It adds no hosted App
permissions.

Create `greenlight-workflows.json` and declare the intended gated jobs:

```json
{
  "workflows": {
    ".github/workflows/pr-checks.yml": {
      "mode": "environment",
      "jobs": {
        "integration": "ci-approval"
      }
    }
  }
}
```

`integration` is the YAML job ID, not its display name. `ci-approval` is an
example custom environment, not a required name. Match its enabled Greenlight
protection rule in GitHub and coordinate any [App operator override](approval-modes.md#explicit-overrides-for-app-operators).
Conventional installations can use `greenlight` instead. Other jobs, such as
quick linting and ordinary deployments, are left alone.

The validator accepts literal names, `environment: {name: ...}`, and this
specific conditional used in the examples:

```yaml
environment: ${{ github.event_name == 'pull_request' && 'ci-approval' || '' }}
```

Names are compared without case sensitivity, as GitHub does. Arbitrary matrix
and other expressions cannot be evaluated locally: these produce a diagnostic
instead of a false pass. Validate such configurations separately.

For dispatch, declare the file without an environment jobs map:

```json
{
  "workflows": {
    ".github/workflows/greenlight-ci.yml": {
      "mode": "dispatch"
    }
  }
}
```

The [combined configuration example](../examples/workflow-validation.json) shows
both forms. Adjust filenames and job IDs and remove unused entries.

Run it locally or add these steps to an **existing automatic quick-check job**:

```yaml
- name: Install workflow validator dependency
  run: python3 -m pip install PyYAML
- name: Validate intended Greenlight workflows
  run: python3 scripts/validate-workflows.py --config greenlight-workflows.json
```

Check out the repository first and use Python 3.9 or newer. No GitHub token is
needed by the validator. Pin dependencies under your project's own policy.
Failures exit with status 1 and create error annotations in GitHub Actions.
Putting this only inside the gated job cannot provide feedback while it waits.
It does not create another App check or require a separate validation job.

## Diagnostics

| Diagnostic | Meaning and fix |
| --- | --- |
| `GL_CONFIG` | Invalid/empty configuration or invalid path. Declare intended workflow files and jobs explicitly. |
| `GL_WORKFLOW_MISSING` | File is absent in this checkout. Correct the filename or add it. |
| `GL_YAML`, `GL_JOBS`, `GL_STEPS` | Malformed YAML, duplicate keys, or invalid job/step structure. Correct the workflow. |
| `GL_JOB_MISSING` | Intended gated job was removed or renamed. Update the contract deliberately or restore the job. |
| `GL_ENV_MISMATCH` | Missing/wrong environment on an intended job. Match the expected name and verify its protection rule in GitHub. |
| `GL_ENV_DYNAMIC` | Expression cannot be verified. Use a supported reference or validate it separately. |
| `GL_DISPATCH_TRIGGER` | Missing `workflow_dispatch` or extra automatic triggers. Restore dispatch-only triggering. |
| `GL_DISPATCH_INPUT` | Missing/wrong Greenlight input or an extra required input. Restore the three required string inputs. |
| `GL_DISPATCH_NAME` | Run name cannot correlate with the result check. Restore the template's `run-name`. |
| `GL_DISPATCH_ENVIRONMENT` | Dispatch job also references an environment. Remove that gate to avoid a second approval/plan restriction. |
| `GL_DISPATCH_CHECKOUT`, `GL_DISPATCH_CREDENTIALS` | Missing/wrong approved-SHA checkout or persisted credentials. Restore the template's checkout. |
| `GL_DISPATCH_REUSABLE` | Called workflow needs separate approved-SHA validation; this script does not inspect it. |

This is an accidental-configuration check, not an enforcement boundary or a
complete workflow linter. It does not validate arbitrary shell/test logic, prove
that input-validation commands are correct, verify protection rules in GitHub,
or prove which workflow revision GitHub will execute. Someone able to edit both
the workflow and contract can change their intended behavior. Keep the dispatch
example's input validation and checkout verification. Use a workflow linter
alongside this check for general Actions syntax.

## App-side setup messages

The App uses its existing permissions to distinguish:

- A missing/inaccessible configured environment or rule from a confirmed
  environment response with no enabled rule belonging to this App.
- A missing/inaccessible dispatch workflow from a disabled workflow or a
  response pointing to the wrong configured path.
- Permission errors from temporary network, rate-limit, or server errors.
- A dispatch rejected because of access, a missing workflow/ref, or invalid
  configuration. HTTP 422 can have several causes; guidance lists the trigger,
  required inputs, and default-branch ref to check.

HTTP 404 may conceal access or feature-availability problems; it does not prove
absence or identify a subscription plan. For ambiguous dispatch errors, inspect
Actions before retrying because GitHub might have accepted the request. The App
does not automatically retry an uncertain dispatch.

Healthy metadata discovery adds no setup check. Fix the reported setup and
retry `/greenlight` where instructed. After a dispatch attempt finishes with an
error, follow its instructions and push a new commit for fresh approval.

The App's metadata warning cannot diagnose a job's misspelled environment; use
the repository-side validator for intended references. Neither can prevent an
ungated job that has already started. Configure GitHub protection rules and any
required checks for the guarantees you need.
