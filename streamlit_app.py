import os
import math
import streamlit as st
import altair as alt

from dotenv import load_dotenv
from datetime import datetime

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


load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

st.title("Developer Portfolio Analyzer")
st.write("Analyze a developer's public GitHub portfolio.")

username = st.text_input("GitHub username")

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "repository_page" not in st.session_state:
    st.session_state.repository_page = 1

analyze_button = st.button("Analyze")


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

    processed_user_profile = analysis_result["profile"]
    repository_summary = analysis_result["repository_summary"]
    primary_language_percentages = (
        analysis_result["primary_language_percentages"]
    )
    language_repo_counts = analysis_result["detailed_language_counts"]
    metadata_analysis = analysis_result["metadata_analysis"]
    readme_analysis = analysis_result["readme_analysis"]
    freshness_buckets = analysis_result["freshness_buckets"]
    sorted_repositories = analysis_result["sorted_repositories"]
    repository_details = analysis_result["repository_details"]

    # Profile
    display_name = (
        processed_user_profile.get("name")
        or processed_user_profile.get("login")
    )
    bio = processed_user_profile.get("bio") or "No bio provided."

    created_at = processed_user_profile.get("created_at")
    member_since = datetime.fromisoformat(created_at)

    avatar_column, profile_column = st.columns([1, 3])

    with avatar_column:
        st.image(processed_user_profile["avatar_url"])

    with profile_column:
        st.subheader(display_name)
        st.subheader(f"@{processed_user_profile['login']}")
        st.write(bio)

        if processed_user_profile.get("location"):
            st.write("📍", processed_user_profile["location"])

        if processed_user_profile.get("company"):
            st.write("🏢", processed_user_profile["company"])

        st.link_button(
            "View GitHub profile",
            processed_user_profile["html_url"]
        )

    repos_column, followers_column, following_column, member_column = (
        st.columns(4)
    )

    with repos_column:
        st.metric(
            "Public repositories",
            processed_user_profile["public_repos"]
        )

    with followers_column:
        st.metric("Followers", processed_user_profile["followers"])

    with following_column:
        st.metric("Following", processed_user_profile["following"])

    with member_column:
        st.metric("Member Since", member_since.year)

    # Repository overview
    st.subheader("Repository Overview")

    original_repos, forked_repos, archived_repos = st.columns(3)

    with original_repos:
        st.metric(
            "Original repositories",
            repository_summary["original"]
        )

    with forked_repos:
        st.metric(
            "Forked repositories",
            repository_summary["forked"]
        )

    with archived_repos:
        st.metric(
            "Archived repositories",
            repository_summary["archived"]
        )

    # Languages
    st.subheader("Languages")

    language_chart_data = []

    for language, percentage in primary_language_percentages.items():
        language_chart_data.append(
            {
                "language": language,
                "percentage": percentage
            }
        )

    language_chart = (
        alt.Chart(alt.Data(values=language_chart_data))
        .mark_arc(innerRadius=70)
        .encode(
            theta=alt.Theta("percentage:Q"),
            color=alt.Color("language:N"),
            tooltip=[
                alt.Tooltip("language:N", title="Language"),
                alt.Tooltip(
                    "percentage:Q",
                    title="Share",
                    format=".2f"
                )
            ]
        )
    )

    language_bar_data = []

    for language, repo_count in language_repo_counts.items():
        language_bar_data.append(
            {
                "language": language,
                "repositories": repo_count
            }
        )

    language_bar_chart = (
        alt.Chart(alt.Data(values=language_bar_data))
        .mark_bar()
        .encode(
            x=alt.X(
                "repositories:Q",
                axis=alt.Axis(tickMinStep=1)
            ),
            y=alt.Y("language:N", sort="-x"),
            tooltip=[
                alt.Tooltip("language:N", title="Language"),
                alt.Tooltip(
                    "repositories:Q",
                    title="Repositories"
                )
            ]
        )
    )

    primary_language_column, detailed_language_column = st.columns(2)

    with primary_language_column:
        st.write("Primary language distribution")
        st.altair_chart(language_chart)

    with detailed_language_column:
        st.write("Languages across projects")
        st.altair_chart(language_bar_chart)

    # Portfolio metadata
    st.subheader("Portfolio Metadata")

    readme_coverage, description_coverage, topics_coverage = st.columns(3)

    with readme_coverage:
        st.metric(
            "README coverage",
            f"{readme_analysis['readme_coverage']}%"
        )
        st.caption(
            f"{readme_analysis['with_readme']} of "
            f"{repository_summary['original']} repositories"
        )

    with description_coverage:
        st.metric(
            "Description coverage",
            f"{metadata_analysis['description_coverage']}%"
        )
        st.caption(
            f"{metadata_analysis['with_description']} of "
            f"{repository_summary['original']} repositories"
        )

    with topics_coverage:
        st.metric(
            "Topics coverage",
            f"{metadata_analysis['topics_coverage']}%"
        )
        st.caption(
            f"{metadata_analysis['with_topics']} of "
            f"{repository_summary['original']} repositories"
        )

    # Repository activity
    st.subheader("Repository Activity")

    (
        activity_column_1,
        activity_column_2,
        activity_column_3,
        activity_column_4
    ) = st.columns(4)

    with activity_column_1:
        st.metric(
            "Last 90 days",
            freshness_buckets["last_90_days"]
        )

    with activity_column_2:
        st.metric(
            "3 months - 1 year",
            freshness_buckets["91_to_365_days"]
        )

    with activity_column_3:
        st.metric(
            "1-2 years",
            freshness_buckets["1_to_2_years"]
        )

    with activity_column_4:
        st.metric(
            "Over 2 years",
            freshness_buckets["over_2_years"]
        )

    st.write("Recently updated")

    for repository in sorted_repositories[:3]:
        st.write(
            f"{repository['name']} — "
            f"{repository['pushed_at'].strftime('%Y-%m-%d')}"
        )

    # Repositories
    st.subheader("Repositories")

    repositories_per_page = 6
    total_pages = math.ceil(
        len(repository_details) / repositories_per_page
    )

    start_index = (
        (st.session_state.repository_page - 1)
        * repositories_per_page
    )
    end_index = start_index + repositories_per_page

    page_repositories = repository_details[start_index:end_index]

    repository_columns = st.columns(3)

    for index, repository in enumerate(page_repositories):
        column = repository_columns[index % 3]

        with column:
            with st.container(border=True):
                st.write(repository["name"])
                st.write(
                    repository["description"]
                    or "No description provided."
                )

                if repository["languages"]:
                    languages = ", ".join(repository["languages"])
                    st.write("Languages:", languages)
                else:
                    st.write("Languages unavailable")

                if repository["topics"]:
                    topics = ", ".join(repository["topics"])
                    st.write("Topics:", topics)
                else:
                    st.write("No topics")

                if repository["has_readme"] is True:
                    st.write("README: Yes")
                elif repository["has_readme"] is False:
                    st.write("README: No")
                else:
                    st.write("README: Unknown")

                st.write(
                    "Stars:",
                    repository["stargazers_count"]
                )
                st.write(
                    "Forks:",
                    repository["forks_count"]
                )

                if repository["pushed_at"]:
                    clean_timestamp = repository["pushed_at"].replace(
                        "Z",
                        "+00:00"
                    )
                    dt_object = datetime.fromisoformat(clean_timestamp)
                    formatted_date = dt_object.strftime("%Y-%m-%d")
                    st.write(f"Updated: {formatted_date}")
                else:
                    st.write("Updated date unavailable")

                st.link_button(
                    "View on GitHub",
                    repository["html_url"]
                )

    previous_column, page_column, next_column = st.columns(3)

    with previous_column:
        if st.button(
            "← Previous",
            disabled=st.session_state.repository_page == 1
        ):
            st.session_state.repository_page -= 1
            st.rerun()

    with page_column:
        st.write(
            f"Page {st.session_state.repository_page} "
            f"of {total_pages}"
        )

    with next_column:
        if st.button(
            "Next →",
            disabled=st.session_state.repository_page == total_pages
        ):
            st.session_state.repository_page += 1
            st.rerun()