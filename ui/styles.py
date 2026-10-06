import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>
        /* Main application */
        .stApp {
            background-color: #f6f7fb;
            color: #111827;
        }

        /* Main content area */
        .block-container {
            max-width: 1180px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        /* Headings */
        h1, h2, h3 {
            color: #111827;
            letter-spacing: -0.02em;
        }

        h1{
            font-weight: 700;
        }

        p {
            color: #64748b;
        }

        /* Inputs */
        div[data-baseweb="input"] {
            border-radius: 8px;
        }

        /* Buttons */
        .stButton > button {
            min-height: 40px;
            border: 1px solid #4f46e5;
            border-radius: 8px;
            background-color: #4f46e5;
            color: #ffffff;
            font-weight: 600;
        }

        .stButton > button p {
            color: #ffffff;
        }

        .stButton > button:hover {
            border-color: #4338ca;
            background-color: #4338ca;
            color: #ffffff;
        }

        .stButton > button:hover p {
            color: #ffffff;
        }

        /* Application header */
        .app-header {
            max-width: 720px;
            margin: 0 auto 2.5rem auto;
            text-align: center;
        }

        .app-header h1 {
            margin: 0;
            font-size: 2.35rem;
            line-height: 1.15;
        }

        .app-description {
            margin: 0.75rem auto 0 auto;
            max-width: 650px;
            font-size: 1rem;
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )