from __future__ import annotations

from reviewpack.config import ReviewpackConfig
from reviewpack.models import ReviewpackInput, ReviewpackResult
from reviewpack.rules import (
    classify_changed_files,
    compute_change_stats,
    detect_risk_signals,
    suggest_review_focus,
)


def analyze_reviewpack_input(
    reviewpack_input: ReviewpackInput,
    config: ReviewpackConfig | None = None,
) -> ReviewpackResult:
    """Analyze Reviewpack input into a structured Reviewpack result."""

    reviewpack_config = config or ReviewpackConfig()

    changed_files = classify_changed_files(
        reviewpack_input.changed_files,
        reviewpack_config,
    )
    stats = compute_change_stats(changed_files)
    risk_signals = detect_risk_signals(
        changed_files,
        stats,
        reviewpack_config,
    )
    review_focus = suggest_review_focus(changed_files, risk_signals)

    return ReviewpackResult(
        pr=reviewpack_input.pr,
        changed_files=changed_files,
        stats=stats,
        risk_signals=risk_signals,
        review_focus=review_focus,
        metadata={
            "ai_used": False,
            "network_used": False,
        },
    )
