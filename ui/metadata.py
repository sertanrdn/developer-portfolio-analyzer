import streamlit as st

def render_metadata(metadata_analysis, readme_analysis, repository_summary):
    # Portfolio metadata
    st.markdown(
        """
        <div class="section-header">
            <h2>Portfolio Metadata</h2>
            <p>
                How consistently original repositories include documentation
                and descriptive information.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    readme_coverage, description_coverage, topics_coverage = st.columns(3)

    readme_known = readme_analysis["with_readme"] + readme_analysis["without_readme"]
    readme_unknown = readme_analysis["unknown_readme"]

    readme_count_text = f"{readme_analysis['with_readme']} of {readme_known} repositories"
    if readme_unknown:
        readme_count_text += f" · {readme_unknown} unknown"

    with readme_coverage:
        with st.container(border=True):
            st.markdown(
                f"""
    <div class="coverage-card">
        <div class="coverage-label">README coverage</div>
        <div class="coverage-value">
            {readme_analysis["readme_coverage"]:.1f}%
        </div>
        <div class="coverage-track">
            <div
                class="coverage-fill"
                style="width: {readme_analysis['readme_coverage']}%;"
            ></div>
        </div>
        <div class="coverage-count">
            {readme_count_text}
        </div>
    </div>
                """,
                unsafe_allow_html=True
            )

    with description_coverage:
        with st.container(border=True):
            st.markdown(
                f"""
    <div class="coverage-card">
        <div class="coverage-label">Description coverage</div>
        <div class="coverage-value">
            {metadata_analysis["description_coverage"]:.1f}%
        </div>
        <div class="coverage-track">
            <div
                class="coverage-fill"
                style="width: {metadata_analysis['description_coverage']}%;"
            ></div>
        </div>
        <div class="coverage-count">
            {metadata_analysis["with_description"]} of
            {repository_summary["original"]} repositories
        </div>
    </div>
                """,
                unsafe_allow_html=True
            )

    with topics_coverage:
        with st.container(border=True):
            st.markdown(
                f"""
    <div class="coverage-card">
        <div class="coverage-label">Topics coverage</div>
        <div class="coverage-value">
            {metadata_analysis["topics_coverage"]:.1f}%
        </div>
        <div class="coverage-track">
            <div
                class="coverage-fill"
                style="width: {metadata_analysis['topics_coverage']}%;"
            ></div>
        </div>
        <div class="coverage-count">
            {metadata_analysis["with_topics"]} of
            {repository_summary["original"]} repositories
        </div>
    </div>
                """,
                unsafe_allow_html=True
            )