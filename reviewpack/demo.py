from __future__ import annotations

from reviewpack.models import ChangedFile, PullRequestInfo, ReviewpackInput


def build_demo_reviewpack_input() -> ReviewpackInput:
    """Build a synthetic Reviewpack input for first-run demos.

    The demo data is fictional. It is designed to show Reviewpack outputs without
    requiring users to create fixture files manually.
    """

    return ReviewpackInput(
        pr=PullRequestInfo(
            title="Add token refresh support",
            author="demo-user",
            url="https://github.com/octo-org/example-repo/pull/123",
            description=(
                "This synthetic demo pull request updates authentication token refresh behavior, "
                "changes dependency metadata, updates CI, and adjusts documentation."
            ),
        ),
        changed_files=[
            ChangedFile(path="src/auth/token.py", additions=120, deletions=32),
            ChangedFile(path="src/auth/session.py", additions=80, deletions=18),
            ChangedFile(path="package.json", additions=4, deletions=2),
            ChangedFile(path=".github/workflows/ci.yml", additions=10, deletions=4),
            ChangedFile(path="README.md", additions=12, deletions=3),
        ],
    )
