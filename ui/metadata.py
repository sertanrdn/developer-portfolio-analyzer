import streamlit as st

def render_metadata(metadata_analysis, readme_analysis, repository_summary):
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