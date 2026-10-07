import streamlit as st

def render_repository_overview(repository_summary):
    # Repository overview
    st.markdown(
        """
        <div class="section-header">
            <h2>Repository Overview</h2>
            <p>How the public repositories in this portfolio are structured.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    original_repos, forked_repos, archived_repos = st.columns(3)

    with original_repos:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="overview-metric">
                    <div class="overview-metric-label">
                        Original repositories
                    </div>
                    <div class="overview-metric-value">
                        {repository_summary["original"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with forked_repos:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="overview-metric">
                    <div class="overview-metric-label">
                        Forked repositories
                    </div>
                    <div class="overview-metric-value">
                        {repository_summary["forked"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with archived_repos:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="overview-metric">
                    <div class="overview-metric-label">
                        Archived repositories
                    </div>
                    <div class="overview-metric-value">
                        {repository_summary["archived"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
