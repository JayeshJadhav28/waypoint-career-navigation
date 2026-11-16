"""Waypoint — AI career navigation.

The application keeps the original Groq/Pydantic career-advisor engine and
replaces the former single-screen interface with a guided, session-based
Streamlit experience.
"""

from __future__ import annotations

import os

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from groq import Groq

import ui_theme as ui
from career_advisor import get_career_advice
from mock_data import MOCK_CAREER_ADVICE
from models import CareerAdvice


# ---------------------------------------------------------------------------
# Page configuration and configuration values
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Waypoint — Career Navigation",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="auto",
)

st.html(f"<style>{ui.CSS}</style>")

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

# Kept for UI development and testing. The environment override lets the
# automated smoke tests exercise the full result flow without an API call.
USE_MOCK_DATA = False
if os.getenv("WAYPOINT_USE_MOCK_DATA", "").strip().lower() in {"1", "true", "yes", "on"}:
    USE_MOCK_DATA = True

client = Groq(api_key=api_key) if api_key and not USE_MOCK_DATA else None


# ---------------------------------------------------------------------------
# Assessment vocabulary
# ---------------------------------------------------------------------------

EDUCATION_OPTIONS = [
    "High school",
    "Undergraduate",
    "Postgraduate",
    "Recent graduate",
    "Working professional",
    "Other",
]

STATUS_OPTIONS = [
    "Student",
    "Recent graduate",
    "Working professional",
    "Career switcher",
    "Exploring options",
]

EXPERIENCE_OPTIONS = [
    "No formal experience yet",
    "Internship experience",
    "Less than 1 year",
    "1–3 years",
    "3–5 years",
    "5+ years",
]

INTEREST_OPTIONS = [
    "Technology & software",
    "AI & data",
    "Design & UX",
    "Business & management",
    "Finance & fintech",
    "Healthcare",
    "Education",
    "Marketing & communications",
    "Research",
    "Public sector",
    "Entrepreneurship",
    "Other",
]

INDUSTRY_OPTIONS = [
    "Technology",
    "Finance",
    "Healthcare",
    "Education",
    "E-commerce",
    "Media & entertainment",
    "Manufacturing",
    "Consulting",
    "Public sector",
    "Non-profit",
    "Any industry",
]

PREFERENCE_OPTIONS = [
    "Build products",
    "Analyse data",
    "Work with people",
    "Lead teams",
    "Research & innovate",
    "Create & design",
    "Not sure yet",
]

LEARNING_OPTIONS = [
    "Video courses",
    "Documentation",
    "Hands-on projects",
    "Books & guides",
    "Mentorship",
    "Bootcamps",
    "Not sure yet",
]

TECHNICAL_OPTIONS = [
    "Python",
    "Java",
    "JavaScript",
    "SQL",
    "HTML & CSS",
    "Git",
    "Cloud platforms",
    "Data analysis",
    "Machine learning",
    "UI design tools",
    "Excel / spreadsheets",
    "Other",
]

NON_TECHNICAL_OPTIONS = [
    "Communication",
    "Teamwork",
    "Problem solving",
    "Leadership",
    "Presentation",
    "Writing",
    "Time management",
    "Other",
]

FORM_KEYS = [
    "asm_education",
    "asm_degree",
    "asm_status",
    "asm_experience",
    "asm_areas",
    "asm_industries",
    "asm_preference",
    "asm_learning",
    "asm_tech",
    "asm_tech_other",
    "asm_nontech",
    "asm_projects",
    "asm_experience_notes",
    "asm_aspirations",
    "asm_direction",
    "asm_objectives",
    "asm_context",
]

RESULT_PAGES = {
    "recommendations",
    "skills",
    "certifications",
    "roadmap",
}


class AnalysisNotConfigured(Exception):
    """Raised when a real analysis is requested without an API key."""


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

st.session_state.setdefault("page", "overview")
st.session_state.setdefault("form_draft", {})

if st.session_state.page in RESULT_PAGES and "career_advice" not in st.session_state:
    st.session_state.page = "overview"


def go(page: str) -> None:
    st.session_state.page = page
    st.rerun()


