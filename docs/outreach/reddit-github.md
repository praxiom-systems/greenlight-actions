I built **Greenlight Actions** because I wanted a more refined setting for CI than just running everything on every push.

It adds a **Run CI** button to the PR, or you can comment `/greenlight`. You can pick which jobs wait for approval and leave quick checks running all the time. Each new commit needs fresh approval, and waiting doesn't use runner minutes.

What it does is already doable in GitHub technically. This just makes it directly accessible from the PR without maintaining your own comment-trigger scripts.

It supports environment gates where available, or dispatch mode for private repos on GitHub Free as well. The app is free; there is some workflow setup involved.

[Repo and setup](https://github.com/praxiom-systems/greenlight-actions) · [GitHub Marketplace](https://github.com/marketplace/greenlight-actions)

I'd welcome feedback, especially on the setup instructions.
