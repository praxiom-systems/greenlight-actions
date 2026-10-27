# Choose which CI jobs wait for approval

Push intermediate changes without repeatedly starting expensive builds, integration tests, or jobs that call paid services. Leave linting and quick tests automatic, and hold the heavy work until you need its results.

Click **Run CI** on the PR or comment `/greenlight`. Each new commit needs fresh approval. Waiting uses no runner minutes.

## How it works

- **Environment mode:** GitHub pauses gated jobs until approval. Supports public repos on all plans and private/internal repos on Enterprise. Enable Greenlight's protection rule on the `greenlight` environment and reference it in your jobs.
- **Dispatch mode:** No workflow run starts until approval. Supports public and private repos on all plans. Add the dispatch workflow on your default branch; it checks out the approved PR commit. Currently supports same-repository PRs, without fork PRs, merge queues, or same-commit reruns.

Install the App and configure your workflow using the guide below. Greenlight selects between configured modes and shows instructions when setup needs attention. Installing the App alone doesn't change your workflow triggers.

GitHub already offers manual workflows and environment approvals. Greenlight adds PR buttons, comment commands, and commit-specific approval without maintaining your own approval scripts. Results stay in GitHub checks. Approval requires repository write access or higher.

The App is free for personal projects and teams. It reads GitHub metadata, not source files or repository secrets. Normal Actions quotas and billing apply when jobs run. Standard public-repo runners are already free; savings depend on your runners and paid services.

[Setup, examples, and limitations](https://github.com/praxiom-systems/greenlight-actions/blob/main/docs/approval-modes.md)
