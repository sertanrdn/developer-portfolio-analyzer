import streamlit as st
import altair as alt

LANGUAGE_COLORS = {
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Python": "#3572A5",
    "HTML": "#e34c26",
    "CSS": "#663399",
    "Vue": "#41b883",
    "Java": "#b07219",
    "C": "#555555",
    "C++": "#f34b7d",
    "C#": "#178600",
    "PHP": "#4F5D95",
    "Ruby": "#701516",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "Swift": "#F05138",
    "Kotlin": "#A97BFF",
    "Dart": "#00B4AB",
    "Shell": "#89e051",
    "Jupyter Notebook": "#DA5B0B",
    "SCSS": "#c6538c",
    "Svelte": "#ff3e00",
    "Astro": "#ff5a03",
    "PLpgSQL": "#336790",
}

DEFAULT_LANGUAGE_COLOR = "#94a3b8"

def render_languages(
    primary_language_percentages,
    detailed_language_counts
):
    # Languages
    st.markdown(
        """
        <div class="section-header">
            <h2>Languages</h2>
            <p>
                See which technologies lead the portfolio and how broadly
                they appear across projects.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    language_chart_data = []

    for language, percentage in primary_language_percentages.items():
        language_chart_data.append(
            {
                "language": language,
                "percentage": percentage
            }
        )

    language_names = list(primary_language_percentages.keys())

    language_colors = [
        LANGUAGE_COLORS.get(language, DEFAULT_LANGUAGE_COLOR)
        for language in language_names
    ]

    language_chart = (
        alt.Chart(alt.Data(values=language_chart_data))
        .mark_arc(
            innerRadius=65,
            outerRadius=105
        )
        .encode(
            theta=alt.Theta("percentage:Q"),
            color=alt.Color(
                "language:N",
                scale=alt.Scale(
                    domain=language_names,
                    range=language_colors
                ),
                legend=None
            ),
            tooltip=[
                alt.Tooltip("language:N", title="Language"),
                alt.Tooltip(
                    "percentage:Q",
                    title="Share",
                    format=".1f"
                )
            ]
        )
        .properties(
            height=240
        )
    )

    sorted_primary_languages = sorted(
        primary_language_percentages.items(),
        key=lambda item: item[1],
        reverse=True
    )

    language_bar_data = []

    for language, repo_count in detailed_language_counts.items():
        language_bar_data.append(
            {
                "language": language,
                "repositories": repo_count
            }
        )

    detailed_language_names = list(detailed_language_counts.keys())

    detailed_language_colors = [
        LANGUAGE_COLORS.get(language, DEFAULT_LANGUAGE_COLOR)
        for language in detailed_language_names
    ]

    max_repository_count = max(
        detailed_language_counts.values(),
        default=0
    )

    x_axis_max = max_repository_count + 2

    language_bar_chart = (
        alt.Chart(alt.Data(values=language_bar_data))
        .mark_bar()
        .encode(
            x=alt.X(
                "repositories:Q",
                scale=alt.Scale(
                    domain=[0, x_axis_max]
                ),
                axis=alt.Axis(tickMinStep=1)
            ),
            y=alt.Y("language:N", sort="-x"),
            color=alt.Color(
                "language:N",
                scale=alt.Scale(
                    domain=detailed_language_names,
                    range=detailed_language_colors
                ),
                legend=None
            ),
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
        with st.container(border=True):
            st.markdown(
                """
                <div class="chart-header">
                    <h3>Primary languages</h3>
                    <p>
                        Main language assigned to each original repository.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.altair_chart(
                language_chart,
                use_container_width=True
            )

            for language, percentage in sorted_primary_languages:
                language_color = LANGUAGE_COLORS.get(
                    language,
                    DEFAULT_LANGUAGE_COLOR
                )

                st.markdown(
                    f"""
            <div class="language-legend-row">
                <div class="language-legend-language">
                    <span
                        class="language-color-dot"
                        style="background-color: {language_color};"
                    ></span>
                    <span class="language-legend-name">{language}</span>
                </div>
                <span class="language-legend-percentage">{percentage:.1f}%</span>
            </div>
                    """,
                    unsafe_allow_html=True
                )

    with detailed_language_column:
        with st.container(border=True):
            st.markdown(
                """
                <div class="chart-header">
                    <h3>Languages across projects</h3>
                    <p>
                        Languages detected across original repositories.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.altair_chart(
                language_bar_chart,
                use_container_width=True
            )