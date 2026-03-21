import sys
import os
import tempfile
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from skill_comparison_table import show_skill_comparison

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pipeline.ats_pipeline_v2 import ATSPipelineV2
from score_cards import show_score_cards
from radar_chart import radar_chart
from skill_gap_panel import show_skill_gap


st.set_page_config(
    page_title="AI Resume ATS Analyzer",
    layout="wide"
)

pipeline = ATSPipelineV2()

# ------------------------------
# HEADER
# ------------------------------

st.title("AI Resume ATS Analyzer")
st.markdown(
    "AI-powered ATS resume analysis with semantic skill matching and ontology intelligence."
)

# ------------------------------
# SIDEBAR INPUTS
# ------------------------------

with st.sidebar:

    st.header("Upload Inputs")

    resume_files = st.file_uploader(
        "Upload Resume(s)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    jd_file = st.file_uploader(
        "Upload Job Description",
        type=["pdf", "docx", "txt"]
    )

    jd_text = st.text_area("Or Paste Job Description")

    analyze_btn = st.button("Analyze Resumes")


# ------------------------------
# SCORE GAUGE
# ------------------------------

def score_gauge(score):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "ATS Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#00C853"}
        }
    ))

    return fig


# ------------------------------
# ANALYSIS
# ------------------------------

if analyze_btn:

    if not resume_files:
        st.warning("Please upload at least one resume.")
        st.stop()

    if not jd_file and not jd_text:
        st.warning("Please upload or paste a job description.")
        st.stop()

    # Handle JD input
    if jd_file:

        suffix = os.path.splitext(jd_file.name)[1].lower()
        temp_path = tempfile.NamedTemporaryFile(delete=False).name + suffix

        with open(temp_path, "wb") as f:
            f.write(jd_file.read())

        jd_input = temp_path

    else:
        jd_input = jd_text

    results = []

    # ------------------------------
    # PROCESS RESUMES
    # ------------------------------

    for file in resume_files:

        suffix = os.path.splitext(file.name)[1].lower()
        temp_path = tempfile.NamedTemporaryFile(delete=False).name + suffix

        with open(temp_path, "wb") as f:
            f.write(file.read())

        resume_path = temp_path

        try:
            report = pipeline.analyze(resume_path, jd_input)

        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")
            continue

        results.append({
            "name": file.name,
            "score": report["final_score"],
            "report": report
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    st.divider()

    # ------------------------------
    # CANDIDATE RANKING
    # ------------------------------

    st.subheader("Candidate Ranking")

    ranking_table = pd.DataFrame([
        {
            "Rank": i + 1,
            "Candidate": r["name"],
            "ATS Score": round(r["score"], 2)
        }
        for i, r in enumerate(results)
    ])

    st.dataframe(
        ranking_table,
        use_container_width=True,
        hide_index=True
    )

    # ------------------------------
    # TOP CANDIDATE ANALYSIS
    # ------------------------------

    if results:

        top_report = results[0]["report"]

        st.divider()
        st.subheader("Top Candidate Analysis")

        col1, col2 = st.columns([2, 1])

        with col1:
            show_score_cards(top_report)

        with col2:
            st.plotly_chart(
                score_gauge(top_report["final_score"]),
                use_container_width=True,
                key="score_gauge"
            )

        st.divider()

        col1, col2 = st.columns([2, 1])

        with col1:
            show_skill_gap(top_report)

        with col2:
            fig = radar_chart(top_report)
            st.plotly_chart(
                fig,
                use_container_width=True,
                key="radar_chart"
            )
        st.divider()

        show_skill_comparison(top_report)
    else:

        st.warning("No resumes were successfully processed.")