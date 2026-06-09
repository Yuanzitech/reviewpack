# Release Note Hints

These hints help maintainers decide whether a PR should be mentioned in release notes.

Reviewpack does not generate final release notes automatically.

## Summary

Review the categories below and decide whether the PR needs a release note entry.

## Changed: Source behavior may have changed

Why this might matter: Source files were changed.

Suggested maintainer action: Decide whether this change affects users, maintainers, APIs, CLI behavior, or runtime behavior.

## Dependencies: Dependency metadata changed

Why this might matter: Dependency files were changed.

Suggested maintainer action: Review whether dependency changes should be mentioned in release notes, migration notes, or compatibility notes.

## CI: CI workflow changed

Why this might matter: CI workflow files were changed.

Suggested maintainer action: Mention this only if it affects contributors, maintainers, release behavior, or required checks.

## Documentation: Documentation changed

Why this might matter: Documentation files were changed.

Suggested maintainer action: Mention this if the documentation update is user-facing or release-relevant.

## Risk: High-risk changes detected

Why this might matter: Reviewpack detected one or more high-risk signals.

Suggested maintainer action: Confirm whether release notes, upgrade notes, or maintainer notes should call out the risk area.

## Suggested Decision Questions

- Is this change visible to users?
- Does this change affect installation, configuration, CI, or release behavior?
- Does this change affect APIs, CLI commands, output files, or compatibility?
- Should this be documented as Added, Changed, Fixed, Deprecated, or Removed?
