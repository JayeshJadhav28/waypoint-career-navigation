"""Presentation helpers and design-system CSS for Waypoint.

This module contains no AI or career-recommendation logic. It renders the
Waypoint brand, typography, layout primitives and result components used by
``app.py``.
"""

from __future__ import annotations

import base64
import html
from typing import Iterable, Sequence


# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------

BG = "#EDEBE5"
BG_SOFT = "#F7F6F2"
INK = "#20252B"
MUTED = "#64748B"
CORAL = "#DB6B4D"
SAND = "#E9B872"
CARD = "#FFFFFF"
LINE = "#E1DED7"
MUTED_BG = "#F1EFE9"
DARK = "#20252B"


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --wp-bg: #EDEBE5;
    --wp-bg-soft: #F7F6F2;
    --wp-ink: #20252B;
    --wp-muted: #64748B;
    --wp-coral: #DB6B4D;
    --wp-sand: #E9B872;
    --wp-card: #FFFFFF;
    --wp-line: #E1DED7;
    --wp-muted-bg: #F1EFE9;
    --wp-dark: #20252B;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: var(--wp-bg);
    color: var(--wp-ink);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Manrope', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--wp-ink);
    letter-spacing: -0.02em;
}

p, li, label, span, div {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

#MainMenu,
footer,
[data-testid="stAppDeployButton"],
[data-testid="stStatusWidget"] {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    background: transparent;
}

[data-testid="stExpandSidebarButton"] {
    background: var(--wp-card) !important;
    border: 1px solid var(--wp-line) !important;
    border-radius: 9px;
    color: var(--wp-ink) !important;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"], .block-container {
    max-width: 1180px;
    padding: 2.4rem 2.6rem 4rem;
    margin: 0 auto;
}

@media (max-width: 900px) {
    [data-testid="stMainBlockContainer"], .block-container {
        padding: 3.6rem 1.1rem 3rem;
    }
}

/* --------------------------------------------------------------------- */
/* Sidebar                                                                */
/* --------------------------------------------------------------------- */

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background: var(--wp-dark);
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(237, 235, 229, 0.12);
}

[data-testid="stSidebarUserContent"] {
    padding: 1.5rem 1rem 2rem;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li {
    color: #D8D5CC;
}

.wp-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.1rem 0.25rem 1.1rem;
    border-bottom: 1px solid rgba(237, 235, 229, 0.14);
}

.wp-brand-name {
    font-family: 'Manrope', 'Inter', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #F7F6F2;
    line-height: 1.1;
}

.wp-brand-tag {
    font-size: 0.7rem;
    color: #A6ADB8;
    margin-top: 0.2rem;
}

.wp-nav-label {
    font-size: 0.64rem;
    letter-spacing: 0.17em;
    text-transform: uppercase;
    color: #838C99;
    font-weight: 700;
    margin: 1.5rem 0.35rem 0.55rem;
}

.wp-side-rule {
    border-top: 1px solid rgba(237, 235, 229, 0.14);
    margin: 1.4rem 0 1rem;
}

.wp-side-note {
    font-size: 0.7rem;
    line-height: 1.65;
    color: #98A0AC;
    margin: 0.85rem 0.35rem 0;
}

.wp-side-note strong {
    color: #C9C5BC;
    font-weight: 600;
}

.wp-status {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    border: 1px solid rgba(237, 235, 229, 0.16);
    border-radius: 999px;
    padding: 0.34rem 0.7rem;
    font-size: 0.7rem;
    color: #D8D5CC;
    margin: 0.2rem 0.35rem;
}

.wp-status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #E9B872;
    flex-shrink: 0;
}

.wp-status-dot.is-ready {
    background: #9CC5A1;
}

.wp-status-dot.is-missing {
    background: #DB6B4D;
}

[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"],
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
    justify-content: flex-start;
    text-align: left;
    border-radius: 9px;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.5rem 0.75rem;
    min-height: 2.4rem;
    box-shadow: none;
}

[data-testid="stSidebar"] button > div,
[data-testid="stSidebar"] button span {
    justify-content: flex-start;
    width: 100%;
    text-align: left;
}