def scroll_to_top() -> None:
    """Reset the page scroll once per page change.

    A tiny zero-height component runs after the new page has rendered and
    resets the main scroll container. It is only emitted when the visible page
    changes, so ordinary widget interactions never jump.
    """
    components.html(
        """
        <script>
          (function () {
            const doc = window.parent.document;
            const main = doc.querySelector('[data-testid="stMain"]');
            if (main) main.scrollTo({ top: 0, left: 0, behavior: 'auto' });
            window.parent.scrollTo({ top: 0, left: 0, behavior: 'auto' });
          })();
        </script>
        """,
        height=0,
    )


def clear_form() -> None:
    for key in list(st.session_state.keys()):
        if key in FORM_KEYS or key == "form_draft":
            del st.session_state[key]
    st.session_state.form_draft = {}


def clear_results() -> None:
    for key in (
        "career_advice",
        "profile_used",
        "pending_profile",
        "analysis_error",
        "analysis_success",
        "last_profile",
        "assessment",
    ):
        st.session_state.pop(key, None)


def start_new_assessment() -> None:
    clear_results()
    clear_form()
    go("assessment")


def reset_session() -> None:
    clear_results()
    clear_form()
    go("overview")


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def nav_button(label: str, page: str) -> None:
    active = st.session_state.page == page
    if st.button(
        label,
        key=f"nav_{page}",
        use_container_width=True,
        type="primary" if active else "secondary",
    ):
        go(page)


def status_chip() -> str:
    if USE_MOCK_DATA:
        return '<div class="wp-status"><span class="wp-status-dot is-ready"></span>Sample data mode</div>'
    if client is not None:
        return '<div class="wp-status"><span class="wp-status-dot is-ready"></span>AI service configured</div>'
    return '<div class="wp-status"><span class="wp-status-dot is-missing"></span>API key required</div>'


def render_sidebar() -> None:
    with st.sidebar:
        st.html(ui.brand_header())

        st.html('<div class="wp-nav-label">Explore</div>')
        nav_button("Overview", "overview")
        nav_button("Career Assessment", "assessment")

        if "career_advice" in st.session_state:
            st.html('<div class="wp-nav-label">Your results</div>')
            nav_button("Career Recommendations", "recommendations")
            nav_button("Skills & Development", "skills")
            nav_button("Certifications & Resources", "certifications")
            nav_button("Career Roadmap", "roadmap")

        st.html('<div class="wp-nav-label">Product</div>')
        nav_button("About Waypoint", "about")

        if "career_advice" in st.session_state:
            if st.button("Start a new assessment", key="side_new", use_container_width=True):
                start_new_assessment()
            if st.button("Clear session", key="side_clear", use_container_width=True):
                reset_session()

        st.html('<div class="wp-side-rule"></div>')
        st.html(status_chip())
        st.html(
            '<p class="wp-side-note">'
            "<strong>Session only.</strong> Results are kept in this browser session and "
            "are not saved to an account or database."
            "</p>",
        )


# ---------------------------------------------------------------------------
# Assessment helpers
# ---------------------------------------------------------------------------

def _draft() -> dict:
    return st.session_state.get("form_draft", {})


def _select_index(options: list[str], key: str):
    value = st.session_state.get(key, _draft().get(key))
    return options.index(value) if value in options else None


def _draft_value(key: str, fallback: str = "") -> str:
    value = st.session_state.get(key, _draft().get(key, fallback))
    return value or ""


def _draft_list(key: str) -> list[str]:
    value = st.session_state.get(key, _draft().get(key, []))
    return list(value) if value else []


def _merge_other(values: list[str], other: str) -> list[str]:
    merged = [value for value in values if value != "Other"]
    other = (other or "").strip()
    if "Other" in values and other:
        merged.append(other)
    return merged


def collect_assessment(
    education,
    degree,
    status,
    experience,
    areas,
    industries,
    preference,
    learning,
    tech,
    tech_other,
    nontech,
    projects,
    experience_notes,
    aspirations,
    direction,
    objectives,
    context,
) -> dict:
    return {
        "education": education,
        "degree": (degree or "").strip(),
        "status": status,
        "experience": experience,
        "areas": list(areas or []),
        "industries": list(industries or []),
        "preference": preference,
        "learning": list(learning or []),
        "technical_skills": _merge_other(list(tech or []), tech_other),
        "non_technical_skills": _merge_other(list(nontech or []), ""),
        "projects": (projects or "").strip(),
        "experience_notes": (experience_notes or "").strip(),
        "aspirations": (aspirations or "").strip(),
        "direction": (direction or "").strip(),
        "objectives": (objectives or "").strip(),
        "context": (context or "").strip(),
    }


