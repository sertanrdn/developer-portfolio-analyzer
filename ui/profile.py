import streamlit as st
from datetime import datetime

def render_profile(profile):
    st.markdown(
        """
        <div class="section-header">
            <h2>Developer Profile</h2>
            <p>A snapshot of the developer's public GitHub presence.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Profile
    display_name = (
        profile.get("name")
        or profile.get("login")
    )
    bio = profile.get("bio") or "No bio provided."

    created_at = profile.get("created_at")
    member_since = datetime.fromisoformat(created_at)

    with st.container(border=True):
        avatar_column, profile_column = st.columns([1, 4])

        with avatar_column:
            st.image(profile["avatar_url"], width=150)

        with profile_column:
            st.subheader(display_name)
            st.caption(f"@{profile['login']}")
            st.write(bio)

            if profile.get("location"):
                st.write("📍", profile["location"])

            if profile.get("company"):
                st.write("🏢", profile["company"])

            st.link_button(
                "View GitHub profile ↗",
                profile["html_url"]
            )

        st.divider()

        repos_column, followers_column, following_column, member_column = (
            st.columns(4)
        )

        with repos_column:
            st.markdown(
                f"""
                <div class="profile-metric">
                    <div class="profile-metric-label">
                        Public repositories
                    </div>
                    <div class="profile-metric-value">
                        {profile["public_repos"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with followers_column:
            st.markdown(
                f"""
                <div class="profile-metric">
                    <div class="profile-metric-label">
                        Followers
                    </div>
                    <div class="profile-metric-value">
                        {profile["followers"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with following_column:
            st.markdown(
                f"""
                <div class="profile-metric">
                    <div class="profile-metric-label">
                        Following
                    </div>
                    <div class="profile-metric-value">
                        {profile["following"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with member_column:
            st.markdown(
                f"""
                <div class="profile-metric">
                    <div class="profile-metric-label">
                        Member Since
                    </div>
                    <div class="profile-metric-value">
                        {member_since.year}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )