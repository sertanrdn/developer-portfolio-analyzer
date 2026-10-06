import os
import streamlit as st

from dotenv import load_dotenv

from github_api import (
    fetch_user_profile,
    fetch_repositories,
    fetch_language_data,
    fetch_readme_data
)
from analysis import (
    process_user_profile,
    process_repositories,
    get_repository_summary,
    analyze_languages,
    analyze_detailed_languages,
    analyze_metadata_coverage,
    analyze_readme_coverage,
    analyze_recent_activity,
    build_repository_details
)

from ui.profile import render_profile
from ui.overview import render_repository_overview
from ui.languages import render_languages
from ui.metadata import render_metadata
from ui.activity import render_activity
from ui.repositories import render_repositories
from ui.styles import apply_global_styles

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
    cleaned_username = username.strip()

    if not cleaned_username:
        st.error("Error: You need to enter a username")
    else:
        user_profile = fetch_user_profile(
            username=cleaned_username,
            github_token=github_token
        )

        if user_profile is not None:
            processed_user_profile = process_user_profile(
                user_profile=user_profile
            )

            repositories = fetch_repositories(
                username=cleaned_username,
                github_token=github_token
            )

            if repositories is not None:
                processed_repos = process_repositories(
                    repositories=repositories
                )

                repository_summary = get_repository_summary(
                    processed_repositories=processed_repos
                )

                (
                    language_counts,
                    no_language_count,
                    primary_language_percentages
                ) = analyze_languages(
                    processed_repositories=processed_repos
                )

                language_results = fetch_language_data(
                    username=cleaned_username,
                    repositories=processed_repos,
                    github_token=github_token
                )

                (
                    language_repo_counts,
                    no_language_data_count,
                    unknown_language_count
                ) = analyze_detailed_languages(language_results)

                metadata_analysis = analyze_metadata_coverage(
                    processed_repositories=processed_repos,
                    original_repositories=repository_summary["original"]
                )

                readme_results = fetch_readme_data(
                    username=cleaned_username,
                    repositories=processed_repos,
                    github_token=github_token
                )

                readme_analysis = analyze_readme_coverage(
                    readme_results=readme_results
                )

                (
                    sorted_repositories,
                    recently_active_count,
                    freshness_buckets
                ) = analyze_recent_activity(
                    processed_repositories=processed_repos
                )

                repository_details = build_repository_details(
                    processed_repositories=processed_repos,
                    readme_results=readme_results,
                    language_results=language_results
                )

                analysis_result = {
                    "profile": processed_user_profile,
                    "repository_summary": repository_summary,
                    "primary_language_percentages": primary_language_percentages,
                    "detailed_language_counts": language_repo_counts,
                    "metadata_analysis": metadata_analysis,
                    "readme_analysis": readme_analysis,
                    "freshness_buckets": freshness_buckets,
                    "sorted_repositories": sorted_repositories,
                    "repository_details": repository_details,
                }

                st.session_state.analysis_result = analysis_result
                st.session_state.repository_page = 1

        else:
            st.error("Could not load this GitHub profile.")


# Render the dashboard using the stored analysis
if st.session_state.analysis_result is not None:
    analysis_result = st.session_state.analysis_result

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