def validate_assessment(data: dict) -> list[str]:
    errors = []
    if not data.get("education"):
        errors.append("Select your current education level.")
    if not data.get("status"):
        errors.append("Select your current academic or professional status.")
    if not data.get("areas"):
        errors.append("Choose at least one area of interest.")
    if not data.get("aspirations"):
        errors.append("Describe the career aspiration you want Waypoint to consider.")
    return errors


def build_profile_text(data: dict) -> str:
    lines = [
        f"Education level: {data['education']}",
        f"Current status: {data['status']}",
    ]
    optional = [
        ("Degree or course", data.get("degree")),
        ("Experience level", data.get("experience")),
        ("Areas of interest", ui.join_values(data.get("areas", []))),
        ("Preferred industries", ui.join_values(data.get("industries", []))),
        ("Career preference", data.get("preference")),
        ("Learning preferences", ui.join_values(data.get("learning", []))),
        ("Technical skills", ui.join_values(data.get("technical_skills", []))),
        ("Non-technical skills", ui.join_values(data.get("non_technical_skills", []))),
        ("Projects", data.get("projects")),
        ("Relevant experience", data.get("experience_notes")),
        ("Career aspiration", data.get("aspirations")),
        ("Preferred career direction", data.get("direction")),
        ("Learning objectives", data.get("objectives")),
        ("Additional context", data.get("context")),
    ]
    for label, value in optional:
        if value:
            lines.append(f"{label}: {value}")
    return "\n".join(lines)


def analyze_profile(profile: str) -> CareerAdvice:
    if USE_MOCK_DATA:
        return CareerAdvice.model_validate(MOCK_CAREER_ADVICE)
    if client is None:
        raise AnalysisNotConfigured
    return get_career_advice(client, profile)


def friendly_error(exc: Exception) -> str:
    if isinstance(exc, AnalysisNotConfigured):
        return (
            "AI analysis is not configured yet. Add a valid GROQ_API_KEY to the "
            "environment and restart Waypoint."
        )
    if isinstance(exc, ValueError):
        return (
            "Waypoint received an unexpected response from the AI service. "
            "Please try the analysis again."
        )
    return (
        "Waypoint could not complete the analysis. Please try again in a moment. "
        "If the problem continues, check the service configuration."
    )


def run_pending_analysis() -> None:
    profile = st.session_state.get("pending_profile")
    if profile is None:
        return

    st.session_state.pop("pending_profile", None)
    st.session_state.last_profile = profile

    with st.spinner("Waypoint is reviewing your profile. This usually takes a few seconds."):
        try:
            advice = analyze_profile(profile)
        except Exception as exc:  # noqa: BLE001 - surface a safe, useful message
            print(f"[waypoint] analysis failed: {type(exc).__name__}")
            st.session_state.analysis_error = friendly_error(exc)
            st.session_state.analysis_success = False
        else:
            st.session_state.career_advice = advice
            st.session_state.profile_used = profile
            st.session_state.analysis_error = None
            st.session_state.analysis_success = True
            st.session_state.page = "recommendations"
    st.rerun()


# ---------------------------------------------------------------------------
# Reusable page fragments
# ---------------------------------------------------------------------------

def require_results() -> bool:
    if "career_advice" not in st.session_state:
        st.html(
            ui.empty_state(
                "No analysis in this session yet",
                "Complete the career assessment and Waypoint will build your "
                "recommendations, skills guidance and roadmap.",
            ),
        )
        if st.button("Start the career assessment", type="primary", key="empty_cta"):
            go("assessment")
        st.html(ui.footer())
        return False
    return True


def page_footer() -> None:
    st.html(ui.footer())


