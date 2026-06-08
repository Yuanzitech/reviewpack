from reviewpack.ai_handoff import render_ai_handoff, render_handoff_terminal_text, write_ai_handoff
from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.demo import build_demo_reviewpack_input


def make_result():
    return analyze_reviewpack_input(build_demo_reviewpack_input())


def test_render_ai_handoff_contains_expected_sections() -> None:
    result = make_result()
    markdown = render_ai_handoff(result)

    assert "# AI Handoff" in markdown
    assert "Start with" in markdown
    assert "ai-review-prompt.md" in markdown
    assert "If files are not accessible" in markdown
    assert "Privacy notes" in markdown


def test_render_ai_handoff_does_not_claim_ai_was_called() -> None:
    result = make_result()
    markdown = render_ai_handoff(result)

    assert "Reviewpack does not call an AI provider by default." in markdown


def test_write_ai_handoff_creates_file(tmp_path) -> None:
    result = make_result()

    output_path = write_ai_handoff(result, tmp_path)

    assert output_path.exists()
    assert output_path.name == "ai-handoff.md"

    markdown = output_path.read_text(encoding="utf-8")
    assert "# AI Handoff" in markdown


def test_render_handoff_terminal_text_points_to_default_files() -> None:
    text = render_handoff_terminal_text(".reviewpack")

    assert "Reviewpack AI handoff" in text
    assert ".reviewpack/ai-handoff.md" in text
    assert ".reviewpack/ai-review-prompt.md" in text