[data-testid="stSidebar"] button p {
    text-align: left;
    margin: 0;
    font-size: 0.9rem;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"],
[data-testid="stSidebar"] button[kind="secondary"] {
    background: transparent;
    border: 1px solid transparent;
    color: #E6E3DA;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover,
[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(237, 235, 229, 0.07);
    border-color: rgba(237, 235, 229, 0.16);
    color: #FFFFFF;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-primary"],
[data-testid="stSidebar"] button[kind="primary"] {
    background: var(--wp-coral);
    border: 1px solid var(--wp-coral);
    color: #FFFFFF;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-primary"]:hover,
[data-testid="stSidebar"] button[kind="primary"]:hover {
    background: #C85C40;
    border-color: #C85C40;
    color: #FFFFFF;
}

/* --------------------------------------------------------------------- */
/* Buttons and inputs                                                     */
/* --------------------------------------------------------------------- */

[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-secondary"],
.stButton > button,
[data-testid="stFormSubmitButton"] button {
    border-radius: 10px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.92rem;
    padding: 0.58rem 1.05rem;
    transition: background 120ms ease, border-color 120ms ease, transform 120ms ease;
    box-shadow: none;
}

[data-testid="stBaseButton-primary"],
[data-testid="stFormSubmitButton"] button {
    background: var(--wp-coral);
    border: 1px solid var(--wp-coral);
    color: #FFFFFF;
}

[data-testid="stBaseButton-primary"]:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background: #C85C40;
    border-color: #C85C40;
    color: #FFFFFF;
}

[data-testid="stBaseButton-secondary"] {
    background: var(--wp-card);
    border: 1px solid var(--wp-line);
    color: var(--wp-ink);
}

[data-testid="stBaseButton-secondary"]:hover {
    border-color: #C9C4B9;
    background: #FCFBF8;
    color: var(--wp-ink);
}

[data-testid="stForm"] {
    background: var(--wp-card);
    border: 1px solid var(--wp-line);
    border-radius: 16px;
    padding: 1.5rem 1.6rem 1.7rem;
    box-shadow: 0 1px 0 rgba(32, 37, 43, 0.03);
}

[data-testid="stWidgetLabel"] p {
    font-size: 0.86rem;
    font-weight: 600;
    color: var(--wp-ink);
}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: var(--wp-muted);
    font-size: 0.78rem;
}

[data-testid="stTextInputRootElement"],
[data-testid="stTextAreaRootElement"],
[data-testid="stSelectbox"] > div[data-rac],
[data-testid="stMultiSelect"] > div[data-rac] {
    background: #FFFFFF !important;
    border: 1px solid var(--wp-line) !important;
    border-radius: 10px !important;
}

[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stTextAreaRootElement"]:focus-within,
[data-testid="stSelectbox"] > div[data-rac]:focus-within,
[data-testid="stMultiSelect"] > div[data-rac]:focus-within {
    border-color: var(--wp-coral) !important;
    box-shadow: 0 0 0 1px var(--wp-coral) !important;
}

[data-testid="stTextInputRootElement"] input,
[data-testid="stTextAreaRootElement"] textarea,
[data-testid="stSelectbox"] input,
[data-testid="stMultiSelect"] input {
    background: transparent !important;
    color: var(--wp-ink) !important;
}

[data-testid="stSelectbox"] [role="group"],
[data-testid="stMultiSelect"] [role="group"],
[data-testid="stMultiSelectTagsContainer"] {
    background: transparent !important;
    border-color: transparent !important;
    gap: 0.25rem;
}

[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid var(--wp-line);
}

.st-key-hero_actions {
    max-width: 330px;
}

.st-key-hero_actions .stButton > button {
    width: 100%;
    white-space: nowrap;
}

/* --------------------------------------------------------------------- */
/* Typography and page structure                                          */
/* --------------------------------------------------------------------- */

.wp-eyebrow {
    font-size: 0.69rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--wp-coral);
}

.wp-page-head {
    margin: 0.2rem 0 1.7rem;
    max-width: 820px;
}

.wp-page-head h1 {
    font-size: clamp(2rem, 3.4vw, 2.9rem);
    line-height: 1.08;
    font-weight: 800;
    letter-spacing: -0.035em;
    margin: 0.55rem 0 0.7rem;
}

.wp-page-head p {
    color: var(--wp-muted);
    font-size: 1rem;
    line-height: 1.7;
    margin: 0;
    max-width: 72ch;
}

.wp-section-head {
    margin: 2.4rem 0 1rem;
}

.wp-section-head h2 {
    font-size: 1.32rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin: 0;
}

.wp-section-head p {
    color: var(--wp-muted);
    font-size: 0.88rem;
    line-height: 1.6;
    margin: 0.35rem 0 0;
    max-width: 75ch;
}

.wp-section-head.tight {
    margin-top: 1.4rem;
}

/* --------------------------------------------------------------------- */
/* Hero                                                                   */
/* --------------------------------------------------------------------- */

.wp-hero {
    position: relative;
    overflow: hidden;
    background: var(--wp-dark);
    border-radius: 20px;
    padding: 3.1rem 3rem;
    margin-bottom: 1.2rem;
}

.wp-hero::before {
    content: "";
    position: absolute;
    width: 360px;
    height: 360px;
    border: 1px solid rgba(237, 235, 229, 0.13);
    border-radius: 50%;
    right: -90px;
    top: -110px;
}

.wp-hero::after {
    content: "";
    position: absolute;
    width: 520px;
    height: 520px;
    border: 1px solid rgba(237, 235, 229, 0.07);
    border-radius: 50%;
    right: -170px;
    top: -190px;
}

.wp-hero-grid {
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: minmax(0, 1.45fr) minmax(160px, 0.7fr);
    gap: 2rem;
    align-items: center;
}

.wp-hero .wp-eyebrow {
    color: var(--wp-sand);
}

.wp-hero h1 {
    color: #F7F6F2;
    font-size: clamp(2.5rem, 5.2vw, 4.05rem);
    line-height: 1.02;
    letter-spacing: -0.045em;
    font-weight: 800;
    margin: 0.9rem 0 1.1rem;
    max-width: 15ch;
}

.wp-hero p {
    color: #C8C4BB;
    font-size: 1.02rem;
    line-height: 1.75;
    max-width: 54ch;
    margin: 0;
}

.wp-hero-note {
    color: #8E959F !important;
    font-size: 0.76rem !important;
    letter-spacing: 0.02em;
    margin-top: 1.5rem !important;
}

.wp-hero-visual {
    display: flex;
    justify-content: center;
    align-items: center;
}

@media (max-width: 820px) {
    .wp-hero {
        padding: 2.2rem 1.6rem;
    }
    .wp-hero-grid {
        grid-template-columns: 1fr;
    }
    .wp-hero-visual {
        display: none;
    }
}

/* --------------------------------------------------------------------- */
/* Cards, grids, metrics                                                  */
/* --------------------------------------------------------------------- */

.wp-grid {
    display: grid;
    gap: 1rem;
}

.wp-grid-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.wp-grid-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.wp-grid-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }

@media (max-width: 980px) {
    .wp-grid-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .wp-grid-3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 640px) {
    .wp-grid-4, .wp-grid-3, .wp-grid-2 {
        grid-template-columns: 1fr;
    }
}

.wp-card {
    background: var(--wp-card);
    border: 1px solid var(--wp-line);
    border-radius: 14px;
    padding: 1.35rem 1.4rem;
    height: 100%;
    box-shadow: 0 1px 0 rgba(32, 37, 43, 0.03);
    box-sizing: border-box;
}

.wp-card-accent {
    border-top: 3px solid var(--wp-coral);
}

.wp-card-kicker {
    font-size: 0.64rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--wp-muted);
    font-weight: 700;
    margin-bottom: 0.7rem;
}

.wp-card-title {
    font-size: 1.14rem;
    line-height: 1.3;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0 0 0.55rem;
    color: var(--wp-ink);
    overflow-wrap: anywhere;
}

.wp-card-text {
    color: #42505F;
    font-size: 0.9rem;
    line-height: 1.68;
    margin: 0.75rem 0 0;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.wp-card-note {
    color: var(--wp-muted);
    font-size: 0.76rem;
    line-height: 1.5;
    margin: 0.8rem 0 0;
}

.wp-journey .wp-step-num {
    font-family: 'Manrope', sans-serif;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    color: var(--wp-coral);
    display: block;
    margin-bottom: 0.75rem;
}

.wp-metrics {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
    margin: 0.4rem 0 0.4rem;
}

@media (max-width: 820px) {
    .wp-metrics { grid-template-columns: 1fr; }
}

.wp-metric {
    background: var(--wp-card);
    border: 1px solid var(--wp-line);
    border-radius: 14px;
    padding: 1.05rem 1.2rem;
}

.wp-metric-value {
    font-family: 'Manrope', sans-serif;
    font-size: 1.45rem;
    line-height: 1.2;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--wp-ink);
    overflow-wrap: anywhere;
}

.wp-metric-label {
    font-size: 0.65rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--wp-muted);
    font-weight: 700;
    margin-top: 0.45rem;
}