def form_section(title: str, note: str, first: bool = False) -> None:
    first_class = " wp-form-first" if first else ""
    st.html(
        f'<div class="wp-form-section{first_class}"><div class="wp-form-title">{ui.esc(title)}</div>'
        f'<div class="wp-form-note">{ui.esc(note)}</div></div>',
    )


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def render_overview() -> None:
    st.html(ui.hero())

    with st.container(key="hero_actions"):
        if st.button("Explore my career path", type="primary", key="hero_cta"):
            go("assessment")

    st.html(
        ui.section_header(
            "A four-stage journey",
            "Waypoint is built around the questions students actually ask: what suits me, "
            "what should I learn and what do I do next?",
        ),
    )
    st.html(
        ui.journey_grid(
            [
                {
                    "number": "01 — Discover",
                    "title": "Understand your starting point",
                    "text": "Share your education, interests, capabilities and goals in a guided assessment.",
                },
                {
                    "number": "02 — Explore",
                    "title": "See possible directions",
                    "text": "Review career directions with indicative suitability scores and a clear explanation.",
                },
                {
                    "number": "03 — Develop",
                    "title": "Build relevant capability",
                    "text": "Identify skills to develop, certifications to investigate and resources to explore.",
                },
                {
                    "number": "04 — Navigate",
                    "title": "Turn direction into steps",
                    "text": "Follow a staged roadmap with estimated time commitments for each milestone.",
                },
            ]
        ),
    )

    st.html(
        ui.section_header("What your analysis includes", "One assessment, presented as a usable plan."),
    )
    st.html(
        ui.detail_card(
            [
                {"label": "Career directions", "value": "Indicative matches with an explanation of fit"},
                {"label": "Skills to develop", "value": "A focused list based on your profile and goals"},
                {"label": "Certifications & resources", "value": "Learning options to investigate further"},
                {"label": "Career roadmap", "value": "Staged milestones with estimated durations"},
            ]
        ),
    )

    if "career_advice" in st.session_state:
        advice = st.session_state.career_advice
        top = max(advice.recommended_careers, key=lambda item: item.suitability_score)
        st.html(
            ui.section_header("Continue where you left off", "Your latest analysis is still available in this session."),
        )
        st.html(
            ui.metric_cards(
                [
                    {
                        "label": "Top direction",
                        "value": top.career,
                        "note": "Based on the profile you submitted",
                    },
                    {
                        "label": "Indicative suitability",
                        "value": f"{top.suitability_score}/100",
                        "note": "Not an employment probability",
                    },
                    {
                        "label": "Estimated transition",
                        "value": advice.estimated_transition_time,
                        "note": "AI-generated estimate",
                    },
                ]
            ),
        )
        c1, c2, c3, _ = st.columns([1.2, 1.05, 1.05, 1.7])
        with c1:
            if st.button("View recommendations", type="primary", key="resume_recs"):
                go("recommendations")
        with c2:
            if st.button("Open roadmap", key="resume_roadmap"):
                go("roadmap")
        with c3:
            if st.button("New assessment", key="resume_new"):
                start_new_assessment()

    st.html(
        ui.notice(
            "<strong>No account needed.</strong> Waypoint keeps your assessment and results "
            "in this browser session only. Nothing is saved permanently.",
            "sand",
        ),
    )
    page_footer()


