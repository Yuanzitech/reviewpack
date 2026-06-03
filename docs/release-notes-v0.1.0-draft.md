# Draft Release Notes: Reviewpack v0.1.0

This is a draft release notes document for the first public milestone of Reviewpack.

## Summary

Reviewpack v0.1.0 introduces a privacy-first foundation for AI-assisted pull request review.

This first milestone focuses on local-first workflows, structured review context generation, and explicit privacy boundaries.

## Highlights

### Structured review context packs

Reviewpack can generate:

- PR summary
- Risk checklist
- AI-ready review prompt
- JSON artifact

### Multiple input modes

Reviewpack currently supports:

- Fixture input
- Local git diff input
- GitHub pull request metadata input

### Privacy-first defaults

Reviewpack is designed to avoid over-collection by default.

Current defaults avoid:

- Raw diff upload
- Full source code upload
- Branch name collection for AI context
- Commit message collection for AI context
- AI provider usage by default

### AI input preview

Reviewpack can generate a local AI input preview so maintainers can inspect context before using any external AI tool.

### Open source project foundations

This milestone also includes:

- Tests
- CI
- Contribution guide
- Security policy
- Issue templates
- Pull request template
- Release checklist
- Documentation set

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
- More maintainer-focused automation
``
