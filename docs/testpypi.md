# TestPyPI Verification

TestPyPI is useful for validating package publishing before publishing to PyPI.

Reviewpack has been published to TestPyPI for verification.

## Why use TestPyPI?

TestPyPI helps maintainers verify:

- Distribution files can be uploaded
- Package metadata renders correctly
- The package can be installed from an index
- The CLI entry point works after index installation
- Basic Reviewpack commands work after installation

## Important note about dependencies

TestPyPI does not mirror all packages from PyPI.

When installing from TestPyPI, use both TestPyPI and PyPI indexes:

    python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ reviewpack

This allows Reviewpack to come from TestPyPI while dependencies can still be resolved from PyPI.

## TestPyPI project page

Reviewpack TestPyPI project page:

    https://test.pypi.org/project/reviewpack/

## Manual installation verification

Create a clean virtual environment:

    python -m venv .testpypi
    source .testpypi/bin/activate
    python -m pip install --upgrade pip

Install Reviewpack from TestPyPI:

    python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ reviewpack

Verify the CLI:

    reviewpack version

## Verify with a synthetic fixture

Create a file named:

    simple-pr.json

Example content:

    {
      "pr": {
        "title": "Verify Reviewpack from TestPyPI",
        "author": "test-user",
        "url": "https://github.com/Yuanzitech/reviewpack/pull/1",
        "description": "Synthetic fixture for TestPyPI installation verification."
      },
      "changed_files": [
        {
          "path": "reviewpack/cli.py",
          "additions": 10,
          "deletions": 2
        },
        {
          "path": "tests/test_cli.py",
          "additions": 20,
          "deletions": 0
        },
        {
          "path": "README.md",
          "additions": 5,
          "deletions": 1
        }
      ]
    }

Run:

    reviewpack from-fixture simple-pr.json --output .reviewpack-testpypi

Expected output files:

    .reviewpack-testpypi/pr-summary.md
    .reviewpack-testpypi/risk-checklist.md
    .reviewpack-testpypi/reviewer-checklist.md
    .reviewpack-testpypi/release-note-hints.md
    .reviewpack-testpypi/ai-review-prompt.md
    .reviewpack-testpypi/reviewpack.json

Optional AI input preview verification:

    reviewpack from-fixture simple-pr.json --output .reviewpack-testpypi-ai --preview-ai-input

Expected additional output:

    .reviewpack-testpypi-ai/ai-input-preview.md

## GitHub Actions verification workflow

Reviewpack includes a manual workflow for TestPyPI installation verification:

    .github/workflows/testpypi-install.yml

Run it from GitHub:

    Actions -> TestPyPI Install -> Run workflow

Input:

    package-version: 0.4.0

The workflow:

- Installs Reviewpack from TestPyPI
- Uses PyPI as an extra index for dependencies
- Runs `reviewpack version`
- Creates a synthetic fixture
- Runs `reviewpack from-fixture`
- Verifies expected output files
- Runs `--preview-ai-input`
- Uploads generated verification outputs as an artifact

## Clean up local verification

Deactivate the environment:

    deactivate

Remove local test output if desired:

    rm -rf .testpypi .reviewpack-testpypi .reviewpack-testpypi-ai simple-pr.json

## Common issues

### Package not found

The package may not have been published to TestPyPI yet, or the package version may not match.

### Dependencies not found

Use:

    --extra-index-url https://pypi.org/simple/

This allows dependencies to be resolved from PyPI.

### Version already exists

Package indexes do not allow overwriting an existing version.

Bump the package version before trying again.

### CLI command missing

If `reviewpack` is not found after installation, check:

- `pyproject.toml` `[project.scripts]`
- Built wheel contents
- Installed package metadata
- Whether the correct package version was installed

## Privacy notes

Installing from TestPyPI should not change Reviewpack runtime privacy behavior.

Reviewpack should remain:

- Local-first where possible
- AI-optional
- Maintainer-controlled
- Explicit about network access
