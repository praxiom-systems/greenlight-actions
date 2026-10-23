# Choosing an approval mode

Greenlight supports two ways to approve expensive CI work. Both wait without
using a runner. Your workflow must be prepared for the selected mode.

| Mode | Public repositories | Private/internal repositories | What happens |
| --- | --- | --- | --- |
| Environment | All GitHub plans | GitHub Enterprise | GitHub pauses an existing PR job; Greenlight approves it |
| Dispatch | All GitHub plans | All GitHub plans, including Free | Greenlight starts a configured workflow after approval |

## Automatic selection

The default is `auto`. When a PR opens or receives a commit, Greenlight:

1. Checks whether its custom protection rule is enabled on the `greenlight`
   environment. If it is, Greenlight chooses environment mode.
2. Otherwise, looks for an active `.github/workflows/greenlight-ci.yml` workflow
   on the default branch. If it exists, Greenlight chooses dispatch mode.
3. If neither is ready, publishes **Greenlight Actions: Setup** with instructions
   for completing setup. No fallback workflow is started.

The setup check records the selected mode for that commit. Adding/removing an
environment rule later does not switch the same commit to another flow. Push a
new commit to select a different mode. A setup failure does not lock a mode;
after correcting setup, comment `/greenlight` to check again.

Only routing records created by this GitHub App are trusted; another App's
same-named check cannot select a mode. The record must also match the current
commit. If the record is missing or malformed, Greenlight checks readiness again
and writes a new record. Retain these checks: changing setup after losing a
record can select a different flow for the same commit. Use a new commit when
changing modes rather than removing checks.

If overlapping deliveries create several valid records, the earliest check ID
wins; Greenlight checks again before routing work. This makes ordering
deterministic but is not an atomic lock against simultaneous selection updates.

An access-denied response asks you to check installation permissions. A network,
rate-limit, or server error asks you to retry. Greenlight does not infer your
subscription from every API error or start fallback CI during an outage.

Automatic selection checks GitHub metadata, not repository file contents. It
cannot verify that your YAML references the environment or contains the dispatch
inputs. Use the matching example below. An enabled environment rule takes
precedence even when a dispatch workflow also exists; disable an unused rule or
ask the App operator to set an explicit dispatch override.

## Environment mode

Use this to keep your normal PR workflow, event context, merge-commit checkout,
job checks, and workflow links. Private/internal repositories require Enterprise
for the custom protection rule.

Native mode retains `/greenlight` approval for fork PRs when GitHub delivers the
native gate request and the commenter has write, maintain, or admin access. The
same-repository restriction below applies to dispatch mode.

1. Install Greenlight on the repository.
2. Open **Settings > Environments**, create/open `greenlight`, enable Greenlight
   Actions under **Deployment protection rules**, and save. You need permission
   to manage environments; merely creating an environment does not enable a rule.
3. Add `environment: greenlight` to each job you want to gate.

```yaml
on:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    environment: greenlight
    steps:
      - uses: actions/checkout@v4
      # Your existing test steps go here.
```

See the complete [environment example](../examples/environment-ci.yml), including
how to leave post-merge pushes ungated. Click **Run CI** on the PR check or comment
`/greenlight` when ready. GitHub's job checks report the actual CI results; the
Greenlight approval check means approval was accepted.

An environment-only workflow cannot automatically become a dispatch workflow.
Installing Greenlight does not rewrite YAML or bypass GitHub's plan restrictions.

## Dispatch mode

Use this for private repositories on GitHub Free, Pro, or Team, or when you prefer
to create CI runs only after approval.

1. Install Greenlight on the repository.
2. Copy [the complete dispatch example](../examples/dispatch-ci.yml) to
   `.github/workflows/greenlight-ci.yml` on the **default branch**.
3. Replace the demo test command with your actual CI steps. Keep all three inputs,
   the exact `run-name`, input validation, checkout of `greenlight_sha`, and checkout
   verification.
4. Remove `environment: greenlight` and automatic `push`/`pull_request` triggers
   from this expensive workflow. Keep quick automatic checks in a separate file.
5. Open a same-repository PR. Click **Run CI** or comment `/greenlight` to approve
   the current commit. If setup was just fixed on an existing PR, `/greenlight`
   rechecks it and can create the approval checks before starting CI.

