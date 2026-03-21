import streamlit as st


def show_score_cards(report):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "ATS Score",
            f"{round(report['final_score'], 2)}"
        )

    with col2:
        st.metric(
            "Experience Alignment",
            round(report["experience_alignment"], 2)
        )

    with col3:
        st.metric(
            "Semantic Fit",
            round(report["semantic_fit"], 2)
        )