import streamlit as st
from datetime import datetime

def render_profile(profile):
    # Profile
    display_name = (
        profile.get("name")
        or profile.get("login")
    )
    bio = profile.get("bio") or "No bio provided."

    created_at = profile.get("created_at")
    member_since = datetime.fromisoformat(created_at)

    avatar_column, profile_column = st.columns([1, 3])

    with avatar_column:
        st.image(profile["avatar_url"])

    with profile_column:
        st.subheader(display_name)
        st.subheader(f"@{profile['login']}")
        st.write(bio)

        if profile.get("location"):
            st.write("📍", profile["location"])

        if profile.get("company"):
            st.write("🏢", profile["company"])

        st.link_button(
            "View GitHub profile",
            profile["html_url"]
        )

    repos_column, followers_column, following_column, member_column = (
        st.columns(4)
    )

    with repos_column:
        st.metric(
            "Public repositories",
            profile["public_repos"]
        )

    with followers_column:
        st.metric("Followers", profile["followers"])

    with following_column:
        st.metric("Following", profile["following"])

    with member_column:
        st.metric("Member Since", member_since.year)