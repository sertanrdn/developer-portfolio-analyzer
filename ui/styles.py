import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>
        /* Main application */
        .stApp {
            background-color: #0B1120;
            color: #E2E8F0;
        }

        /* Streamlit's native header */
        header[data-testid="stHeader"] {
            background-color: #0B1120;
        }

        /* Main content area */
        .block-container {
            max-width: 1180px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        /* Headings */
        h1, h2, h3 {
            color: #F1F5F9;
            letter-spacing: -0.02em;
        }

        h1 {
            font-weight: 700;
        }

        p {
            color: #94A3B8;
        }

        /* Inputs */
        div[data-baseweb="input"] {
            border-radius: 8px;
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
            margin-top: 1.75rem;
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
            color: #94A3B8;
            font-size: 0.875rem;
            line-height: 1.4;
            text-align: center;
        }

        .profile-metric-value {
            color: #E2E8F0;
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
            color: #94A3B8;
            font-size: 0.875rem;
            line-height: 1.4;
        }

        .overview-metric-value {
            color: #E2E8F0;
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
            border-bottom: 1px solid #263449;
        }

        .language-legend-row:last-child {
            border-bottom: none;
        }

        .language-legend-name {
            color: #CBD5E1;
            font-size: 0.875rem;
        }

        .language-legend-percentage {
            color: #F1F5F9;
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
            color: #94A3B8;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }

        .coverage-value {
            color: #E2E8F0;
            font-size: 1.75rem;
            font-weight: 500;
            line-height: 1.3;
            margin-bottom: 1rem;
        }

        .coverage-track {
            width: 100%;
            height: 8px;
            background-color: #263449;
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 0.75rem;
        }

        .coverage-fill {
            height: 100%;
            background-color: #818CF8;
            border-radius: 999px;
        }

        .coverage-count {
            color: #94A3B8;
            font-size: 0.8rem;
        }

        /* Repository activity */

        .activity-card {
            padding: 0.75rem 0.5rem;
        }

        .activity-card-label {
            color: #94A3B8;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }

        .activity-card-value {
            color: #E2E8F0;
            font-size: 1.75rem;
            font-weight: 500;
            line-height: 1.3;
        }

        .activity-recent-header {
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }

        .activity-recent-header h3 {
            margin: 0;
            font-size: 1.05rem;
            font-weight: 600;
        }

        .activity-repository {
            padding: 0.75rem 0;
        }

        .activity-repository-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .activity-repository-name {
            color: #E2E8F0;
            font-size: 0.875rem;
            font-weight: 500;
        }

        .activity-repository-date {
            color: #94A3B8;
            font-size: 0.8rem;
        }

        .activity-divider {
            height: 1px;
            background-color: #263449;
        }

        /* Repository cards */
        .repo-card-title {
            color: #F1F5F9;
            font-size: 1rem;
            font-weight: 650;
            line-height: 1.4;
            overflow-wrap: anywhere;
            margin-bottom: 0.5rem;
        }

        .repo-card-stats {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            color: #94A3B8;
            font-size: 0.78rem;
            margin-bottom: 0.85rem;
        }

        .repo-card-description {
            color: #CBD5E1;
            font-size: 0.875rem;
            line-height: 1.5;
            min-height: 2.6rem;
            margin-bottom: 0.85rem;
        }

        .repo-card-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            margin-bottom: 0.75rem;
        }

        .repo-badge {
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border: 1px solid #373D70;
            border-radius: 999px;
            background-color: #222747;
            color: #C7D2FE;
            font-size: 0.72rem;
            line-height: 1.4;
            overflow-wrap: anywhere;
        }

        .repo-topic {
            border-color: #334155;
            background-color: #1E293B;
            color: #CBD5E1;
        }

        .repo-card-footer {
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            border-top: 1px solid #263449;
            padding-top: 0.75rem;
            margin-top: 0.25rem;
            margin-bottom: 0.75rem;
            color: #94A3B8;
            font-size: 0.75rem;
        }

        .repo-pagination {
            text-align: center;
            color: #94A3B8;
            font-size: 0.85rem;
            padding-top: 0.65rem;
        }

        /* Section navigation: sticky full-width stripe */
        .stElementContainer:has(.section-nav) {
            position: sticky;
            top: 60px;              /* exactly below Streamlit's 60px header */
            z-index: 999;           /* above page content, below Streamlit's header */
        }

        .section-nav {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.5rem;
            width: 100vw;                   /* full browser width */
            margin-left: calc(50% - 50vw);  /* pull out of the centred 1180px column */
            padding: 0.6rem 1rem;
            background-color: #0B1120;
            border-bottom: 1px solid #334155;
        }

        /* Stop section titles landing under the header + stripe after a click */
        .stMain {
            scroll-padding-top: 100px;
        }

        .section-nav .nav-link {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.4rem 0.85rem;
            border: 1px solid #334155;
            border-radius: 999px;
            background-color: #111C30;
            color: #CBD5E1;
            font-size: 0.85rem;
            font-weight: 500;
            text-decoration: none;
        }

        .section-nav .nav-link:hover {
            border-color: #818CF8;
            background-color: #1E293B;
            color: #C7D2FE;
        }

        /* Input text and labels */
        .stApp label,
        .stApp [data-testid="stWidgetLabel"] p {
            color: #CBD5E1;
        }

        /* Dividers */
        hr {
            border-color: #263449;
        }

        /* Buttons */
        .stButton > button {
            min-height: 40px;
            border: 1px solid #6366F1;
            border-radius: 8px;
            background-color: #6366F1;
            color: #FFFFFF;
            font-weight: 600;
        }

        .stButton > button p {
            color: #FFFFFF;
        }

        .stButton > button:hover {
            border-color: #818CF8;
            background-color: #818CF8;
            color: #0B1120;
        }

        .stButton > button:hover p {
            color: #0B1120;
        }

        /* Disabled buttons */
        .stButton > button:disabled {
            border: 1px solid #334155;
            background-color: #1E293B;
            color: #94A3B8;
            opacity: 1;
            cursor: not-allowed;
        }

        .stButton > button:disabled p {
            color: #94A3B8;
        }

        /* Link buttons */
        .stLinkButton a {
            border: 1px solid #334155;
            border-radius: 8px;
            background-color: #111C30;
            color: #A5B4FC;
            font-weight: 600;
        }

        .stLinkButton a p {
            color: #A5B4FC;
        }

        .stLinkButton a:hover {
            border-color: #818CF8;
            background-color: #1E293B;
            color: #C7D2FE;
        }

        .stLinkButton a:hover p {
            color: #C7D2FE;
        }
        </style>
        """,
        unsafe_allow_html=True
    )