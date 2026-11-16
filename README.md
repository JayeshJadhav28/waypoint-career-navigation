# Waypoint – AI Career Navigation

**Find your next direction.**

Waypoint is an AI-powered career navigation platform for students and early-career
professionals. It turns a guided career assessment into structured, readable
guidance: career directions with indicative suitability scores, skills to develop,
certifications and learning resources to investigate, and a staged career roadmap.

Waypoint is built with Python, Streamlit, the Groq API and Pydantic. It keeps the
original career-advisor engine and response model while presenting the results as a
cohesive, responsive product experience.

---

## What Waypoint does

1. **Discover** — you complete a guided assessment covering your education,
   interests, current capabilities and goals.
2. **Explore** — the assessment is converted into a profile description, sent to the
   Groq API and analysed against the existing career-advisor prompt.
3. **Develop** — Waypoint presents the suggested skills, certifications and learning
   resources returned by the model.
4. **Navigate** — the generated roadmap is shown as a numbered timeline with
   estimated durations.

Waypoint is **not** a chatbot, a job board or a validated psychometric test. It does
not store results permanently, does not use accounts and does not claim guaranteed
employment outcomes.

## Who it serves

Students, recent graduates and early-career professionals who want a structured
starting point for career research and planning.

## Features

- Guided, section-based career assessment (personal profile, interests,
  capabilities, goals) with required-field validation.
- AI analysis through the existing Groq integration and the configured
  `openai/gpt-oss-20b` model.
- Pydantic-validated structured responses.
- Career recommendation cards with suitability scores and explanations.
- Skills to develop, alongside the capabilities you reported.
- Certification and learning-resource recommendations.
- Numbered career roadmap with AI-estimated durations.
- Session-based persistence while navigating: results stay available until the
  browser session ends.
- "Start a new assessment" and "Clear session" actions.
- Friendly error handling when the API key is missing or the response is invalid.
- Mock-data mode for interface development and automated testing.
- Rich console CLI (`main.py`) from the original codebase.

## How recommendations are generated

```text
Structured assessment
        │
        ▼
Profile description (plain text)
        │
        ▼
career_advisor.get_career_advice()
        │
        ▼
prompts.py  →  Groq API (openai/gpt-oss-20b)
        │
        ▼
JSON response
        │
        ▼
Pydantic validation (models.CareerAdvice)
        │
        ▼
Waypoint results screens
```

The backend modules (`career_advisor.py`, `prompts.py`, `models.py`,
`mock_data.py`) are unchanged by the interface redesign. `app.py` collects the
structured form input, converts it into the profile text expected by the advisor,
and renders the validated response.

### About the suitability score

Scores are an **indicative AI assessment** of alignment between the submitted
profile and the returned career. They are:

- not an employment probability;
- not a scientifically validated aptitude result;
- dependent on the quality and honesty of the submitted profile.

Users should research roles, talk to people working in the field and verify
requirements independently.

## Skills, certifications and resources

- **Skills to develop** are returned by the AI response and displayed in order. The
  application does not measure proficiency.
- **Reported capabilities** are exactly what the user entered in the assessment;
  Waypoint does not verify or score them.
- **Certifications and resources** are rendered from the AI response. The current
  response schema does not include provider URLs, so Waypoint does not invent links,
  validity periods or endorsements. Always confirm details with the official provider.
- **Roadmap durations** are AI estimates, not commitments.

## Technology stack

| Layer | Technology |
| --- | --- |
| Language | Python 3.13.12 (pinned via `.python-version`) |
| Interface | Streamlit |
| AI provider | Groq API |
| Model | `openai/gpt-oss-20b` |
| Validation | Pydantic |
| Configuration | `python-dotenv`, environment variables, Streamlit secrets |
| CLI | Rich |
| Deployment | Render (Blueprint via `render.yaml`) |

No additional runtime dependencies were introduced by the redesign.

## Project structure

