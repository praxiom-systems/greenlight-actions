I'm a backend/DevOps engineer, and I've worked with CI jobs that were expensive enough that running them on every commit added up quickly. Even in personal projects, having a bunch of jobs kick off on every little push gets annoying.

So I built **Greenlight Actions**. You can keep quick lints and tests automatic, and hold heavier jobs until you click **Run CI** on the PR or comment `/greenlight`. Waiting doesn't use runner minutes, and each new commit needs fresh approval.

It uses environment protection rules where supported, or workflow dispatch for private repos on GitHub Free too. The app is free, with some workflow setup required.

[Repo and setup](https://github.com/praxiom-systems/greenlight-actions) · [GitHub Marketplace](https://github.com/marketplace/greenlight-actions)

I'd be interested in how others handle this, and any gaps you see in the approach.
