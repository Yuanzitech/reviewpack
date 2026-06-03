# PyPI Publishing Notes

This document tracks the planned PyPI publishing process for Reviewpack.

Reviewpack is not yet published to PyPI.

The current goal is publishing readiness: make sure the package can be built, inspected, smoke tested, and safely prepared for a future PyPI release.

## Current status

Reviewpack already has:

- `pyproject.toml`
- Hatchling build backend
- Console script entry point
- Project metadata
- GitHub release tags
- CI tests
- Package build workflow
- Installed wheel smoke tests
- Manual publishing workflow

Reviewpack does not yet have:

- PyPI project publication
- PyPI trusted publishing configuration
- `pip install reviewpack` availability
- `pipx install reviewpack` availability

## Build package locally

Install build tooling:

    python -m pip install --upgrade pip
    python -m pip install build twine

Build distributions:

    python -m build

This should create:

    dist/*.tar.gz
    dist/*.whl

## Check package metadata

Run:

    python -m twine check dist/*

The check should pass before uploading to PyPI.

## Inspect wheel contents

A Reviewpack wheel should mainly contain:

    reviewpack/
    reviewpack-*.dist-info/

It should not need to include:

    docs/
    tests/
    .github/
    examples/
    issue templates

Those files are useful in the GitHub repository, but they are not required at runtime for the installed CLI.

## Installed wheel smoke test

Before publishing, install the built wheel in a clean virtual environment:

    python -m venv .smoke
    source .smoke/bin/activate
    python -m pip install --upgrade pip
    python -m pip install dist/*.whl

Verify the CLI:

    reviewpack version
    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack-smoke

Confirm expected output files are generated.

## Manual publishing workflow

Reviewpack includes a manual publishing workflow:

    .github/workflows/publish.yml

The workflow is triggered with:

    workflow_dispatch

It supports:

- dry-run build and validation
- TestPyPI publishing
- PyPI publishing

The default `dry-run` value is true.

This means the workflow builds, validates, and uploads distribution artifacts, but does not publish unless maintainers explicitly choose `dry-run: false`.

## Recommended publishing order

Recommended flow:

1. Prepare release PR
2. Update version numbers
3. Update CHANGELOG
4. Merge after CI and Package workflows pass
5. Create GitHub release tag
6. Run Publish workflow with `dry-run: true`
7. Run Publish workflow for TestPyPI with `dry-run: false`
8. Verify TestPyPI installation
9. Run Publish workflow for PyPI with `dry-run: false`
10. Verify PyPI installation

## TestPyPI

TestPyPI should be used before the first real PyPI publish when possible.

See:

    docs/testpypi.md

## PyPI trusted publishing

Trusted publishing is preferred over long-lived API tokens.

A future PyPI project should be configured to trust the GitHub repository and publishing workflow.

Expected GitHub environments:

- `testpypi`
- `pypi`

The workflow uses OIDC permissions:

    permissions:
      id-token: write

## Version consistency

Before publishing, confirm that these versions match:

- GitHub tag
- `pyproject.toml`
- `reviewpack/__init__.py`
- GitHub release title

Example:

    GitHub tag: v0.3.0
    pyproject.toml: version = "0.3.0"
    reviewpack/__init__.py: __version__ = "0.3.0"

## Token handling

If using a PyPI API token instead of trusted publishing:

- Do not commit it
- Do not print it in logs
- Store it only in GitHub Actions secrets
- Prefer scoped tokens when possible
- Rotate tokens if exposure is suspected

## Non-goals for current publishing readiness

This publishing readiness step does not:

- Publish to PyPI automatically
- Add AI provider integration
- Change Reviewpack runtime behavior
- Change GitHub Action behavior
- Add automatic release publishing on tag push

## Privacy notes

Publishing Reviewpack to PyPI should not change Reviewpack's privacy model.

Reviewpack should continue to be:

- Local-first where possible
- AI-optional
- Maintainer-controlled
- Explicit about network access
- Careful with tokens and secrets
