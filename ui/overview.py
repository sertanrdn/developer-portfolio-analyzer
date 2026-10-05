import streamlit as st

def render_repository_overview(repository_summary):
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
