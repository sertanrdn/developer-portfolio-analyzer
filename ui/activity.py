import streamlit as st


def render_activity(freshness_buckets, sorted_repositories):
    st.markdown(
        """
        <div class="section-header">
            <h2>Repository Activity</h2>
            <p>
                How recently your original repositories have been updated.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    activity_column_1, activity_column_2, activity_column_3, activity_column_4 = st.columns(4)

    activity_data = [
        ("Last 90 days", freshness_buckets["last_90_days"]),
        ("91–365 days", freshness_buckets["91_to_365_days"]),
        ("1–2 years", freshness_buckets["1_to_2_years"]),
        ("Over 2 years", freshness_buckets["over_2_years"]),
    ]

    for column, (label, value) in zip(
        (
            activity_column_1,
            activity_column_2,
            activity_column_3,
            activity_column_4,
        ),
        activity_data,
    ):
        with column:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="activity-card">
                        <div class="activity-card-label">
                            {label}
                        </div>
                        <div class="activity-card-value">
                            {value}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown(
        """
        <div class="activity-recent-header">
            <h3>Recently updated</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container(border=True):
        for index, repository in enumerate(sorted_repositories[:3]):
            st.markdown(
                f"""
                <div class="activity-repository">
                    <div class="activity-repository-row">
                        <span class="activity-repository-name">
                            {repository["name"]}
                        </span>
                        <span class="activity-repository-date">
                            {repository["pushed_at"].strftime("%Y-%m-%d")}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if index < 2:
                st.markdown(
                    '<div class="activity-divider"></div>',
                    unsafe_allow_html=True
                )