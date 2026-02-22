import streamlit as st
import os
from app.main import run_pipeline

st.set_page_config(layout="wide")

st.title("AI Resume Screening Dashboard")

jd_file = st.file_uploader(
    "Upload Job Description",
    type=["pdf", "docx", "txt"]
)

resume_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if jd_file and resume_files:

    jd_path = f"temp_{jd_file.name}"

    with open(jd_path, "wb") as f:
        f.write(jd_file.getbuffer())

    results = []

    progress_bar = st.progress(0)

    for idx, resume in enumerate(resume_files):

        resume_path = f"temp_{resume.name}"

        with open(resume_path, "wb") as f:
            f.write(resume.getbuffer())

        report = run_pipeline(resume_path, jd_path)
        report["resume_file"] = resume.name
        results.append(report)

        os.remove(resume_path)
        progress_bar.progress((idx + 1) / len(resume_files))

    os.remove(jd_path)

    results = sorted(results, key=lambda x: x["final_score"], reverse=True)

    st.subheader("Ranked Candidates")

    for candidate in results:

        with st.expander(
            f"{candidate['resume_file']} — Score: {candidate['final_score']}"
        ):

            col1, col2, col3 = st.columns(3)

            col1.metric("Experience", candidate["experience_alignment"])
            col2.metric("Skill Coverage", candidate["skill_coverage"])
            col3.metric("Semantic Fit", candidate["semantic_fit"])

            st.metric("Confidence", candidate["confidence"])

            st.write("### Verdict")
            st.write(candidate["explanation"]["verdict"])

            st.write("### Experience Gap")
            st.write(candidate["explanation"]["experience_gap"])

            st.write("### Missing Skills")
            st.write(candidate.get("missing_skills", [])[:10])