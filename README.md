# Reviewpack

Privacy-first context packs for AI-assisted pull request review.

Reviewpack helps open-source maintainers and engineering teams prepare structured, reusable context before reviewing a pull request with a human reviewer or an AI coding assistant.

It is not another noisy AI reviewer. Reviewpack is a context layer: it collects pull request metadata, changed files, test signals, documentation signals, dependency signals, risk indicators, and review focus areas into a clear review pack.

## Why Reviewpack?

AI coding tools are powerful, but review quality depends heavily on context.

Direct AI review often starts from raw diffs. That can miss important project-level signals:

- Which files are high risk?
- Were tests updated?
- Were docs updated?
- Did dependencies change?
- Is the pull request too large?
- Does the change affect CI, configuration, or release behavior?
- What should a maintainer focus on first?

Reviewpack prepares that context before review starts.

## Core idea

Direct AI review:

PR diff -> AI -> review comments

Reviewpack workflow:

PR data -> local analysis -> structured context pack -> human reviewer or AI assistant

## Privacy-first by default

Reviewpack runs locally by default.

By default, it does not send code, diffs, branch names, commit messages, environment variables, repository metadata, or terminal information to any external service.

AI features, when added, will be optional and explicit. Users will be able to control what context is sent to an AI provider.

Planned privacy controls include:

- AI disabled by default
- No raw diff upload by default
- No branch name upload by default
- No commit message upload by default
- Optional AI input preview
- Redaction for common secret-like values
- Local-first review pack generation

## What Reviewpack generates

A review pack may include:

- PR summary
- Changed file overview
- Risk checklist
- Test impact
- Documentation impact
- Dependency impact
- CI and configuration impact
- Suggested review focus
- AI-ready review prompt
- Machine-readable JSON output

Example output directory:

.reviewpack/
  pr-summary.md
  risk-checklist.md
  ai-review-prompt.md
  reviewpack.json

## Current status

Reviewpack is in early development.

The first milestone is a local-only CLI that reads fixture data and generates a structured review context pack without network access or AI calls.

## Planned CLI

Initial local fixture mode:

reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

Future GitHub pull request mode:

reviewpack github https://github.com/owner/repo/pull/123 --output .reviewpack

Future local git mode:

reviewpack local --base main --head feature-branch --output .reviewpack

Future optional AI mode:

reviewpack github https://github.com/owner/repo/pull/123 --ai

## Roadmap

### v0.1.0

- Local fixture input
- Deterministic rule-based analysis
- Markdown review pack output
- JSON artifact output
- No network access
- No AI calls
- Basic tests and CI

### v0.2.0

- .reviewpack.yml configuration
- Local git diff mode
- More risk rules
- AI input preview file

### v0.3.0

- GitHub PR URL support
- GitHub token support
- Optional AI provider skeleton
- OpenAI provider support as opt-in

### v0.4.0

- GitHub Action integration
- Optional PR comment mode
- Release note hints
- More maintainer workflow automation

## Non-goals

Reviewpack does not aim to:

- Automatically approve pull requests
- Automatically merge pull requests
- Replace human maintainers
- Spam line-by-line comments
- Upload code by default
- Require AI to be useful

## Design principles

1. Local-first
2. Privacy-first
3. AI-optional
4. Human-readable
5. Machine-readable
6. Maintainer-controlled
7. Tool-agnostic

Reviewpack should work with human reviewers, Codex, Cursor, Cline, OpenCode, Claude Code, GitHub Copilot, and other coding assistants.

## License

MIT
