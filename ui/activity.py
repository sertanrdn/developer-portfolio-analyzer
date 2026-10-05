import streamlit as st

def render_activity(freshness_buckets, sorted_repositories):
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