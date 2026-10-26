# Publishing the Marketplace listing

[marketplace-listing.md](marketplace-listing.md) contains only the public long description. Copy the entire file into the Marketplace description editor. Its links are absolute so they work outside this repository. Updating this file does not publish changes to Marketplace.

## Copy the description

From the repository root, use one of these commands.

Linux with X11:

```sh
xclip -selection clipboard < docs/marketplace-listing.md
```

macOS:

```sh
pbcopy < docs/marketplace-listing.md
```

Linux with Wayland and wl-clipboard installed:

```sh
wl-copy < docs/marketplace-listing.md
```

## Short description

Paste this into the short description field:

```text
Run expensive CI when you're ready. Approve from your PR and keep quick checks automatic.
```

## Free plan

Use these values when editing the free plan:

- **Name:** Free
- **Description:** Free for personal projects and teams. Run expensive CI when you're ready.
- **Features:** PR approval button; `/greenlight` comment command; environment and dispatch modes; private repositories on GitHub Free through dispatch.

Confirm the plan is available to both personal accounts and organizations. Remove personal-use-only wording and the claim that every setup needs only one line of YAML.

## Resource links

- **Documentation:** <https://github.com/praxiom-systems/greenlight-actions#readme>
- **Support:** <https://github.com/praxiom-systems/greenlight-actions/blob/main/SUPPORT.md>
- **Privacy policy:** <https://github.com/praxiom-systems/greenlight-actions/blob/main/PRIVACY.md>
- **Terms of Service:** Replace the current link to `SECURITY.md` with the actual published terms. This repository currently has no Terms of Service document; do not relabel the security policy as terms.

## Screenshots and release checks

- Confirm the matching backend is deployed and the production App has the webhook subscriptions and permissions described in the [README](../README.md#security-and-permissions).
- Keep environment screenshots labeled as environment mode. Environment setup must show the enabled Greenlight protection rule, not just an environment with the right name.
- Add a dispatch screenshot showing the Run CI approval and Dispatch CI result checks, and label it as working with private repos on GitHub Free.
- Preview the Markdown, verify links, and check that both account types can select the free plan before publishing.
- Revisit the [live listing](https://github.com/marketplace/greenlight-actions) after saving; repository edits do not update its description or plan settings automatically.
