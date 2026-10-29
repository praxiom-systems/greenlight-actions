**TL;DR:** I built **Greenlight Actions** so that you can give your CI runs a greenlight when you want.

I'm a seasoned backend/DevOps engineer. And I've run into this a lot of times: I want a more refined setting than just "run it on every push" or "never run it." Some CI providers make this easier than others. And I've found GitHub Actions to be pretty limited in this regard.

So, if you have GitHub Actions jobs that you want to hold off on running until you click one button or leave a comment, this app makes that easy. Click **Run CI** on the PR or comment `/greenlight`.

This avoids running expensive or annoying CI pipelines on every little push, while still giving you an easy way to run them within GitHub, using just the mouse or just the keyboard. Waiting for approval doesn't use runner minutes.

And you can pick and choose which pipelines to gate behind Greenlight vs. run all the time as well. Let's say you want quick lints or something else running on every push; you can still do so.

So, what Greenlight does is already doable in GitHub technically. This tool just makes it more intuitive and friction-free to run, and makes it directly accessible from the PR with a button or comment.

Depending on your GitHub plan, you can choose either:

- **Environment mode:** Public repos on any plan, or private/internal repos on Enterprise.
- **Dispatch mode:** Works for private repos on GitHub Free as well. Currently supports PRs from branches in the same repository.

The app is free. There is some workflow setup involved, and I've tried to make the [documentation](https://github.com/praxiom-systems/greenlight-actions) pretty comprehensive. But please let me know if you see any gaps. I welcome any feedback and suggestions.

You can install it from the [GitHub Marketplace](https://github.com/marketplace/greenlight-actions).
