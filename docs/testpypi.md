# TestPyPI Verification

TestPyPI is useful for validating package publishing before publishing to PyPI.

Reviewpack is not yet published to TestPyPI or PyPI. This document describes the intended verification flow.

## Why use TestPyPI?

TestPyPI helps maintainers verify:

- Distribution files can be uploaded
- Package metadata renders correctly
- The package can be installed from an index
- The CLI entry point works after index installation

## Important note about dependencies

TestPyPI does not mirror all packages from PyPI.

When installing from TestPyPI, use both TestPyPI and PyPI indexes:

    python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ reviewpack

This allows Reviewpack to come from TestPyPI while dependencies can still be resolved from PyPI.

## Publish to TestPyPI

Reviewpack's future publishing workflow should support TestPyPI through a manual workflow dispatch.

Recommended workflow options:

    repository: testpypi
    dry-run: false

The workflow should build distributions, check metadata, run smoke tests, and then publish to TestPyPI.

## Verify TestPyPI installation

Create a clean virtual environment:

    python -m venv .testpypi
    source .testpypi/bin/activate
    python -m pip install --upgrade pip

Install Reviewpack from TestPyPI:

    python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ reviewpack

Verify the CLI:

    reviewpack version

Run a basic command:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack-testpypi

Expected output files:

    .reviewpack-testpypi/pr-summary.md
    .reviewpack-testpypi/risk-checklist.md
    .reviewpack-testpypi/reviewer-checklist.md
    .reviewpack-testpypi/release-note-hints.md
    .reviewpack-testpypi/ai-review-prompt.md
    .reviewpack-testpypi/reviewpack.json

## Clean up

Deactivate the environment:

    deactivate

Remove local test output if desired:

    rm -rf .testpypi .reviewpack-testpypi

## Common issues

### Package not found

The package may not have been published to TestPyPI yet, or the version may already exist under a different state.

### Dependencies not found

Use `--extra-index-url https://pypi.org/simple/` so dependencies can be resolved from PyPI.

### Version already exists

Package indexes do not allow overwriting an existing version.

Bump the package version before trying again.

## Privacy notes

Installing from TestPyPI should not change Reviewpack runtime privacy behavior.

Reviewpack should remain:

- Local-first where possible
- AI-optional
- Maintainer-controlled
- Explicit about network access