.wp-metric-note {
    font-size: 0.74rem;
    color: var(--wp-muted);
    line-height: 1.5;
    margin-top: 0.25rem;
}

/* --------------------------------------------------------------------- */
/* Scores, chips, details                                                 */
/* --------------------------------------------------------------------- */

.wp-score {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 0.15rem 0 0.5rem;
}

.wp-score-value {
    font-family: 'Manrope', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--wp-coral);
    white-space: nowrap;
    line-height: 1;
}

.wp-score-value span {
    font-size: 0.72rem;
    color: var(--wp-muted);
    font-weight: 600;
    letter-spacing: 0;
}

.wp-score-track {
    flex: 1;
    min-width: 60px;
    height: 7px;
    border-radius: 999px;
    background: var(--wp-muted-bg);
    overflow: hidden;
}

.wp-score-fill {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: var(--wp-coral);
}

.wp-score-label {
    font-size: 0.64rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--wp-muted);
    font-weight: 700;
    margin-top: 0.45rem;
}

.wp-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.35rem 0 0.2rem;
}

.wp-chip {
    display: inline-block;
    padding: 0.4rem 0.72rem;
    border-radius: 999px;
    background: var(--wp-muted-bg);
    border: 1px solid var(--wp-line);
    color: var(--wp-ink);
    font-size: 0.82rem;
    font-weight: 500;
    line-height: 1.35;
}

