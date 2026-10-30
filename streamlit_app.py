import os
import streamlit as st

from dotenv import load_dotenv

from github_api import (
    GitHubError,
    GitHubAuthenticationError,
    GitHubRateLimitError,
    GitHubUserNotFoundError,
)
from portfolio import analyze_portfolio

from ui.profile import render_profile
from ui.overview import render_repository_overview
from ui.languages import render_languages
from ui.metadata import render_metadata
from ui.activity import render_activity
from ui.repositories import render_repositories
from ui.styles import apply_global_styles
from ui.navigation import render_navigation

st.set_page_config(
    page_title="Developer Portfolio Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_global_styles()

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

st.markdown(
    """
    <div class="app-header">
        <h1>Developer Portfolio Analyzer</h1>
        <p class="app-description">
            Understand what a developer's public GitHub portfolio communicates
            through repositories, languages, activity, and project metadata.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

_, search_column, _ = st.columns([1.5, 5, 1.5])

with search_column:
    input_column, button_column = st.columns([4, 1])

    with input_column:
        username = st.text_input(
            "GitHub username",
            placeholder="Enter a GitHub username",
            label_visibility="collapsed"
        )

    with button_column:
        analyze_button = st.button(
            "Analyze",
            use_container_width=True,
        )

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "repository_page" not in st.session_state:
    st.session_state.repository_page = 1

# Fetch and analyze data only when the Analyze button is clicked
if analyze_button:
    st.session_state.analysis_result = None

    cleaned_username = username.strip()

    if not cleaned_username:
        st.error("Please enter a GitHub username")
    elif not github_token:
        st.error(
            "GitHub token not found. Please configure GITHUB_TOKEN in your .env file."
        )
    else:
        try:
            analysis_result = analyze_portfolio(
                username=cleaned_username,
                github_token=github_token
            )

            st.session_state.analysis_result = analysis_result
            st.session_state.repository_page = 1

        except GitHubUserNotFoundError:
            st.error(f"No GitHub user named '{cleaned_username}' was found.")

        except GitHubAuthenticationError:
            st.error(
                "The app's GitHub token is invalid or expired. "
                "Please check GITHUB_TOKEN in your .env file."
            )

        except GitHubRateLimitError:
            st.error(
                "GitHub's request limit has been reached. "
                "Please wait a while and try again."
            )

        except GitHubError as error:
            st.error(f"GitHub API error: {error}")

# Render the dashboard using the stored analysis
if st.session_state.analysis_result is not None:
    analysis_result = st.session_state.analysis_result

    render_navigation()

    unknown_readmes = analysis_result["readme_analysis"]["unknown_readme"]
    unknown_languages = analysis_result.get("unknown_language_count", 0)
    if unknown_readmes or unknown_languages:
        st.warning(
            "Some checks could not be completed, so these results are partial. "
            f"README status is unknown for {unknown_readmes} "
            f"{'repository' if unknown_readmes == 1 else 'repositories'}, "
            f"and language data is unknown for {unknown_languages}. "
            "Try again later."
        )

    render_profile(
        analysis_result["profile"]
    )

    render_repository_overview(
        analysis_result["repository_summary"]
    )

    render_languages(
        analysis_result["primary_language_percentages"],
        analysis_result["detailed_language_counts"]
    )

    render_metadata(
        analysis_result["metadata_analysis"],
        analysis_result["readme_analysis"],
        analysis_result["repository_summary"]
    )

    render_activity(
        analysis_result["freshness_buckets"],
        analysis_result["sorted_repositories"]
    )

    render_repositories(
        analysis_result["repository_details"]
    )