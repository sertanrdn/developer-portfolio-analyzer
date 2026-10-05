import streamlit as st
import altair as alt

def render_languages(
    primary_language_percentages,
    detailed_language_counts
):
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

    for language, repo_count in detailed_language_counts.items():
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