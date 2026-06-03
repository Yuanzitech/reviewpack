# PyPI Release Checklist

This checklist is for future Reviewpack PyPI releases.

Reviewpack is not published to PyPI yet. This checklist should be used when preparing the first PyPI release and later package releases.

## Before publishing

- [ ] Confirm CI workflow is passing on main
- [ ] Confirm Package workflow is passing on main
- [ ] Confirm version in `pyproject.toml`
- [ ] Confirm version in `reviewpack/__init__.py`
- [ ] Confirm GitHub release tag matches the package version
- [ ] Confirm CHANGELOG.md is updated
- [ ] Confirm release notes are prepared
- [ ] Confirm README.md is accurate
- [ ] Confirm installation docs are accurate
- [ ] Confirm no secrets or private data are committed
- [ ] Confirm package name availability on PyPI
- [ ] Confirm PyPI trusted publishing is configured, if used
- [ ] Confirm TestPyPI publishing has been tested, if applicable

## Version consistency

Before publishing, confirm these values match:

    GitHub tag: vX.Y.Z
    pyproject.toml: version = "X.Y.Z"
    reviewpack/__init__.py: __version__ = "X.Y.Z"

## Build verification

The package workflow should verify:

- Source distribution can be built
- Wheel distribution can be built
- `twine check` passes
- Wheel contains the `reviewpack` package
- Wheel does not unexpectedly include repository-only directories
- Built wheel can be installed
- Installed CLI can run `reviewpack version`
- Installed CLI can run `reviewpack from-fixture`
- Expected output files are generated

## TestPyPI verification

Before publishing to PyPI, consider publishing to TestPyPI first.

After TestPyPI publishing, verify installation in a clean environment:

    python -m venv .test-install
    source .test-install/bin/activate
    python -m pip install --upgrade pip
    python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ reviewpack
    reviewpack version

Then run:

    reviewpack from-fixture examples/fixtures/simple-pr.json --output .reviewpack-testpypi

Confirm expected output files are generated.

## PyPI publishing

Only publish to PyPI after:

- TestPyPI verification has passed, or maintainers explicitly decide to skip it
- Version numbers are final
- GitHub release notes are ready
- Package workflow is green
- Maintainers are comfortable that the package name and metadata are correct

## Token and publishing safety

Prefer PyPI trusted publishing where possible.

If API tokens are used:

- Do not commit tokens
- Do not print tokens in logs
- Store tokens only in GitHub Actions secrets
- Use scoped tokens when possible
- Rotate tokens if there is any exposure concern

## After publishing

After publishing to PyPI:

- [ ] Verify `pip install reviewpack`
- [ ] Verify `pipx install reviewpack`, if pipx is supported
- [ ] Verify `reviewpack version`
- [ ] Verify a basic `reviewpack from-fixture` run
- [ ] Update installation documentation
- [ ] Update README quick start if needed
- [ ] Announce the release in GitHub Releases

## Privacy review

Publishing to PyPI should not change Reviewpack runtime privacy behavior.

Confirm that package publishing does not introduce:

- Telemetry
- AI provider calls
- Source upload behavior
- Raw diff upload behavior
- Token logging
- Unexpected network access
