# Run expensive CI when you're ready

Greenlight Actions adds a **Run CI** button to your pull request. Click it or comment `/greenlight` when you're ready for the heavy work to run.

Keep linting and quick tests automatic. Hold longer builds, integration tests, or jobs that use paid services until you need them. Waiting uses no runner minutes, and each new commit needs fresh approval.

**Free for personal projects and teams, including private repositories on GitHub Free through dispatch mode.**

## How it works

- **Environment mode:** GitHub pauses gated jobs until approval. Supports public repos on all plans and private/internal repos on Enterprise. Enable Greenlight's protection rule on the `greenlight` environment and reference it in your jobs.
- **Dispatch mode:** No workflow run starts until approval. Supports public and private repos on all plans. Add the dispatch workflow on your default branch; it checks out the approved PR commit. Currently supports same-repository PRs, without fork PRs, merge queues, or same-commit reruns.

Greenlight selects between configured modes and shows instructions when setup needs attention. You still need to configure your workflow; installing the App alone doesn't change its triggers.

GitHub already offers manual workflows and environment approvals. Greenlight adds PR buttons, comment commands, and commit-specific approval without maintaining your own approval scripts. Results stay in GitHub checks. Approval requires repository write access or higher.

The App reads GitHub metadata, not source files or repository secrets. Normal Actions quotas and billing apply when jobs run. Standard public-repo runners are already free; savings depend on your runners and paid services.

[Setup, examples, and limitations](https://github.com/praxiom-systems/greenlight-actions/blob/main/docs/approval-modes.md)
