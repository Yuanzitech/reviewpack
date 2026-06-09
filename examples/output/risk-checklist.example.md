# Risk Checklist

## [HIGH] High-risk area changed

### Why this matters

This PR changes paths configured as high risk in Reviewpack configuration.

### What to check

- Confirm the changed behavior is intentional and well-scoped.
- Check edge cases, failure modes, and compatibility impact.
- Confirm test coverage is strong enough for the risk area.

### Affected files

- src/auth/token.py

## [MEDIUM] Dependency files changed

### Why this matters

Dependency changes can affect installation, compatibility, and security.

### What to check

- Confirm the impact is understood and reviewed by the right maintainer.
- Check whether tests, docs, or release notes should be updated.

### Affected files

- package.json

## [MEDIUM] CI workflow changed

### Why this matters

CI changes can affect required checks, automation, or release behavior.

### What to check

- Confirm the impact is understood and reviewed by the right maintainer.
- Check whether tests, docs, or release notes should be updated.

### Affected files

- .github/workflows/ci.yml