.wp-chip-coral {
    background: #FBEAE5;
    border-color: #F3CABB;
    color: #8A3B27;
}

.wp-detail-card {
    background: var(--wp-card);
    border: 1px solid var(--wp-line);
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
}

.wp-details {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.1rem 2rem;
}

@media (max-width: 700px) {
    .wp-details { grid-template-columns: 1fr; }
}

.wp-detail-label {
    font-size: 0.64rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--wp-muted);
    font-weight: 700;
}

.wp-detail-value {
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--wp-ink);
    margin-top: 0.25rem;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.wp-detail-empty {
    color: #8A94A3;
    font-style: italic;
}

/* --------------------------------------------------------------------- */
/* Timeline                                                               */
/* --------------------------------------------------------------------- */

.wp-timeline {
    position: relative;
    margin: 0.6rem 0 0;
}

.wp-timeline::before {
    content: "";
    position: absolute;
    left: 21px;
    top: 10px;
    bottom: 16px;
    width: 1px;
    background: var(--wp-line);
}

.wp-tl-item {
    position: relative;
    display: grid;
    grid-template-columns: 44px minmax(0, 1fr);
    gap: 1.05rem;
    padding-bottom: 1.15rem;
}

.wp-tl-marker {
    position: relative;
    z-index: 1;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--wp-card);
    border: 1px solid var(--wp-line);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Manrope', sans-serif;
    font-size: 0.76rem;
    font-weight: 800;
    color: var(--wp-coral);
}

.wp-tl-body {
    background: var(--wp-card);
    border: 1px solid var(--wp-line);
    border-radius: 13px;
    padding: 1rem 1.2rem 1.1rem;
}

