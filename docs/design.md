# Design Notes

Reviewpack generates structured context packs for AI-assisted pull request review.

It is not designed to be another automatic AI reviewer. Instead, it acts as a context layer between raw pull request data and the reviewer.

## Problem

Pull request review quality depends heavily on context.

Direct AI review often starts from a raw diff. That can be useful for small changes, but it often misses project-level signals:

- Whether tests were updated
- Whether documentation was updated
- Whether dependencies changed
- Whether CI or deployment files changed
- Whether high-risk paths were touched
- Whether the pull request is too large
- What the maintainer should review first

Human reviewers also spend time collecting this context manually.

Reviewpack prepares this context before review starts.

## Core workflow

Direct AI review:

    PR diff -> AI -> review comments

Reviewpack workflow:

    PR data -> local analysis -> structured context pack -> human or AI review

The goal is not to replace the reviewer.

The goal is to improve the review input.

## Reviewpack as a context layer

Reviewpack converts scattered pull request information into reusable review artifacts:

- Human-readable Markdown
- Machine-readable JSON
- AI-ready prompts
- Risk checklists
- Review focus areas

These artifacts can be used by:

- Human maintainers
- New contributors
- Codex
- Cursor
- Cline
- OpenCode
- Claude Code
- GitHub Copilot
- Other AI coding tools

## Deterministic first

The first version of Reviewpack uses deterministic rules instead of AI calls.

This keeps the tool:

- Fast
- Local
- Predictable
- Cheap to run
- Easy to test
- Safe by default

Examples of deterministic signals:

- Source changed without tests
- Source changed without docs
- Dependency files changed
- CI workflow changed
- Infrastructure files changed
- Configured high-risk paths changed
- Large pull request
- Large line change

## AI-ready, not AI-required

Reviewpack can generate an AI review prompt without calling any AI provider.

This lets users copy the prompt into their preferred AI coding tool while keeping Reviewpack itself local and provider-neutral.

Future versions may support optional AI providers, but AI should remain disabled by default.

## Configuration

Projects should be able to customize Reviewpack with a .reviewpack.yml file.

Example configuration areas:

- High-risk paths
- Test paths
- Documentation paths
- Large PR thresholds
- Privacy controls
- Optional AI provider settings

## Non-goals

Reviewpack does not aim to:

- Automatically approve PRs
- Automatically merge PRs
- Replace maintainers
- Become a noisy line-by-line review bot
- Require AI provider tokens for basic use
- Upload code by default

## Design principles

1. Local-first
2. Privacy-first
3. AI-optional
4. Human-readable
5. Machine-readable
6. Maintainer-controlled
7. Tool-agnostic
8. Useful without network access
