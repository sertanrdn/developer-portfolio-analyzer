import streamlit as st

st.title("Developer Portfolio Analyzer")
st.write("Analyze a developer's public GitHub portfolio.")

username = st.text_input("GitHub username")

analyze_button = st.button("Analyze")

if analyze_button:
    cleaned_username = username.strip()
    if not cleaned_username:
        st.error("Error: You need to enter a username")
    else:
        st.write("Analyzing:", cleaned_username)