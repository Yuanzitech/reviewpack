# PR Review Context Pack

## Pull Request

- Title: Add token refresh support
- Author: demo-user
- URL: https://github.com/octo-org/example-repo/pull/123
- State: open
- Draft: false
- Base branch: main
- Head branch: feature/token-refresh
- Commits: 3
- Labels: enhancement, auth

## Description

Adds token refresh support and updates related documentation.

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

- src/auth/token.py (modified, source, +120/-20)
- src/auth/refresh.py (added, source, +80/-0)
- README.md (modified, docs, +16/-4)
- package.json (modified, dependency, +4/-2)
- .github/workflows/ci.yml (modified, ci, +6/-33)

## Suggested Review Focus

1. Review behavior changes
   - Source files changed.
2. Check test coverage
   - Source files changed without detected test updates.
3. Check documentation accuracy
   - Documentation files changed.
4. Review dependency impact
   - Dependency files changed.
5. Review CI behavior
   - CI workflow files changed.
6. Review detected risk signals
   - Reviewpack detected deterministic risk signals.

## Privacy Notes

- This pack was generated locally from provided input data.
- AI was not used.
- Raw diffs and full source code were not collected by default.
- Users remain in control of what Reviewpack artifacts are shared with AI tools.
