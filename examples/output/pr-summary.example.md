# PR Review Context Pack

## Pull Request

- Title: Add token refresh support
- Author: alice
- URL: https://github.com/octo-org/example-repo/pull/123

## Description

This pull request updates authentication token refresh behavior and adds dependency changes.

## Change Statistics

- Files changed: 5
- Lines added: 226
- Lines deleted: 59
- Source files: 2
- Test files: 0
- Documentation files: 1
- Dependency files: 1
- CI files: 1
- Config files: 0
- Infrastructure files: 0
- Unknown files: 0

## Changed Files

- src/auth/token.py (source, +120/-32)
- src/auth/session.py (source, +80/-18)
- package.json (dependency, +4/-2)
- .github/workflows/ci.yml (ci, +10/-4)
- README.md (docs, +12/-3)

## Suggested Review Focus

1. Validate behavior changes
   - Source files changed. Review correctness, edge cases, and backward compatibility.
2. Check test coverage
   - Source files changed without test updates. Confirm whether existing tests are sufficient.
3. Review dependency impact
   - Dependency files changed. Check version compatibility, security, and lockfile consistency.
4. Review CI behavior
   - CI configuration changed. Check triggers, permissions, secrets, and required checks.
5. Verify documentation accuracy
   - Documentation changed. Confirm examples and usage notes match the implementation.

## Privacy Notes

- This pack was generated locally from provided input data.
- Network access was not used.
- AI was not used.
- Branch names, commit messages, and terminal environment variables were not collected.
