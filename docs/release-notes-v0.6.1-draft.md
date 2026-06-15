# Reviewpack v0.6.1

Reviewpack v0.6.1 is a small patch release that fixes a user-visible Pydantic warning introduced in v0.6.0.

## Summary

Reviewpack v0.6.0 could print this warning when commands imported `reviewpack.config`:

    UserWarning: Field name "json" in "OutputConfig" shadows an attribute in parent "BaseModel"

This warning appeared because `OutputConfig` used a field named `json`, which conflicts with Pydantic `BaseModel`.

Reviewpack v0.6.1 fixes this by renaming the internal field to:

    json_output

The public configuration key remains:

    outputs:
      json: true

Existing `.reviewpack.yml` files that use `outputs.json` continue to work.

## What's changed

### Fixed

- Fixed Pydantic warning caused by `OutputConfig.json` shadowing `BaseModel.json`

### Changed

- Internal output config field renamed from `json` to `json_output`
- Public `.reviewpack.yml` key `outputs.json` remains supported through a Pydantic alias
- Configuration documentation now clarifies the public `json` output key

### Added

- Test coverage for importing `reviewpack.config` with `UserWarning` treated as errors
- Package smoke test coverage for Reviewpack config import warnings

## Compatibility

This release does not change output file names.

The JSON output file remains:

    reviewpack.json

The public config key remains:

    outputs:
      json: true

Users do not need to change existing `.reviewpack.yml` files.

## Verification

The package workflow now verifies that the installed wheel can import Reviewpack config with user warnings treated as errors:

    python -W error::UserWarning -c "import reviewpack.config"

The release was also intended to preserve normal workflows:

    reviewpack version
    reviewpack demo
    reviewpack guide
    reviewpack handoff

## Privacy notes

This release does not change Reviewpack's privacy model.

Reviewpack still does not:

- call AI providers by default
- collect raw diffs by default
- upload source code by default
- post PR comments by default

## Upgrade

Install or upgrade from PyPI:

    pip install --upgrade reviewpack

Verify:

    reviewpack version
    reviewpack demo
    reviewpack handoff
    reviewpack guide
