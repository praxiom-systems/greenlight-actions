# Developer community drafts

These files are local publishing copy and notes. Saving or merging them does not publish to any community.

## Reddit

Paste [reddit-github.md](reddit-github.md) as a comment in the current pinned r/github project-promotion megathread. Paste [reddit-devops.md](reddit-devops.md) in r/devops' current pinned weekly self-promotion thread. These are replies, so they don't need titles. Check the current threads and rules before posting.

Copy and paste one at a time, from the repository root:

```sh
xclip -selection clipboard < docs/outreach/reddit-github.md
```

```sh
xclip -selection clipboard < docs/outreach/reddit-devops.md
```

## DEV Community

Suggested title: **Keeping quick checks automatic while approving expensive GitHub Actions jobs**

Suggested tags: `showdev`, `github`, `devops`, `tutorial`.

[dev-walkthrough.md](dev-walkthrough.md) contains the article body only. Enter the title separately. Review the Node example against your own setup and use DEV's AI-assistance disclosure controls as appropriate; the draft also includes a disclosure sentence.

The draft includes the banner and two environment-mode screenshots from the
published article, linked to this repository's assets using absolute raw URLs
so the images render when the Markdown is pasted into DEV.

```sh
xclip -selection clipboard < docs/outreach/dev-walkthrough.md
```

## Show HN

[show-hn-notes.md](show-hn-notes.md) is an outline to write from, not a post to paste. HN requires you to write the submission yourself. Copy these notes into your own editor if useful:

```sh
xclip -selection clipboard < docs/outreach/show-hn-notes.md
```

## Other clipboard tools

On macOS, replace `xclip -selection clipboard` with `pbcopy`. On Wayland, use `wl-copy` if wl-clipboard is installed.

## Community references

- [r/github project thread](https://www.reddit.com/r/github/comments/1jy8rea/promote_your_projects_here_selfpromotion/)
- [r/devops rules](https://www.reddit.com/r/devops/about/rules.json)
- [DEV Show DEV](https://dev.to/t/showdev)
- [DEV's AI disclosure announcement](https://dev.to/devteam/introducing-ai-disclosure-on-dev-tools-for-nuance-clarity-and-better-feeds-34mk)
- [Show HN guidelines](https://news.ycombinator.com/showhn.html)
