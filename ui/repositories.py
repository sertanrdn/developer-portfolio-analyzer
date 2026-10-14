
import math
from datetime import datetime

import streamlit as st


def render_repositories(repository_details):
    st.markdown(
        """
        <div class="section-header">
            <h2>Repositories</h2>
            <p>Explore projects, technologies, and repository details.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    repositories_per_page = 6
    total_pages = max(
        1, math.ceil(len(repository_details) / repositories_per_page)
    )

    # Keep the current page valid when a new profile has fewer repositories.
    st.session_state.repository_page = min(
        max(1, st.session_state.repository_page), total_pages
    )

    start_index = (st.session_state.repository_page - 1) * repositories_per_page
    page_repositories = repository_details[
        start_index : start_index + repositories_per_page
    ]

    columns = st.columns(3)

    for index, repository in enumerate(page_repositories):
        with columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    f'<div class="repo-card-title">{repository["name"]}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div class="repo-card-stats">
                        <span>★ {repository["stargazers_count"]} stars</span>
                        <span>⑂ {repository["forks_count"]} forks</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="repo-card-description">'
                    f'{repository["description"] or "No description provided."}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                languages = repository.get("languages") or []
                if languages:
                    language_badges = "".join(
                        f'<span class="repo-badge">{language}</span>'
                        for language in languages
                    )
                    st.markdown(
                        f'<div class="repo-card-badges">{language_badges}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption("Languages unavailable")

                topics = repository.get("topics") or []
                if topics:
                    topic_badges = "".join(
                        f'<span class="repo-badge repo-topic">{topic}</span>'
                        for topic in topics
                    )
                    st.markdown(
                        f'<div class="repo-card-badges">{topic_badges}</div>',
                        unsafe_allow_html=True,
                    )

                has_readme = repository.get("has_readme")
                if has_readme is True:
                    readme_label = "README available"
                elif has_readme is False:
                    readme_label = "README missing"
                else:
                    readme_label = "README unknown"

                pushed_at = repository.get("pushed_at")
                if pushed_at:
                    timestamp = pushed_at.replace("Z", "+00:00")
                    updated_date = datetime.fromisoformat(timestamp).strftime(
                        "%b %d, %Y"
                    )
                else:
                    updated_date = "Date unavailable"

                st.markdown(
                    f"""
                    <div class="repo-card-footer">
                        <span>{readme_label}</span>
                        <span>Updated {updated_date}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.link_button("View on GitHub ↗", repository["html_url"])

    _, previous, page, next_button, _ = st.columns([3, 1.2, 1.5, 1.2, 3])

    with previous:
        if st.button(
            "← Previous",
            disabled=st.session_state.repository_page <= 1,
            key="repositories_previous",
            width="stretch",
        ):
            st.session_state.repository_page -= 1
            st.rerun()

    with page:
        st.markdown(
            f'<div class="repo-pagination">Page '
            f'{st.session_state.repository_page} of {total_pages}</div>',
            unsafe_allow_html=True,
        )

    with next_button:
        if st.button(
            "Next →",
            disabled=st.session_state.repository_page >= total_pages,
            key="repositories_next",
            width="stretch",
        ):
            st.session_state.repository_page += 1
            st.rerun()
