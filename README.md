<p align="center">
  <img src="assets/icon/greenlight-icon-256.png" alt="Greenlight Actions icon" width="128">
</p>

<h1 align="center">Greenlight Actions</h1>

Run expensive CI when you're ready. Keep pushing without starting every job on every commit.

[Install Greenlight](https://github.com/apps/greenlight-actions) · [Approval modes and setup](docs/approval-modes.md) · [Support](SUPPORT.md)

Greenlight adds a **Run CI** button to your PR. Click it or comment `/greenlight` to approve work on the current commit. Keep quick checks automatic and hold expensive builds or tests until you want them to run. Waiting does not consume runner minutes.

**Release status:** the dual-mode instructions in this branch require the matching backend update and App webhook subscriptions. The existing hosted environment gate continues to work; dispatch and automatic selection must be deployed before hosted users can use the new setup.

## Two Approval Modes

| Mode | How It Works | Repository Support |
| --- | --- | --- |
| **Environment** | Your PR workflow starts, and GitHub pauses gated jobs until approval | Public repos on all plans; private/internal repos on Enterprise |
| **Dispatch** | Greenlight creates the workflow run only after approval | Public and private repos on all plans, including GitHub Free |

Dispatch has been tested live in a **private repository on GitHub Free**, using both the browser button and PR comment, with passing and failing results. It uses ordinary workflow dispatch APIs rather than deployment protection rules.

**The App is free.** Standard GitHub-hosted runners are already free for public repositories. Greenlight still reduces unnecessary work, check noise, and runner usage; monetary savings depend on paid larger runners, your own infrastructure, or external services used by your jobs. Normal GitHub Actions quotas and billing still apply when CI runs. See [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions).

## Automatic Selection and Setup Guidance

Greenlight defaults to `auto`:

1. Prefer the `greenlight` environment if this App's custom protection rule is enabled.
2. Otherwise, discover an active `.github/workflows/greenlight-ci.yml` dispatch workflow.
3. If neither is ready, show **Greenlight Actions: Setup** with instructions.

Selection is kept for the current commit. GitHub errors do not silently start a different flow. Permission problems and temporary outages get different guidance; a missing environment is not treated as proof of a subscription plan.

Your YAML must support the chosen mode. The App checks GitHub metadata, never reads source files, and cannot rewrite an environment-only workflow into a dispatch workflow. See the [mode guide](docs/approval-modes.md) for explicit overrides, conflicts, and setup recovery.

## Get Started

### Environment Mode

Use this for public repos on any plan, or private/internal repos on Enterprise.

1. [Install Greenlight](https://github.com/apps/greenlight-actions) on the repository.
2. In **Settings > Environments**, create/open `greenlight`, enable Greenlight Actions under **Deployment protection rules**, and save. Creating an environment alone does not enable a protection rule.
3. Add the environment to the jobs you want to gate:

```yaml
on:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    environment: greenlight
    steps:
      - uses: actions/checkout@v4
      # Your existing test steps stay here.
```

Open a PR, then click **Run CI** or comment `/greenlight`. Each new push creates a new gate. Normal PR event data, checkout behavior, job checks, and workflow links remain available.

See the [complete environment example](examples/environment-ci.yml), including leaving post-merge pushes ungated. Installing a free App does not bypass GitHub's Enterprise requirement for private/internal custom protection rules. [GitHub's requirements](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/configure-custom-protection-rules)

### Dispatch Mode

Use this for private repos on Free, Pro, or Team, or to create runs only after approval.

1. Install Greenlight on the repository.
2. Copy the [dispatch example](examples/dispatch-ci.yml) to `.github/workflows/greenlight-ci.yml` on the **default branch**.
3. Replace the demo test step with your real tests. Keep the three Greenlight inputs, exact run name, input validation, and approved-SHA checkout.
4. Leave the expensive workflow triggered only by `workflow_dispatch`, with no `environment: greenlight`. Keep fast automatic checks in another workflow.
5. Open a same-repository PR and click **Run CI** or comment `/greenlight`.

Greenlight shows a separate approval check and CI result check. **Run CI** means approval was accepted; **Dispatch CI** reports whether tests actually passed. A new commit needs fresh approval. After correcting setup, `/greenlight` can recheck an existing PR without another push.

The workflow definition runs from the default branch and checks out the exact approved PR head. Workflows depending on `github.event.pull_request`, synthetic merge commits, or PR changes to the workflow definition need adaptation. Read the [dispatch setup and limitations](docs/approval-modes.md#dispatch-mode) before migrating.

## Why Use Greenlight?

- Push intermediate commits without repeatedly starting expensive jobs.
- Keep linting and quick tests automatic while approving heavy work from the PR.
- Use a button or `/greenlight` rather than maintaining approval scripts.
- Use native environment gates where supported and dispatch on Free private repos.
- Get setup guidance when the expected gate or dispatch workflow is missing.

GitHub already offers manual workflows and native environment approvals. Greenlight packages PR buttons, comment commands, mode selection, and setup guidance around those features. Both modes wait without using a runner.

## Security and Permissions

The hosted App has no database or app-owned file storage. It reads GitHub metadata and stores check status plus small routing records in GitHub check runs: commit SHA, workflow/environment names, identifiers, and the selected mode. It does not read, clone, or store source files or repository secrets. It does not log comment bodies or webhook payloads.

### Permissions Explained

| Permission | Access | Purpose |
| --- | --- | --- |
| Checks | Read & Write | Create approval, setup, and result checks; record mode selection in GitHub |
| Actions | Read & Write | Inspect rules and workflow metadata, dispatch workflows, read results, approve protection rules |
| Deployments | Read & Write | Handle native deployment protection rules |
| Issues | Read | Receive PR conversation comments for `/greenlight` |
| Pull Requests | Read | Read current PR metadata and associate approval with a commit |

The App uses **Pull request**, **Deployment protection rule**, **Check run**, **Issue comment**, and **Workflow run** webhook events. Existing registrations need the Pull request and Workflow run subscriptions added for automatic/dispatch mode. Approve any pending permission updates on the installation. The development App also needs Deployments permission and the protection-rule event to test environment mode.

Buttons and comment commands require write, maintain, or admin repository permission. `/greenlight run` also works. Regular issue comments and non-matching commands are ignored. See [privacy](PRIVACY.md) and [security](SECURITY.md).

## FAQ

**Does Greenlight require Enterprise?**
Only the environment gate requires Enterprise for private/internal repos. Dispatch works in Free private repos. Public repositories support both modes on all plans.

**Can it switch my existing workflow automatically?**
It selects between configured modes and explains missing setup. It cannot change your YAML. An environment-only workflow needs adaptation before dispatch can replace it.

**Why does the setup check say it cannot verify access?**
Check the App installation and permission updates. Access errors, missing setup, and outages are different conditions; the message describes what could be verified. Fix setup and retry `/greenlight`.

**Does it work with forks?**
Greenlight currently supports PRs from branches in the same repository. Fork PRs are not supported.

**Can I gate several jobs?**
Environment mode gates jobs referencing the environment. Dispatch approves one configured workflow per repository, and that workflow can contain multiple jobs.

**What if nobody approves?**
Dispatch creates no workflow run. Environment jobs wait without runner usage until approved, cancelled, or timed out; GitHub allows up to 30 days for environment approval, subject to overall workflow limits. [GitHub Actions limits](https://docs.github.com/en/actions/reference/limits)

**Are there dispatch limitations?**
Same-SHA reruns, fork PRs, and merge queues are not supported by this implementation. Sequential duplicate commands are ignored, but simultaneous approvals are not protected by an atomic lock. See the [full limitations](docs/approval-modes.md#troubleshooting-and-limits).

**How do I remove it?**
Remove the environment gate or restore the triggers you want on a dispatch workflow, then uninstall the App. Existing check runs remain subject to GitHub retention.

## Support and License

Built and maintained by [Praxiom Systems LLC](https://praxiomsystems.com/). See [support](SUPPORT.md), [privacy](PRIVACY.md), [security](SECURITY.md), and the [MIT license](LICENSE).
