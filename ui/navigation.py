import streamlit as st

# (icon, label, anchor) - the anchor is the "#name" Streamlit made for each heading
NAVIGATION_ITEMS = [
    ("👤", "Profile", "developer-profile"),
    ("📦", "Overview", "repository-overview"),
    ("🧠", "Languages", "languages"),
    ("📋", "Metadata", "portfolio-metadata"),
    ("📈", "Activity", "repository-activity"),
    ("🗂️", "Repositories", "repositories"),
]


def render_navigation():
    links = "".join(
        f'<a class="nav-link" href="#{anchor}" target="_self">'
        f'<span>{icon}</span>{label}</a>'
        for icon, label, anchor in NAVIGATION_ITEMS
    )

    st.markdown(
        f'<nav class="section-nav">{links}</nav>',
        unsafe_allow_html=True,
    )