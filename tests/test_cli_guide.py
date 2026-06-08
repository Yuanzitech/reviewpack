from reviewpack.cli import render_guide_text


def test_render_guide_text_contains_common_workflows() -> None:
    text = render_guide_text()

    assert "Reviewpack quick guide" in text
    assert "reviewpack demo" in text
    assert "reviewpack github https://github.com/owner/repo/pull/123" in text
    assert "reviewpack local" in text
    assert "reviewpack from-fixture simple-pr.json" in text
    assert "reviewpack writes files to .reviewpack/ by default".lower() in text.lower()


def test_render_guide_text_mentions_ai_handoff() -> None:
    text = render_guide_text()

    assert ".reviewpack/ai-handoff.md" in text
    assert "Please read .reviewpack/ai-handoff.md and follow it." in text
