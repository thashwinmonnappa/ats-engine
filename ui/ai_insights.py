from fastapi import HTTPException
import streamlit as st
import requests

def safe_list(x):
    if isinstance(x, set):
        return list(x)
    return x or []

def show_ai_insights(preview: dict, backend_url: str, auth_headers: dict):
    """
    AI-powered resume improvement insights tab.
    Calls the backend /generate-insights route which hits HuggingFace API.
    Results cached in session_state so we don't re-call on every rerun.
    """

    st.subheader("AI Resume Insights")
    st.caption("Powered by meta-llama — personalised tips based on your resume vs JD")

    # Cache key based on the analysis so insights regenerate if resume changes
    cache_key = "ai_insights_text"

    if cache_key not in st.session_state:
        st.session_state[cache_key] = None

    if st.session_state[cache_key]:
        st.markdown(st.session_state[cache_key])
        if st.button("Regenerate Insights"):
            st.session_state[cache_key] = None
            st.rerun()
        return

    if st.button("Generate AI Insights"):
        with st.spinner("Analysing your resume with AI..."):
            try:
                payload = {
                    "matched_skills": safe_list(preview.get("matched_skills")),
                    "missing_skills": safe_list(preview.get("missing_skills")),
                    "jd_skills": safe_list(preview.get("jd_skills")),
                    "resume_skills": safe_list(preview.get("resume_skills")),
                    "final_score": float(preview.get("final_score", 0)),
                    "experience_alignment": float(preview.get("experience_alignment", 0)),
                }

                res = requests.post(
                    f"{backend_url}/generate-insights",
                    json=payload,
                    headers=auth_headers,   # ✅ KEEP THIS (explained below)
                    timeout=60,
                )


                if res.status_code == 200:
                    insights = res.json().get("insights", "")
                    st.session_state[cache_key] = insights
                    st.rerun()

                else:
                    st.error(f"Could not generate insights: {res.text}")

            except requests.exceptions.Timeout:
                st.error("Request timed out. HuggingFace free tier can be slow — try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