```text
AI-Career-Advisor-main/
├── app.py                  # Waypoint Streamlit application and router
├── ui_theme.py             # Design system, HTML components and CSS
├── career_advisor.py       # Groq client call and response handling
├── prompts.py              # AI prompt definitions
├── models.py               # Pydantic response models
├── mock_data.py            # Sample response for mock mode
├── main.py                 # Rich console CLI version
├── config.py               # Empty placeholder from the original project
├── requirements.txt        # Pinned Python dependencies
├── render.yaml             # Render Blueprint
├── .python-version         # 3.13.12
├── .streamlit/
│   └── config.toml         # Waypoint theme and headless server settings
├── assets/
│   ├── waypoint-logo.svg
│   ├── waypoint-mark.svg
│   ├── favicon.svg
│   └── favicon.png
├── tests/
│   └── test_app.py         # Streamlit AppTest functional tests
└── screenshots/            # Waypoint interface screenshots
```

## Local setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate it

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

Get a key from <https://console.groq.com/keys>. Never commit `.env`; it is already
listed in `.gitignore`.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Open <http://localhost:8501>.

### Optional: mock-data mode

To exercise the full result flow without calling the API:

```powershell
$env:WAYPOINT_USE_MOCK_DATA="true"
python -m streamlit run app.py
```

When mock mode is on, Waypoint displays a "Sample data mode" indicator and returns
the bundled example analysis from `mock_data.py`.

### Optional: console CLI

```bash
python main.py
```

## Running the tests

```bash
pip install pytest
$env:WAYPOINT_USE_MOCK_DATA="true"
python -m pytest tests -q
```

The tests use `streamlit.testing.v1.AppTest`; they do not call the Groq API.

## Deploying to Render

`render.yaml` defines a Render Blueprint with:

- service name `waypoint-career-navigation`
- Python runtime and `pip install -r requirements.txt`
- start command:
  `python -m streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true --browser.gatherUsageStats false`
- health check path `/_stcore/health`
- `GROQ_API_KEY` prompted at deploy time (`sync: false`)
- Free plan initially

### Steps

1. Push this repository to GitHub (after your own review).
2. In the Render dashboard choose **New → Blueprint**.
3. Connect the GitHub repository. Render reads `render.yaml`.
4. When prompted, paste your `GROQ_API_KEY` value.
5. Apply the Blueprint and wait for the first deploy.
6. Open the service URL and confirm the health check and the assessment flow.

### Free-plan considerations

Render's Free instance type provides 0.1 CPU and 512 MB RAM and spins down after
inactivity, so the first request after idling can take tens of seconds. If the app
runs out of memory during real Groq analysis or is too slow to be usable, move to a
paid instance type in the Render dashboard. The application itself does not require
more than the Free plan to start.

No service has been deployed from this workspace; the configuration is ready but the
live deployment still has to be performed.

## Security and privacy

- API keys are read from the environment or Streamlit secrets; none are hard-coded.
- `.env`, `.venv/`, `.streamlit/secrets.toml` and Python caches are git-ignored.
- Assessment results live only in the current Streamlit session; there is no
  database, account or permanent history.
- Profile text is sent to the Groq API to generate the analysis.
- Error messages shown to users are generic; internal exception details are not
  displayed.
- Do not enter passwords, financial details or unnecessary sensitive personal data.

## Current limitations

- No authentication, saved history or cross-device sync.
- No resume upload, job-market data, salary prediction or interview preparation.
- No multi-turn conversation; each analysis is based on one submitted assessment.
- AI output can be inaccurate or outdated, and certification/resource details must be
  verified independently.
- The AI response schema does not include provider URLs or skill proficiency scores,
  so the interface does not display them.

## Attribution

Waypoint began as an existing AI career-advisor codebase and the redesign preserves
its original backend, prompts, models and source attribution. Original project:
AI Career Advisor, created by Muskan, built with Python, Groq, Pydantic and
Streamlit. Waypoint is an independent project and is not affiliated with or endorsed
by any employer, certification provider or educational institution.

## License

MIT License, as with the original project.
