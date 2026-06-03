# Reviewpack v0.3.0

Reviewpack v0.3.0 adds packaging readiness, installation documentation, package build checks, and installed wheel smoke tests.

This release prepares Reviewpack for future PyPI publishing and installable CLI distribution.

## Highlights

### Installation guide

Reviewpack now includes a dedicated installation guide:

    docs/installation.md

The guide documents:

- Source installation
- Editable development installation
- Windows PowerShell setup
- Installing from a built wheel
- Verifying the installed CLI
- Future PyPI and pipx installation plans

### PyPI publishing notes

Reviewpack now includes PyPI publishing notes:

    docs/pypi-publishing.md

This document tracks the planned PyPI publishing process and covers:

- Building distributions
- Running `twine check`
- Inspecting wheel contents
- Version consistency
- Token handling
- Future trusted publishing flow
- Privacy notes for package distribution

### Package build workflow

Reviewpack now includes a package build workflow:

    .github/workflows/package.yml

The workflow verifies that Reviewpack can be packaged successfully.

It runs:

    python -m build
    python -m twine check dist/*

It also checks that the generated wheel contains the `reviewpack` package and does not unexpectedly include repository-only directories such as:

- `tests/`
- `docs/`
- `.github/`

### Installed wheel smoke test

The package workflow now installs the built wheel into a clean virtual environment and verifies that the CLI works after installation.

The smoke test runs:

    reviewpack version

and:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack-smoke

It verifies that expected output files are generated:

    .reviewpack-smoke/pr-summary.md
    .reviewpack-smoke/risk-checklist.md
    .reviewpack-smoke/reviewer-checklist.md
    .reviewpack-smoke/release-note-hints.md
    .reviewpack-smoke/ai-review-prompt.md
    .reviewpack-smoke/reviewpack.json

This gives maintainers more confidence that the built wheel is not only valid, but also usable as an installed CLI.

## What's changed since v0.2.0

### Added

- Installation guide
- PyPI publishing notes
- Package build workflow
- Package metadata tests
- Installed wheel smoke test
- Wheel installation smoke test documentation

### Changed

- Package version bumped to 0.3.0
- CLI version bumped to 0.3.0
- README now links to installation documentation
- Package workflow now verifies that the installed wheel exposes a working `reviewpack` CLI

## Why this release matters

Reviewpack v0.1.0 introduced the first public milestone.

Reviewpack v0.2.0 added maintainer workflow artifacts and GitHub Action integration.

Reviewpack v0.3.0 focuses on packaging readiness.

This release does not publish Reviewpack to PyPI yet, but it prepares the project for future package distribution by verifying that:

- Distribution files can be built
- Package metadata is valid
- The wheel contains expected runtime files
- The installed wheel exposes a working CLI
- The installed CLI can generate Reviewpack outputs

## Privacy notes

Reviewpack v0.3.0 does not change Reviewpack's runtime privacy behavior.

The new packaging and installation checks do not add AI provider calls, runtime telemetry, PR comments, source upload behavior, or raw diff upload behavior.

Reviewpack remains:

- Local-first where possible
- AI-optional
- Maintainer-controlled
- Explicit about network access
- Careful with tokens and secrets

## Known limitations

This release does not yet include:

- PyPI publishing
- `pip install reviewpack`
- `pipx install reviewpack`
- PyPI trusted publishing workflow
- Optional PR comments
- AI provider integration
- Local AI provider integration

## Next steps

Planned next steps include:

- PyPI publishing workflow
- TestPyPI or PyPI setup
- Installation documentation polish after PyPI publication
- Optional PR comment mode
- Stronger configuration support
- Optional AI provider interface
