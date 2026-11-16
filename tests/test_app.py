"""Functional tests for the Waypoint Streamlit application.

These tests run the real ``app.py`` through ``streamlit.testing.v1.AppTest``.
They never call the Groq API: the analysis flow uses the bundled mock response.
"""

from __future__ import annotations

import os
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_FILE = str(Path(__file__).resolve().parents[1] / "app.py")


def _run(**env: str) -> AppTest:
    """Create an AppTest instance with explicit environment overrides."""
    os.environ["WAYPOINT_USE_MOCK_DATA"] = env.get("mock", "true")
    os.environ["GROQ_API_KEY"] = env.get("groq_key", "test-key-not-used")

    app = AppTest.from_file(APP_FILE, default_timeout=60)
    app.run()
    return app


def _button_labels(app: AppTest) -> list[str]:
    return [button.label for button in app.button]


def _html_content(app: AppTest) -> str:
    """Join the raw HTML rendered through ``st.html`` (reported as UnknownElement)."""
    return "\n".join(str(element.proto.body) for element in app.get("html"))


def _go_to_assessment(app: AppTest) -> AppTest:
    app.button(key="nav_assessment").click().run()
    return app


def _fill_required_fields(app: AppTest) -> AppTest:
    app.selectbox(key="asm_education").set_value("Undergraduate")
    app.selectbox(key="asm_status").set_value("Student")
    app.multiselect(key="asm_areas").set_value(["Technology & software", "AI & data"])
    app.text_area(key="asm_aspirations").set_value(
        "I am a computer science student who wants to become a backend developer."
    )
    return app


def test_landing_page_renders() -> None:
    app = _run()
    assert not app.exception
    labels = _button_labels(app)
    assert "Explore my career path" in labels
    assert "Career Assessment" in labels
    assert "About Waypoint" in labels
    assert app.session_state["page"] == "overview"

    content = _html_content(app)
    assert "Find your next direction." in content
    assert "Career navigation" in content
    assert "A four-stage journey" in content
    assert "Muskan" not in content


def test_results_navigation_hidden_before_analysis() -> None:
    app = _run()
    labels = _button_labels(app)
    assert "Career Recommendations" not in labels
    assert "Skills & Development" not in labels
    assert "Career Roadmap" not in labels


def test_assessment_form_renders_all_sections() -> None:
    app = _go_to_assessment(_run())
    assert not app.exception
    assert app.selectbox(key="asm_education") is not None
    assert app.selectbox(key="asm_status") is not None
    assert app.multiselect(key="asm_areas") is not None
    assert app.text_area(key="asm_aspirations") is not None
    assert app.button(key="FormSubmitter:waypoint_assessment-Generate my career direction")


def test_required_field_validation_blocks_submission() -> None:
    app = _go_to_assessment(_run())
    app.button(key="FormSubmitter:waypoint_assessment-Generate my career direction").click().run()

    assert not app.exception
    assert app.session_state["page"] == "assessment"
    errors = [error.value for error in app.error]
    assert any("Select your current education level" in error for error in errors)
    assert any("Choose at least one area of interest" in error for error in errors)
    assert "pending_profile" not in app.session_state


def test_mock_analysis_generates_results() -> None:
    app = _go_to_assessment(_run())
    _fill_required_fields(app)
    app.button(key="FormSubmitter:waypoint_assessment-Generate my career direction").click().run()

    assert not app.exception
    assert app.session_state["page"] == "recommendations"
    advice = app.session_state["career_advice"]
    assert len(advice.recommended_careers) >= 1
    assert any("Backend Developer" == career.career for career in advice.recommended_careers)

    heading_text = _html_content(app)
    assert "Backend Developer" in heading_text
    assert "Indicative suitability" in heading_text

    labels = _button_labels(app)
    assert "Career Recommendations" in labels
    assert "Career Roadmap" in labels


def test_result_pages_render_from_session_state() -> None:
    app = _go_to_assessment(_run())
    _fill_required_fields(app)
    app.button(key="FormSubmitter:waypoint_assessment-Generate my career direction").click().run()

    expected = {
        "nav_skills": ("skills", ["Skills to develop", "Spring Boot", "REST APIs"]),
        "nav_certifications": (
            "certifications",
            ["AWS Certified Developer", "Spring Boot Documentation", "DeepLearning.AI"],
        ),
        "nav_roadmap": (
            "roadmap",
            ["Your staged plan", "Strengthen Java and backend fundamentals", "1-2 months"],
        ),
        "nav_about": ("about", ["Responsible AI", "Current limitations", "openai/gpt-oss-20b"]),
    }

    for key, (page, snippets) in expected.items():
        app.button(key=key).click().run()
        assert not app.exception
        assert app.session_state["page"] == page
        content = _html_content(app)
        for snippet in snippets:
            assert snippet in content, f"{snippet!r} missing on {page}"


def test_start_new_assessment_clears_results() -> None:
    app = _go_to_assessment(_run())
    _fill_required_fields(app)
    app.button(key="FormSubmitter:waypoint_assessment-Generate my career direction").click().run()
    assert "career_advice" in app.session_state

    app.button(key="side_new").click().run()

    assert not app.exception
    assert app.session_state["page"] == "assessment"
    assert "career_advice" not in app.session_state
    assert "assessment" not in app.session_state


def test_clear_session_returns_to_overview() -> None:
    app = _go_to_assessment(_run())
    _fill_required_fields(app)
    app.button(key="FormSubmitter:waypoint_assessment-Generate my career direction").click().run()

    app.button(key="side_clear").click().run()

    assert not app.exception
    assert app.session_state["page"] == "overview"
    assert "career_advice" not in app.session_state


def test_missing_api_key_produces_friendly_error() -> None:
    app = _go_to_assessment(_run(mock="", groq_key=""))
    _fill_required_fields(app)
    app.button(key="FormSubmitter:waypoint_assessment-Generate my career direction").click().run()

    assert not app.exception
    assert app.session_state["page"] == "assessment"
    errors = [error.value for error in app.error]
    assert any("AI analysis is not configured" in error for error in errors)
    # No stack trace or secret material is exposed to the user.
    assert all("Traceback" not in error for error in errors)
    assert all("gsk_" not in error for error in errors)
