# Reviewer Checklist

Use this checklist to guide human review.

Reviewpack output is deterministic context, not a replacement for maintainer judgment.

## Correctness

- [ ] Confirm the intended behavior is clear from the PR description and changed files.
- [ ] Review edge cases and failure modes around the changed areas.
- [ ] Check whether the implementation matches the stated PR goal.
- [ ] Review source changes for behavior, compatibility, and maintainability.

## Tests

- [ ] Source files changed but no test files were detected.
- [ ] Ask whether tests should be added or updated before merging.

## Documentation

- [ ] Review documentation changes for accuracy and completeness.
- [ ] Confirm examples, commands, and paths match current behavior.

## Dependencies

- [ ] Review dependency changes for compatibility and security impact.
- [ ] Confirm lock files and package metadata are consistent.

## CI, Configuration, and Infrastructure

- [ ] Review CI workflow changes for required checks and release behavior.

## Release Notes

- [ ] Check `release-note-hints.md` to decide whether this PR should be mentioned in release notes.
- [ ] Confirm whether the change is user-facing, maintainer-facing, or internal only.

## Risk Review

- [ ] High risk signals were detected. Review these before merging.
  - [ ] High-risk area changed

## AI Handoff

- [ ] If using an AI assistant, start with `ai-handoff.md` when file access is available.
- [ ] If uploading one file, use `ai-context.md`.
- [ ] If only copy and paste is available, use `ai-review-prompt.md`.

## Final Maintainer Decision

- [ ] Confirm open questions are resolved.
- [ ] Confirm required checks pass.
- [ ] Confirm the PR is appropriately scoped for merge.