You will see:

- **Setup:** the selected mode and setup guidance; this does not mean tests passed.
- **Run CI:** the approval button, neutral before approval and successful after
  approval is accepted.
- **Dispatch CI:** queued before approval, in progress while running, then the
  actual workflow result. Where your plan supports required checks, require this
  result check rather than the approval/setup checks.

The workflow definition comes from the default branch and checks out the exact
approved PR head SHA. It does not use the normal `pull_request` event payload or
GitHub's synthetic merge commit. Workflows using `github.event.pull_request`, PR
merge refs, or workflow-definition changes on a PR need adaptation.

## Explicit overrides for App operators

Self-hosted App operators can set `GREENLIGHT_REPOSITORIES` in the Worker's
configuration. Keys are `owner/repository`, matched case-insensitively:

```json
{
  "owner/public-repo": {"mode": "environment", "environment": "greenlight"},
  "owner/private-repo": {"mode": "dispatch", "workflow": "heavy-ci.yml"},
  "owner/another-repo": {"mode": "auto"}
}
```

An environment override reports missing gate setup instead of selecting dispatch.
A dispatch override skips the native capability probe. Custom workflow values
are filenames, not paths; custom environment names use letters, digits, hyphens,
underscores, or dots. Existing `DISPATCH_WORKFLOWS` entries remain explicit
dispatch overrides unless replaced by a `GREENLIGHT_REPOSITORIES` entry.

This is App configuration, not an Actions job variable. Hosted users using the
conventional names do not need to configure the App backend.

## Troubleshooting and limits

- **Setup needed:** finish the matching setup and retry `/greenlight`.
- **No setup or approval check appears:** ask the App operator to verify the
  installation and the **Pull request**, **Deployment protection rule**,
  **Check run**, **Issue comment**, and **Workflow run** subscriptions. The App
  cannot inspect or diagnose an event GitHub never delivers. After correcting
  subscriptions, redeliver the missed webhook or push a new commit.
- **Could not verify setup:** check App permissions or wait for GitHub to recover.
  A 403/404 response alone is not proof of a particular subscription.
  Failures reading or saving the routing check also stop approval. Greenlight
  tries to publish temporary-error guidance; if the Checks API is unavailable,
  that message may be impossible to publish. Operators can inspect Worker logs
  and retry `/greenlight` after recovery.
- **Configuration conflict:** the commit already selected another mode. A native
  gate request conflicting with dispatch is rejected with instructions rather
  than approved as a second flow. Correct the workflow and push a new commit.
- **Native job waits without an approval check:** confirm it belongs to a PR.
  Requests without a PR SHA or callback URL are ignored with a Worker warning;
  the App cannot associate an approval with them. Use the environment example's
  conditional gate to leave post-merge pushes ungated.
- **Dispatch rejected:** confirm the workflow is on the default branch, active,
  and accepts `greenlight_sha`, `greenlight_pr`, and `greenlight_check_id` inputs.
  Metadata discovery cannot verify these declarations before dispatch.
- **Dispatch could not be confirmed:** inspect Actions before trying again; a
  timeout can occur after GitHub accepted the request. A late completion event
  can still update the result.
- **Result stuck in progress:** make sure the App receives **Workflow run** events;
  redeliver a missed completion event from the App's webhook settings.
- Fork PRs and merge queues are not supported by this dispatch implementation.
- Same-SHA reruns do not reset an already-finished dispatch result yet. Use a new
  commit for a fresh approval.
- Sequential duplicate commands are ignored. Simultaneous approvals/webhooks are
  not protected by an atomic lock; workflow concurrency bounds parallel work but
  does not guarantee exactly-once execution. Before dispatch, Greenlight checks
  its approval is still neutral and its associated result is still queued, then
  marks the result in progress. This blocks sequential retries; two requests
  can still both read the queued state before either updates it. An atomic
  idempotency mechanism is required to prevent that race.
- GitHub Free private repositories can run CI, but required-check enforcement
  through protected branches is a separate plan-dependent feature.

## GitHub references

- [Custom deployment protection rule requirements](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/configure-custom-protection-rules)
- [Workflow dispatch API and permissions](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event)
- [Manual workflow default-branch requirements](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
- [Protected branch availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
