# Release Checklist

This checklist is for preparing Reviewpack releases.

## Before release

- [ ] Confirm CI is passing on main
- [ ] Run tests locally if possible
- [ ] Review README for accuracy
- [ ] Review docs for outdated commands
- [ ] Review CHANGELOG.md
- [ ] Confirm version number
- [ ] Confirm pyproject.toml project URLs
- [ ] Confirm no secrets or private data are committed
- [ ] Confirm examples use fictional data
- [ ] Confirm generated outputs are not committed accidentally

## Privacy review

Before each release, confirm that new features do not unexpectedly collect or send:

- Source code
- Raw diffs
- Branch names
- Commit messages
- Environment variables
- Git remote URLs
- API tokens
- Repository secrets
- Terminal history

If a feature uses network access, document:

- What endpoint is called
- What data is sent
- Whether tokens are required
- Whether the feature is opt-in
- Whether output can be inspected

## Documentation review

Check these files:

- README.md
- docs/usage.md
- docs/privacy.md
- docs/design.md
- docs/local-git.md
- docs/github.md
- docs/ai-preview.md
- docs/integrations.md
- examples/README.md

## Versioning

During early development, Reviewpack may use 0.x versions.

Recommended early release tags:

- v0.1.0 for local fixture and core context pack generation
- v0.2.0 for local git and AI input preview
- v0.3.0 for GitHub metadata support
- v0.4.0 for GitHub Actions integration

## GitHub release notes template

Title:

    Reviewpack vX.Y.Z

Summary:

    This release adds ...

Highlights:

- 
- 
- 

Privacy notes:

- 
- 
- 

Breaking changes:

- None

Upgrade notes:

- 
