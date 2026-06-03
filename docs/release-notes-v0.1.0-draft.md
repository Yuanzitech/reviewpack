# Reviewpack v0.1.0

Reviewpack v0.1.0 is the first public milestone of Reviewpack.

Reviewpack is a privacy-first context generator for AI-assisted pull request review. It helps maintainers prepare structured, reusable review context before involving a human reviewer or an AI coding assistant.

## Highlights

### Privacy-first review context packs

Reviewpack generates structured context packs for pull request review while avoiding over-collection by default.

The current release can generate:

- PR summary
- Risk checklist
- AI-ready review prompt
- AI input preview
- Machine-readable JSON artifact

### Multiple input modes

Reviewpack v0.1.0 supports three input modes:

- Fixture input
- Local git diff input
- GitHub pull request metadata input

Example commands:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack

    reviewpack local --base main --head HEAD --output .reviewpack

    reviewpack github https://github.com/owner/repo/pull/123 --output .reviewpack

### AI-ready, not AI-required

Reviewpack does not require AI to be useful.

It can generate an AI-ready review prompt locally without calling any AI provider.

It can also generate an AI input preview:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack --preview-ai-input

The preview helps maintainers inspect what kind of context may be prepared before any future AI provider integration is used.

### Local-first workflows

Fixture mode and local git diff mode run locally.

They do not require:

- Network access
- GitHub tokens
- AI provider tokens
- External services

### GitHub PR metadata mode

Reviewpack can fetch GitHub pull request metadata and changed file statistics from the GitHub API.

The GitHub mode currently collects:

- Pull request title
- Pull request author
- Pull request description
- Pull request URL
- Changed file paths
- Added line counts
- Deleted line counts

It does not collect raw diffs or full source code by default.

### Privacy and safety foundations

This release includes:

- Privacy model documentation
- Security policy
- Best-effort secret redaction helper
- AI input preview documentation
- Integration principles
- Release checklist with privacy review items

### Open source project foundations

This release includes:

- README
- Simplified Chinese README
- Changelog
- Contributing guide
- Security policy
- Issue templates
- Pull request template
- Documentation set
- Examples
- Tests
- GitHub Actions CI

## What's included

### CLI commands

- `reviewpack from-fixture`
- `reviewpack local`
- `reviewpack github`
- `reviewpack version`

### Generated files

Reviewpack can generate:

    .reviewpack/pr-summary.md
    .reviewpack/risk-checklist.md
    .reviewpack/ai-review-prompt.md
    .reviewpack/ai-input-preview.md
    .reviewpack/reviewpack.json

### Documentation

Key documentation includes:

- `docs/usage.md`
- `docs/privacy.md`
- `docs/design.md`
- `docs/local-git.md`
- `docs/github.md`
- `docs/ai-preview.md`
- `docs/integrations.md`
- `docs/roadmap.md`
- `docs/release-checklist.md`

## Why this release matters

Many AI review workflows jump directly from a raw diff to an AI response.

Reviewpack takes a different approach: it prepares structured, reusable, privacy-aware context first.

That makes it easier for maintainers to:

- Understand what changed
- Identify review risks
- Check whether tests and docs changed
- Reuse context across human and AI review workflows
- Keep control over what is prepared for AI

## Known limitations

This release does not yet include:

- GitHub Actions integration
- PR comment posting
- AI provider integration
- Release note hints
- Linked issue collection
- Raw diff analysis

## Next steps

Planned next steps include:

- Better review artifacts
- Better GitHub workflow support
- Optional AI provider integration
- GitHub Actions integration
- More maintainer-focused automation

## Privacy notes

Reviewpack v0.1.0 is designed with privacy-first defaults.

By default, Reviewpack does not send code, raw diffs, branch names, commit messages, environment variables, repository secrets, or terminal information to AI providers.

GitHub mode uses network access only to fetch explicitly requested pull request metadata and changed file statistics from the GitHub API.

AI provider calls are not included in this release.