def render_assessment() -> None:
    st.html(
        ui.page_header(
            "01 — Discover",
            "Career assessment",
            "Give Waypoint enough context to make the analysis useful. Required fields are marked "
            "in the form. The more specific your answers, the more grounded the guidance.",
        ),
    )

    if USE_MOCK_DATA:
        st.html(
            ui.notice(
                "<strong>Sample data mode is on.</strong> Submitting the form returns a bundled "
                "example analysis instead of calling the Groq API.",
                "sand",
            ),
        )
    elif client is None:
        st.html(
            ui.notice(
                "<strong>AI analysis is not configured.</strong> Add a valid <code>GROQ_API_KEY</code> "
                "environment variable to enable real recommendations. You can still review the form "
                "and the rest of the interface.",
                "coral",
            ),
        )

    form_errors = st.session_state.pop("form_errors", None)
    if form_errors:
        st.error("Please complete the following before continuing:\n\n" + "\n".join(f"- {item}" for item in form_errors))

    analysis_error = st.session_state.get("analysis_error")
    if analysis_error:
        st.error(analysis_error)
        can_retry = USE_MOCK_DATA or client is not None
        c1, c2, _ = st.columns([1.15, 1.15, 2])
        with c1:
            if st.button(
                "Try again",
                type="primary",
                key="retry_analysis",
                disabled=not can_retry,
            ):
                st.session_state.pending_profile = st.session_state.get("last_profile")
                st.session_state.pop("analysis_error", None)
                st.rerun()
        with c2:
            if st.button("Edit my profile", key="edit_after_error"):
                st.session_state.pop("analysis_error", None)
                st.rerun()

    if st.session_state.get("pending_profile") is not None:
        run_pending_analysis()

    with st.form("waypoint_assessment", clear_on_submit=False):
        form_section(
            "Personal and academic profile",
            "Your current stage helps Waypoint calibrate the advice.",
            first=True,
        )
        left, right = st.columns(2, gap="large")
        with left:
            education = st.selectbox(
                "Education level *",
                EDUCATION_OPTIONS,
                index=_select_index(EDUCATION_OPTIONS, "asm_education"),
                placeholder="Select education level",
                key="asm_education",
            )
            degree = st.text_input(
                "Degree or course",
                value=_draft_value("asm_degree"),
                placeholder="e.g. BSc Computer Science",
                key="asm_degree",
            )
        with right:
            status = st.selectbox(
                "Current status *",
                STATUS_OPTIONS,
                index=_select_index(STATUS_OPTIONS, "asm_status"),
                placeholder="Select current status",
                key="asm_status",
            )
            experience = st.selectbox(
                "Experience",
                EXPERIENCE_OPTIONS,
                index=_select_index(EXPERIENCE_OPTIONS, "asm_experience"),
                placeholder="Select experience level",
                key="asm_experience",
            )

        form_section(
            "Interests and preferences",
            "Choose what genuinely interests you; these answers shape the career directions.",
        )
        left, right = st.columns(2, gap="large")
        with left:
            areas = st.multiselect(
                "Areas of interest *",
                INTEREST_OPTIONS,
                default=_draft_list("asm_areas"),
                placeholder="Choose one or more areas",
                key="asm_areas",
            )
            industries = st.multiselect(
                "Preferred industries",
                INDUSTRY_OPTIONS,
                default=_draft_list("asm_industries"),
                placeholder="Choose industries you would consider",
                key="asm_industries",
            )
        with right:
            preference = st.selectbox(
                "Career preference",
                PREFERENCE_OPTIONS,
                index=_select_index(PREFERENCE_OPTIONS, "asm_preference"),
                placeholder="How would you like to work?",
                key="asm_preference",
            )
            learning = st.multiselect(
                "Learning preferences",
                LEARNING_OPTIONS,
                default=_draft_list("asm_learning"),
                placeholder="How do you prefer to learn?",
                key="asm_learning",
            )

        form_section(
            "Current capabilities",
            "List what you can already work with. These are reported capabilities, not measured proficiency levels.",
        )
        left, right = st.columns(2, gap="large")
        with left:
            tech = st.multiselect(
                "Technical skills",
                TECHNICAL_OPTIONS,
                default=_draft_list("asm_tech"),
                placeholder="Select technical skills you have used",
                key="asm_tech",
            )
            tech_other = st.text_input(
                "Other technical skills",
                value=_draft_value("asm_tech_other"),
                placeholder="e.g. Kotlin, Figma, Rust",
                key="asm_tech_other",
            )
            nontech = st.multiselect(
                "Non-technical skills",
                NON_TECHNICAL_OPTIONS,
                default=_draft_list("asm_nontech"),
                placeholder="Select strengths you would bring",
                key="asm_nontech",
            )
        with right:
            projects = st.text_area(
                "Projects",
                value=_draft_value("asm_projects"),
                placeholder="Briefly describe one or two projects and what you built or learned.",
                height=105,
                key="asm_projects",
            )
            experience_notes = st.text_area(
                "Relevant experience",
                value=_draft_value("asm_experience_notes"),
                placeholder="Internships, part-time work, volunteering or self-directed work.",
                height=105,
                key="asm_experience_notes",
            )

        form_section(
            "Goals",
            "Describe the direction you want to explore. This is the strongest signal in the assessment.",
        )
        left, right = st.columns(2, gap="large")
        with left:
            aspirations = st.text_area(
                "Career aspiration *",
                value=_draft_value("asm_aspirations"),
                placeholder="e.g. I want to become a backend developer or AI engineer.",
                height=115,
                key="asm_aspirations",
            )
        with right:
            direction = st.text_input(
                "Preferred career direction",
                value=_draft_value("asm_direction"),
                placeholder="e.g. Backend engineering, data analysis, product design",
                key="asm_direction",
            )
            objectives = st.text_area(
                "Learning objectives",
                value=_draft_value("asm_objectives"),
                placeholder="What would you like to be able to do after your next learning phase?",
                height=70,
                key="asm_objectives",
            )
        context = st.text_area(
            "Anything else Waypoint should know",
            value=_draft_value("asm_context"),
            placeholder="Constraints, opportunities, subjects you enjoy, or an existing free-text profile.",
            height=90,
            key="asm_context",
        )

        st.caption(
            "Your answers are used to generate this analysis and are kept in this browser "
            "session. Avoid sharing passwords, financial details or unnecessary sensitive data."
        )

        submitted = st.form_submit_button(
            "Generate my career direction",
            type="primary",
            use_container_width=True,
        )

    data = collect_assessment(
        education,
        degree,
        status,
        experience,
        areas,
        industries,
        preference,
        learning,
        tech,
        tech_other,
        nontech,
        projects,
        experience_notes,
        aspirations,
        direction,
        objectives,
        context,
    )
    st.session_state.form_draft = data

    if submitted:
        errors = validate_assessment(data)
        if errors:
            st.session_state.form_errors = errors
            st.rerun()
        else:
            st.session_state.assessment = data
            st.session_state.pending_profile = build_profile_text(data)
            st.session_state.analysis_error = None
            st.session_state.pop("form_errors", None)
            st.rerun()

    page_footer()


