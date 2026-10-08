import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>
        /* Main application */
        .stApp {
            background-color: #f6f7fb;
            color: #111827;
        }

        /* Main content area */
        .block-container {
            max-width: 1180px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        /* Headings */
        h1, h2, h3 {
            color: #111827;
            letter-spacing: -0.02em;
        }

        h1{
            font-weight: 700;
        }

        p {
            color: #64748b;
        }

        /* Inputs */
        div[data-baseweb="input"] {
            border-radius: 8px;
        }

        /* Buttons */
        .stButton > button {
            min-height: 40px;
            border: 1px solid #4f46e5;
            border-radius: 8px;
            background-color: #4f46e5;
            color: #ffffff;
            font-weight: 600;
        }

        .stButton > button p {
            color: #ffffff;
        }

        .stButton > button:hover {
            border-color: #4338ca;
            background-color: #4338ca;
            color: #ffffff;
        }

        .stButton > button:hover p {
            color: #ffffff;
        }

        /* Application header */
        .app-header {
            max-width: 720px;
            margin: 0 auto 2.5rem auto;
            text-align: center;
        }

        .app-header h1 {
            margin: 0;
            font-size: 2.35rem;
            line-height: 1.15;
        }

        .app-description {
            margin: 0.75rem auto 0 auto;
            max-width: 650px;
            font-size: 1rem;
            line-height: 1.6;
        }

        /* Dashboard sections */
        .section-header {
            margin-top: 3.5rem;
            margin-bottom: 1.25rem;
        }

        .section-header h2 {
            margin: 0;
            font-size: 1.5rem;
            line-height: 1.3;
        }

        .section-header p {
            margin: 0.35rem 0 0 0;
            font-size: 0.95rem;
        }

        /* Profile metrics */
        .profile-metric {
            width: 100%;
            padding: 0.25rem 0 1rem 0;
            text-align: center;
        }

        .profile-metric-label {
            margin-bottom: 0.25rem;
            color: #64748b;
            font-size: 0.875rem;
            line-height: 1.4;
            text-align: center;
        }

        .profile-metric-value {
            color: #111827;
            font-size: 1.75rem;
            font-weight: 400;
            line-height: 1.2;
            text-align: center;
        }

        /* Repository overview cards */
        .overview-metric {
            padding: 1rem;
            text-align: center;
        }

        .overview-metric-label {
            margin-bottom: 0.35rem;
            color: #64748b;
            font-size: 0.875rem;
            line-height: 1.4;
        }

        .overview-metric-value {
            color: #111827;
            font-size: 1.75rem;
            font-weight: 400;
            line-height: 1.2;
        }

        /* Chart cards */
        .chart-header {
            margin-bottom: 0.75rem;
        }

        .chart-header h3 {
            margin: 0;
            font-size: 1.05rem;
            font-weight: 600;
        }

        .chart-header p {
            margin: 0.3rem 0 0 0;
            color: #64748b;
            font-size: 0.875rem;
            line-height: 1.5;
        }

        /* Language legend */
        .language-legend-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.4rem 0;
            border-bottom: 1px solid #e2e8f0;
        }

        .language-legend-row:last-child {
            border-bottom: none;
        }

        .language-legend-name {
            color: #475569;
            font-size: 0.875rem;
        }

        .language-legend-percentage {
            color: #111827;
            font-size: 0.875rem;
            font-weight: 600;
        }

        .language-legend-language {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .language-color-dot {
            width: 0.65rem;
            height: 0.65rem;
            border-radius: 50%;
            flex-shrink: 0;
        }

        /* Metadata coverage cards */
        .coverage-card {
            padding: 0.75rem 0.5rem;
        }

        .coverage-label {
            color: #64748b;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }

        .coverage-value {
            color: #111827;
            font-size: 1.75rem;
            font-weight: 500;
            line-height: 1.3;
            margin-bottom: 1rem;
        }

        .coverage-track {
            width: 100%;
            height: 8px;
            background-color: #e2e8f0;
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 0.75rem;
        }

        .coverage-fill {
            height: 100%;
            background-color: #4f46e5;
            border-radius: 999px;
        }

        .coverage-count {
            color: #64748b;
            font-size: 0.8rem;
        }

        /* Link buttons */
        .stLinkButton a {
            border: 1px solid #c7d2fe;
            border-radius: 8px;
            background-color: #ffffff;
            color: #4f46e5;
            font-weight: 600;
        }

        .stLinkButton a p {
            color: #4f46e5;
        }

        .stLinkButton a:hover {
            border-color: #4f46e5;
            background-color: #eef2ff;
            color: #4338ca;
        }

        .stLinkButton a:hover p {
            color: #4338ca;
        }
        </style>
        """,
        unsafe_allow_html=True
    )