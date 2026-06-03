# Reviewpack v0.4.0

Reviewpack v0.4.0 adds PyPI publishing workflow preparation, TestPyPI guidance, and release checklist documentation.

This release prepares Reviewpack for safer future package publishing while keeping publishing manual, explicit, and auditable.

## Highlights

### Manual PyPI publishing workflow

Reviewpack now includes a manual publishing workflow:

    .github/workflows/publish.yml

The workflow is triggered manually with:

    workflow_dispatch

It supports:

- Dry-run build and validation
- TestPyPI publishing
- PyPI publishing

The default mode is dry-run.

This means the workflow builds, validates, and uploads distribution artifacts, but does not publish unless maintainers explicitly choose `dry-run: false`.

### TestPyPI and PyPI targets

The publish workflow supports two package repository targets:

- `testpypi`
- `pypi`

This allows maintainers to validate publishing through TestPyPI before publishing to the real PyPI index.

### Trusted publishing preparation

The publish workflow is prepared for OIDC-style trusted publishing with:

    permissions:
      id-token: write

Expected GitHub environments:

- `testpypi`
- `pypi`

This is intended to support safer publishing without long-lived API tokens once the corresponding PyPI or TestPyPI trusted publisher configuration is set up.

### PyPI release checklist

Reviewpack now includes a PyPI release checklist:

    docs/pypi-release-checklist.md

The checklist covers:

- CI verification
- Package workflow verification
- Version consistency
- Changelog and release notes review
- TestPyPI verification
- PyPI publishing safety
- Post-publish verification
- Privacy review

### TestPyPI verification guide

Reviewpack now includes a TestPyPI verification guide:

    docs/testpypi.md

The guide documents:

- Why TestPyPI is useful
- How to install from TestPyPI
- Why `--extra-index-url https://pypi.org/simple/` may be needed
- How to verify the Reviewpack CLI after TestPyPI installation
- Common TestPyPI issues

### Expanded PyPI publishing notes

The existing PyPI publishing documentation has been expanded with:

- Manual publishing workflow details
- Recommended publishing order
- TestPyPI guidance
- Trusted publishing notes
- Version consistency checks
- Token handling guidance
- Privacy notes

## What's changed since v0.3.0

### Added

- Manual PyPI publishing workflow
- PyPI release checklist
- TestPyPI verification guide
- Publish workflow metadata tests

### Changed

- Package version bumped to 0.4.0
- CLI version bumped to 0.4.0
- Expanded PyPI publishing notes with manual workflow and TestPyPI guidance

## Why this release matters

Reviewpack v0.3.0 made the project packaging-ready by adding build checks and installed wheel smoke tests.

Reviewpack v0.4.0 makes the project publishing-ready by adding the workflow and documentation needed for future TestPyPI and PyPI publication.

This release does not publish Reviewpack to PyPI yet.

Instead, it prepares a safer path for package publishing by making the process:

- Manual
- Explicit
- Documented
- Auditable
- Dry-run by default

## Privacy notes

Reviewpack v0.4.0 does not change Reviewpack's runtime privacy behavior.

The new publishing workflow and documentation do not add:

- AI provider calls
- Runtime telemetry
- PR comments
- Source upload behavior
- Raw diff upload behavior
- Token logging

Reviewpack remains:

- Local-first where possible
- AI-optional
- Maintainer-controlled
- Explicit about network access
- Careful with tokens and secrets

## Known limitations

This release does not yet include:

- Actual TestPyPI publication
- Actual PyPI publication
- `pip install reviewpack`
- `pipx install reviewpack`
- Optional PR comments
- AI provider integration
- Local AI provider integration

## Next steps

Planned next steps include:

- Configure TestPyPI trusted publishing
- Run the Publish workflow against TestPyPI
- Verify TestPyPI installation
- Configure PyPI trusted publishing
- Publish Reviewpack to PyPI
- Update installation documentation after PyPI publication
