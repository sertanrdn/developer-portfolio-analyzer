import math
import streamlit as st
from datetime import datetime 

def render_repositories(repository_details):
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