.wp-tl-duration {
    font-size: 0.64rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8A6226;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.wp-tl-text {
    color: var(--wp-ink);
    font-size: 0.92rem;
    line-height: 1.6;
    margin: 0;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

@media (max-width: 520px) {
    .wp-tl-item {
        grid-template-columns: 34px minmax(0, 1fr);
        gap: 0.75rem;
    }
    .wp-tl-marker {
        width: 34px;
        height: 34px;
        font-size: 0.66rem;
    }
    .wp-timeline::before { left: 16px; }
}

/* --------------------------------------------------------------------- */
/* Notices, empty states, footer                                          */
/* --------------------------------------------------------------------- */

.wp-notice {
    border: 1px solid var(--wp-line);
    border-radius: 12px;
    padding: 0.95rem 1.1rem;
    font-size: 0.86rem;
    line-height: 1.65;
    margin: 1rem 0;
}

[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) {
    background: #EDF3EA;
    border: 1px solid #D5E2D0;
    color: #33512F;
}

[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) [data-testid="stAlertContainer"] {
    background: transparent;
}

[data-testid="stAlertContentSuccess"] {
    color: #33512F !important;
}

.wp-notice strong {
    font-weight: 700;
}

.wp-notice-sand {
    background: #FBF1DF;
    border-color: #EFDDBB;
    color: #5C4A2C;
}

.wp-notice-coral {
    background: #FBEAE5;
    border-color: #F3CABB;
    color: #733526;
}

.wp-notice-muted {
    background: var(--wp-muted-bg);
    border-color: var(--wp-line);
    color: #4B5563;
}

.wp-disclaimer {
    border-top: 1px solid var(--wp-line);
    margin-top: 2rem;
    padding-top: 1rem;
    color: var(--wp-muted);
    font-size: 0.76rem;
    line-height: 1.65;
}

.wp-disclaimer strong {
    color: #4B5563;
}

.wp-empty {
    background: rgba(255, 255, 255, 0.55);
    border: 1px dashed #CFC9BC;
    border-radius: 16px;
    padding: 2.2rem 1.8rem;
    text-align: center;
    margin: 0.5rem 0 1rem;
}

.wp-empty h3 {
    font-size: 1.15rem;
    margin: 0 0 0.45rem;
}

.wp-empty p {
    color: var(--wp-muted);
    font-size: 0.9rem;
    line-height: 1.6;
    margin: 0 auto;
    max-width: 54ch;
}

.wp-footer {
    margin-top: 3rem;
    padding-top: 1.1rem;
    border-top: 1px solid var(--wp-line);
    display: flex;
    justify-content: space-between;
    gap: 0.9rem;
    flex-wrap: wrap;
    color: #7A8492;
    font-size: 0.74rem;
    line-height: 1.6;
}

.wp-footer strong {
    color: #4B5563;
    font-weight: 600;
}

.wp-list {
    margin: 0.35rem 0 0;
    padding-left: 1.05rem;
    color: #42505F;
    font-size: 0.9rem;
    line-height: 1.8;
}

.wp-list li {
    margin-bottom: 0.2rem;
}

.wp-form-section {
    margin: 1.5rem 0 0.4rem;
    padding-top: 1.35rem;
    border-top: 1px solid var(--wp-line);
}

.wp-form-section.wp-form-first {
    margin-top: 0;
    padding-top: 0;
    border-top: none;
}

.wp-form-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1.03rem;
    font-weight: 700;
    letter-spacing: -0.015em;
    color: var(--wp-ink);
    margin: 0;
}

.wp-form-note {
    color: var(--wp-muted);
    font-size: 0.79rem;
    line-height: 1.55;
    margin: 0.25rem 0 0;
}

@media (max-width: 640px) {
    .wp-page-head h1 { font-size: 1.9rem; }
    .wp-card { padding: 1.15rem 1.1rem; }
    .wp-detail-card { padding: 1.15rem 1.1rem; }
}
"""


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def esc(value: object) -> str:
    """Escape untrusted text for safe insertion into small HTML fragments."""
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def join_values(values: Iterable[str]) -> str:
    return ", ".join(str(value) for value in values if str(value).strip())


def _svg_data_uri(svg: str) -> str:
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f'data:image/svg+xml;base64,{encoded}'


def _mark_svg(light: bool = False) -> str:
    ink = "#F7F6F2" if light else INK
    center = DARK if light else BG_SOFT
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
      <circle cx="32" cy="32" r="24.5" stroke="{ink}" stroke-width="2.5"/>
      <path d="M32 15.5 39.5 32 32 48.5 24.5 32Z" fill="{ink}"/>
      <path d="M32 15.5 39.5 32H24.5Z" fill="{CORAL}"/>
      <circle cx="32" cy="32" r="2.6" fill="{center}"/>
    </svg>
    """


def _hero_svg() -> str:
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" fill="none">
      <circle cx="60" cy="60" r="54" stroke="#F7F6F2" stroke-opacity="0.35" stroke-width="1.5"/>
      <circle cx="60" cy="60" r="42" stroke="#F7F6F2" stroke-opacity="0.14" stroke-width="1"/>
      <path d="M60 20 74 60 60 100 46 60Z" fill="#F7F6F2" fill-opacity="0.9"/>
      <path d="M60 20 74 60H46Z" fill="{CORAL}"/>
      <circle cx="60" cy="60" r="4" fill="{DARK}"/>
      <circle cx="60" cy="60" r="2" fill="#F7F6F2"/>
    </svg>
    """


CSS += f"""
.wp-brand-mark {{
    width: 38px;
    height: 38px;
    display: inline-block;
    flex-shrink: 0;
    background-image: url("{_svg_data_uri(_mark_svg(light=True))}");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}}

.wp-hero-mark {{
    width: 180px;
    height: 180px;
    display: block;
    background-image: url("{_svg_data_uri(_hero_svg())}");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}}
"""


def brand_header() -> str:
    return f"""
    <div class="wp-brand">
      <span class="wp-brand-mark" role="img" aria-label="Waypoint compass mark"></span>
      <div>
        <div class="wp-brand-name">Waypoint</div>
        <div class="wp-brand-tag">Find your next direction.</div>
      </div>
    </div>
    """


def page_header(eyebrow: str, title: str, description: str = "") -> str:
    description_html = f"<p>{esc(description)}</p>" if description else ""
    return f"""
    <div class="wp-page-head">
      <div class="wp-eyebrow">{esc(eyebrow)}</div>
      <h1>{esc(title)}</h1>
      {description_html}
    </div>
    """


def section_header(title: str, note: str = "", tight: bool = False) -> str:
    note_html = f"<p>{esc(note)}</p>" if note else ""
    tight_class = " tight" if tight else ""
    return f"""
    <div class="wp-section-head{tight_class}">
      <h2>{esc(title)}</h2>
      {note_html}
    </div>
    """


def hero() -> str:
    return f"""
    <section class="wp-hero">
      <div class="wp-hero-grid">
        <div>
          <div class="wp-eyebrow">Career navigation</div>
          <h1>Find your next direction.</h1>
          <p>
            Understand your potential, explore career opportunities and discover
            the steps that can move your future forward.
          </p>
          <p class="wp-hero-note">
            An AI-guided career assessment for students and early-career professionals.
          </p>
        </div>
        <div class="wp-hero-visual">
          <span class="wp-hero-mark" role="img" aria-label="Waypoint compass"></span>
        </div>
      </div>
    </section>
    """


def journey_grid(steps: Sequence[dict]) -> str:
    cards = []
    for step in steps:
        cards.append(
            f"""
            <article class="wp-card wp-journey">
              <span class="wp-step-num">{esc(step['number'])}</span>
              <h3 class="wp-card-title">{esc(step['title'])}</h3>
              <p class="wp-card-text">{esc(step['text'])}</p>
            </article>
            """
        )
    return f'<div class="wp-grid wp-grid-4">{"".join(cards)}</div>'


def metric_cards(items: Sequence[dict]) -> str:
    cards = []
    for item in items:
        note = f'<div class="wp-metric-note">{esc(item["note"])}</div>' if item.get("note") else ""
        cards.append(
            f"""
            <div class="wp-metric">
              <div class="wp-metric-value">{esc(item['value'])}</div>
              <div class="wp-metric-label">{esc(item['label'])}</div>
              {note}
            </div>
            """
        )
    return f'<div class="wp-metrics">{"".join(cards)}</div>'


def career_cards(careers: Sequence) -> str:
    if not careers:
        return ""
    scores = [max(0, min(100, int(career.suitability_score))) for career in careers]
    best = max(scores)
    cards = []
    for index, (career, score) in enumerate(zip(careers, scores), start=1):
        is_best = score == best
        kicker = "Strongest match" if is_best else f"Direction {index:02d}"
        accent = " wp-card-accent" if is_best else ""
        cards.append(
            f"""
            <article class="wp-card{accent}">
              <div class="wp-card-kicker">{kicker}</div>
              <h3 class="wp-card-title">{esc(career.career)}</h3>
              <div class="wp-score">
                <div class="wp-score-value">{score}<span>/100</span></div>
                <div class="wp-score-track">
                  <span class="wp-score-fill" style="width:{score}%"></span>
                </div>
              </div>
              <div class="wp-score-label">Indicative suitability</div>
              <p class="wp-card-text">{esc(career.reason)}</p>
            </article>
            """
        )
    return f'<div class="wp-grid wp-grid-3">{"".join(cards)}</div>'


def chips(items: Iterable[str], variant: str = "") -> str:
    class_name = "wp-chip"
    if variant:
        class_name += f" wp-chip-{variant}"
    values = [str(item).strip() for item in items if str(item).strip()]
    if not values:
        return '<p class="wp-card-note">Nothing was returned for this section.</p>'
    return (
        '<div class="wp-chips">'
        + "".join(f'<span class="{class_name}">{esc(value)}</span>' for value in values)
        + "</div>"
    )


def certification_cards(certifications: Sequence[str]) -> str:
    cards = []
    for certification in certifications:
        cards.append(
            f"""
            <article class="wp-card">
              <div class="wp-card-kicker">Certification</div>
              <h3 class="wp-card-title">{esc(certification)}</h3>
              <p class="wp-card-note">
                Confirm the curriculum, cost and current status with the official provider.
              </p>
            </article>
            """
        )
    return f'<div class="wp-grid wp-grid-2">{"".join(cards)}</div>'


def resource_cards(resources: Sequence) -> str:
    cards = []
    for resource in resources:
        cards.append(
            f"""
            <article class="wp-card">
              <div class="wp-card-kicker">{esc(resource.type)}</div>
              <h3 class="wp-card-title">{esc(resource.resource)}</h3>
              <p class="wp-card-note">
                Search for this resource on the provider's official site before enrolling.
              </p>
            </article>
            """
        )
    return f'<div class="wp-grid wp-grid-2">{"".join(cards)}</div>'


def roadmap_timeline(steps: Sequence) -> str:
    items = []
    for index, step in enumerate(steps, start=1):
        items.append(
            f"""
            <div class="wp-tl-item">
              <div class="wp-tl-marker">{index:02d}</div>
              <div class="wp-tl-body">
                <div class="wp-tl-duration">Estimated: {esc(step.time_required)}</div>
                <p class="wp-tl-text">{esc(step.step)}</p>
              </div>
            </div>
            """
        )
    return f'<div class="wp-timeline">{"".join(items)}</div>'


def detail_card(items: Sequence[dict]) -> str:
    blocks = []
    for item in items:
        value = item.get("value")
        if isinstance(value, (list, tuple)):
            value = join_values(value)
        value_text = esc(value) if value else "Not provided"
        value_class = "wp-detail-value" if value else "wp-detail-value wp-detail-empty"
        blocks.append(
            f"""
            <div>
              <div class="wp-detail-label">{esc(item['label'])}</div>
              <div class="{value_class}">{value_text}</div>
            </div>
            """
        )
    return f'<div class="wp-detail-card"><div class="wp-details">{"".join(blocks)}</div></div>'


def notice(message: str, kind: str = "muted") -> str:
    return f'<div class="wp-notice wp-notice-{kind}">{message}</div>'


def disclaimer(text: str) -> str:
    return f'<div class="wp-disclaimer">{text}</div>'


def empty_state(title: str, body: str) -> str:
    return f"""
    <div class="wp-empty">
      <h3>{esc(title)}</h3>
      <p>{esc(body)}</p>
    </div>
    """


def footer() -> str:
    return """
    <div class="wp-footer">
      <div><strong>Waypoint</strong> · Career navigation · Find your next direction.</div>
      <div>AI-generated guidance can be inaccurate. Verify important decisions independently.</div>
    </div>
    """