def render_recommendations() -> None:
    if not require_results():
        return

    advice = st.session_state.career_advice
    top = max(advice.recommended_careers, key=lambda item: item.suitability_score)

    st.html(
        ui.page_header(
            "02 — Explore",
            "Career recommendations",
            "These are AI-generated directions based on the profile you submitted. "
            "Treat them as a starting point for research, not a final decision.",
        ),
    )

    if st.session_state.pop("analysis_success", False):
        st.success("Analysis complete. Your recommendations, skills guidance and roadmap are ready.")

    st.html(
        ui.metric_cards(
            [
                {
                    "label": "Directions returned",
                    "value": str(len(advice.recommended_careers)),
                    "note": "AI-ranked career possibilities",
                },
                {
                    "label": "Top suitability",
                    "value": f"{top.suitability_score}/100",
                    "note": "Indicative assessment, not a probability",
                },
                {
                    "label": "Estimated transition",
                    "value": advice.estimated_transition_time,
                    "note": "Estimate for planning, not a promise",
                },
            ]
        ),
    )

    st.html(
        ui.section_header(
            "Recommended directions",
            "Scores reflect how well the AI response aligns with the profile you provided. "
            "The order and scores are not a scientific assessment.",
        ),
    )
    st.html(ui.career_cards(advice.recommended_careers))

    st.html(
        ui.notice(
            "<strong>How to read the scores.</strong> A suitability score is an indicative "
            "AI assessment. It is not a guaranteed employment probability, a validated aptitude "
            "test or a substitute for research, conversations and real-world experience.",
            "sand",
        ),
    )

    if st.session_state.get("profile_used"):
        with st.expander("Review the profile used for this analysis"):
            st.text(st.session_state.profile_used)

    c1, c2, c3, _ = st.columns([1.15, 1.2, 1.1, 1.6])
    with c1:
        if st.button("Skills to develop", type="primary", key="recs_skills"):
            go("skills")
    with c2:
        if st.button("Certifications & resources", key="recs_certs"):
            go("certifications")
    with c3:
        if st.button("Open roadmap", key="recs_roadmap"):
            go("roadmap")

    st.html(
        ui.disclaimer(
            "<strong>Important:</strong> Career decisions are personal. Research roles, "
            "talk to people working in the field and check current requirements before making "
            "a significant decision."
        ),
    )
    page_footer()


