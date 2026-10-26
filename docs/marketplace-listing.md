# Run expensive CI when you're ready

Keep pushing without starting every expensive job on every commit. Greenlight Actions adds a **Run CI** button to your pull request. Click it or comment `/greenlight` when you want the heavy work to run.

Keep linting and quick tests automatic, while longer builds, integration tests, and jobs that use paid services wait for approval. Waiting does not consume runner minutes. Each new commit needs fresh approval.

**The App is free for personal projects and teams. Dispatch mode supports private repositories on GitHub Free.**

## Why Greenlight?

- **Avoid unnecessary compute.** Push intermediate changes without repeatedly starting expensive jobs.
- **Reduce CI noise.** Run the heavy checks when you're ready to use their results.
- **Approve from the PR.** Use the Run CI button or `/greenlight`, with results shown in GitHub checks.
- **Keep fast feedback.** Leave quick checks running automatically and gate only the work you choose.

GitHub already offers manual workflows and environment approvals. Greenlight brings PR buttons, comment commands, approval tied to the current commit, automatic mode selection, and setup guidance together so you don't have to maintain your own approval scripts.

## Two ways to approve CI

### Environment mode

Your PR workflow starts, and GitHub pauses jobs that use the `greenlight` environment until you approve them. This keeps the normal PR workflow context and job checks.

Available for **public repositories on all GitHub plans**, and **private/internal repositories on Enterprise**.

### Dispatch mode

Greenlight creates the workflow run only after approval. The workflow uses its definition from the default branch and checks out the exact approved PR commit. Separate approval and result checks show whether approval was accepted and whether CI passed.

Available for **public and private repositories on all GitHub plans, including GitHub Free**. Dispatch currently supports PRs from branches in the same repository; fork PRs, merge queues, and same-commit reruns are not supported.

Greenlight automatically selects between the modes you've configured, preferring an enabled environment protection rule. If setup is missing or cannot be verified, it shows instructions on the PR's CI check. Healthy setup adds no separate setup check. The App does not rewrite your workflow YAML.

## Get started

1. [Install Greenlight Actions](https://github.com/apps/greenlight-actions) on your repository.
2. Configure the mode you want:
   - **Environment:** Create the `greenlight` environment, enable Greenlight Actions under its deployment protection rules, and add `environment: greenlight` to the jobs you want to gate.
   - **Dispatch:** Add the [dispatch workflow example](https://github.com/praxiom-systems/greenlight-actions/blob/main/examples/dispatch-ci.yml) as `.github/workflows/greenlight-ci.yml` on your default branch. Replace the demo tests while preserving the approval inputs, validation, run name, and approved-commit checkout. Keep the expensive workflow dispatch-only, without the `greenlight` environment gate.
3. Open a PR, then click **Run CI** or comment `/greenlight`.

Approvals require write, maintain, or admin repository permission. Installing the App alone does not change your existing workflow triggers.

See the [setup guide](https://github.com/praxiom-systems/greenlight-actions/blob/main/docs/approval-modes.md) for complete examples, permissions, and limitations.

## Cost and privacy

Greenlight is free. Normal GitHub Actions quotas and billing apply when your jobs run. Standard GitHub-hosted runners are already free for public repositories; savings depend on the runners, infrastructure, or paid services your jobs use.

The App reads GitHub metadata, not source files or repository secrets. It has no app-owned database or file storage; check status and small routing records are stored in GitHub check runs. See the [privacy policy](https://github.com/praxiom-systems/greenlight-actions/blob/main/PRIVACY.md) and [permission details](https://github.com/praxiom-systems/greenlight-actions#permissions-explained).

[Documentation](https://github.com/praxiom-systems/greenlight-actions#readme) · [Support](https://github.com/praxiom-systems/greenlight-actions/blob/main/SUPPORT.md)
