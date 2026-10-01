import os
import streamlit as st

from dotenv import load_dotenv
from datetime import datetime

from github_api import fetch_user_profile
from analysis import process_user_profile

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

st.title("Developer Portfolio Analyzer")
st.write("Analyze a developer's public GitHub portfolio.")

username = st.text_input("GitHub username")

analyze_button = st.button("Analyze")

if analyze_button:
    cleaned_username = username.strip()
    if not cleaned_username:
        st.error("Error: You need to enter a username")
    else:
        user_profile = fetch_user_profile(
            username=cleaned_username, github_token=github_token
        )

        if user_profile is not None:
            processed_user_profile = process_user_profile(
                user_profile=user_profile
            )
            display_name = (
                processed_user_profile.get("name") 
                or processed_user_profile.get("login")
            )
            bio = processed_user_profile.get("bio") or "No bio provided."

            created_at = processed_user_profile.get("created_at")
            member_since = datetime.fromisoformat(created_at)

            avatar_column, profile_column = st.columns([1, 3])

            with avatar_column:
                st.image(processed_user_profile["avatar_url"])
            with profile_column:
                st.subheader(display_name)
                st.subheader(f"@{processed_user_profile['login']}")
                st.write(bio)
        
                if processed_user_profile.get("location"):
                    st.write("📍", processed_user_profile["location"])
                
                if processed_user_profile.get("company"):
                    st.write("🏢", processed_user_profile["company"])
                
                st.link_button(
                    "View GitHub profile", processed_user_profile["html_url"]
                )

            repos_column, followers_column, following_column, member_column = st.columns(4)

            with repos_column:
                st.metric("Public repositories", processed_user_profile["public_repos"])
            with followers_column:
                st.metric("Followers", processed_user_profile["followers"])
            with following_column:
                st.metric("Following", processed_user_profile["following"])
            with member_column:
                st.metric("Member Since", member_since.year)
    
        else:
            st.error("Could not load this GitHub profile.")