def render_skills() -> None:
    if not require_results():
        return

    advice = st.session_state.career_advice
    assessment = st.session_state.get("assessment") or {}

    st.html(
        ui.page_header(
            "03 — Develop",
            "Skills & development",
            "Use this page to translate the recommendations into a focused learning direction. "
            "Waypoint does not measure proficiency; it suggests skills to develop.",
        ),
    )

    st.html(
        ui.section_header(
            "Skills to develop",
            "Suggested by the AI from your profile and goals. The order follows the returned "
            "recommendation list, not a measured priority.",
        ),
    )
    st.html(ui.chips(advice.skills_to_learn, "coral"))

    st.html(
        ui.section_header(
            "Capabilities you reported",
            "These are the skills, projects and experience you entered in the assessment. "
            "They are not verified or scored by Waypoint.",
        ),
    )
    st.html(
        ui.detail_card(
            [
                {"label": "Technical skills", "value": assessment.get("technical_skills")},
                {"label": "Non-technical skills", "value": assessment.get("non_technical_skills")},
                {"label": "Projects", "value": assessment.get("projects")},
                {"label": "Relevant experience", "value": assessment.get("experience_notes")},
            ]
        ),
    )

    if assessment.get("objectives") or assessment.get("context"):
        st.html(
            ui.section_header("Your learning context", "What you said you want from the next phase."),
        )
        st.html(
            ui.detail_card(
                [
                    {"label": "Learning objectives", "value": assessment.get("objectives")},
                    {"label": "Additional context", "value": assessment.get("context")},
                ]
            ),
        )

    st.html(
        ui.notice(
            "Waypoint cannot confirm that you have mastered a skill, and it does not generate "
            "proficiency levels. Use projects, feedback and interviews to validate your progress.",
            "muted",
        ),
    )

    c1, c2, _ = st.columns([1.3, 1.2, 2])
    with c1:
        if st.button("Find certifications & resources", type="primary", key="skills_certs"):
            go("certifications")
    with c2:
        if st.button("Open my roadmap", key="skills_roadmap"):
            go("roadmap")
    page_footer()


def render_certifications() -> None:
    if not require_results():
        return

    advice = st.session_state.career_advice

    st.html(
        ui.page_header(
            "03 — Develop",
            "Certifications & resources",
            "Learning options suggested by the AI. Verify current content, cost, eligibility and "
            "recognition with the official provider before committing time or money.",
        ),
    )

    st.html(
        ui.section_header(
            "Recommended certifications",
            "The current AI response returns certification names only, so Waypoint does not "
            "invent provider links or validity claims.",
        ),
    )
    st.html(
        ui.certification_cards(advice.recommended_certifications),
    )

    st.html(
        ui.section_header(
            "Learning resources",
            "Resource names and types returned by the analysis.",
        ),
    )
    st.html(ui.resource_cards(advice.learning_resources))

    st.html(
        ui.notice(
            "<strong>No provider URLs were returned in this analysis.</strong> Search for each "
            "resource on the provider's official website and confirm that it is current. "
            "A course or certification does not guarantee employment.",
            "sand",
        ),
    )

    c1, c2, _ = st.columns([1.3, 1.25, 2])
    with c1:
        if st.button("Review skills", type="primary", key="certs_skills"):
            go("skills")
    with c2:
        if st.button("Open roadmap", key="certs_roadmap"):
            go("roadmap")
    page_footer()


def render_roadmap() -> None:
    if not require_results():
        return

    advice = st.session_state.career_advice

    st.html(
        ui.page_header(
            "04 — Navigate",
            "Career roadmap",
            "A staged plan generated from your profile. Durations are AI estimates; adjust them "
            "to your available time and commitments.",
        ),
    )

    st.html(
        ui.metric_cards(
            [
                {
                    "label": "Roadmap milestones",
                    "value": str(len(advice.roadmap)),
                    "note": "Steps returned by the analysis",
                },
                {
                    "label": "Estimated transition",
                    "value": advice.estimated_transition_time,
                    "note": "AI estimate, not a guarantee",
                },
                {
                    "label": "Skills to develop",
                    "value": str(len(advice.skills_to_learn)),
                    "note": "Supporting capabilities",
                },
            ]
        ),
    )

    st.html(
        ui.section_header(
            "Your staged plan",
            "Work through the milestones in order, or adapt the sequence to your circumstances.",
        ),
    )
    st.html(ui.roadmap_timeline(advice.roadmap))

    st.html(
        ui.notice(
            "<strong>All timelines are estimates.</strong> Progress depends on your starting point, "
            "available time, learning pace and the opportunities you can access. Reassess the plan "
            "as you learn more.",
            "sand",
        ),
    )

    c1, c2, _ = st.columns([1.3, 1.2, 2])
    with c1:
        if st.button("Supporting skills", type="primary", key="roadmap_skills"):
            go("skills")
    with c2:
        if st.button("New assessment", key="roadmap_new"):
            start_new_assessment()
    page_footer()


def render_about() -> None:
    st.html(
        ui.page_header(
            "About",
            "Waypoint",
            "An AI-powered career navigation platform for students and early-career "
            "professionals. Find your next direction, then turn it into steps.",
        ),
    )

    st.html(
        ui.section_header("How recommendations are generated", "The same Groq-based analysis engine, presented more clearly."),
    )
    st.html(
        ui.journey_grid(
            [
                {
                    "number": "01",
                    "title": "Your profile",
                    "text": "Your structured assessment is converted into a concise profile description.",
                },
                {
                    "number": "02",
                    "title": "AI analysis",
                    "text": "The profile is sent to the Groq API using the configured career-advisor prompt.",
                },
                {
                    "number": "03",
                    "title": "Structured response",
                    "text": "The model returns career matches, skills, certifications, resources and a roadmap as JSON.",
                },
                {
                    "number": "04",
                    "title": "Validation",
                    "text": "Pydantic checks the response against the expected schema before Waypoint displays it.",
                },
            ]
        ),
    )

    st.html(
        ui.section_header("Responsible AI", "Use Waypoint as a structured starting point, not a verdict."),
    )
    st.html(
        """
        <div class="wp-notice wp-notice-sand">
          <ul class="wp-list">
            <li>AI-generated guidance may contain inaccuracies or outdated suggestions.</li>
            <li>Career suitability scores are indicative, not scientifically validated aptitude results.</li>
            <li>Certifications, courses and resources should be verified independently with the provider.</li>
            <li>No recommendation guarantees an interview, job offer or employment outcome.</li>
            <li>Recommendations depend heavily on the quality and honesty of the profile you submit.</li>
          </ul>
        </div>
        """,
    )

    st.html(
        ui.section_header("Privacy and data", "Be deliberate about what you share."),
    )
    st.html(
        """
        <div class="wp-notice wp-notice-muted">
          <ul class="wp-list">
            <li>Waypoint does not require an account and does not provide permanent result storage.</li>
            <li>Your assessment and results are kept in this browser session and disappear when the session ends.</li>
            <li>The profile text is sent to the Groq API so the configured model can generate the analysis.</li>
            <li>Do not enter passwords, financial details, identity documents or unnecessary sensitive personal information.</li>
          </ul>
        </div>
        """,
    )

    st.html(
        ui.section_header("Current limitations", "What Waypoint does not do."),
    )
    st.html(
        """
        <ul class="wp-list">
          <li>No authentication, saved history or cross-device sync.</li>
          <li>No resume upload, live job-market data or salary prediction.</li>
          <li>No conversational multi-turn advisor; each analysis is based on one submitted assessment.</li>
          <li>The AI response does not include provider URLs, so resource links are not fabricated.</li>
        </ul>
        """,
    )

    st.html(
        ui.section_header("Technology", "A small, focused stack."),
    )
    st.html(
        ui.detail_card(
            [
                {"label": "Interface", "value": "Streamlit"},
                {"label": "AI provider", "value": "Groq API, openai/gpt-oss-20b"},
                {"label": "Validation", "value": "Pydantic response models"},
                {"label": "Deployment", "value": "Render Python web service"},
            ]
        ),
    )

    st.html(
        ui.notice(
            "Waypoint is an independent project. It is not affiliated with or endorsed by any "
            "certification provider, employer or educational institution.",
            "muted",
        ),
    )
    page_footer()


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

render_sidebar()

if st.session_state.get("_rendered_page") != st.session_state.page:
    st.session_state["_rendered_page"] = st.session_state.page
    scroll_to_top()

PAGES = {
    "overview": render_overview,
    "assessment": render_assessment,
    "recommendations": render_recommendations,
    "skills": render_skills,
    "certifications": render_certifications,
    "roadmap": render_roadmap,
    "about": render_about,
}

PAGES.get(st.session_state.page, render_overview)()
