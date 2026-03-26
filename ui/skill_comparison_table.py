import pandas as pd
import streamlit as st


def show_skill_comparison(report):

    jd_skills = set(report["jd_skills"])
    resume_skills = set(report["resume_skills"])

    rows = []

    for skill in sorted(jd_skills):

        rows.append(
            {
                "Skill": skill,
                "Required in JD": "✓",
                "Present in Resume": "✓" if skill in resume_skills else "✗",
            }
        )

    df = pd.DataFrame(rows)

    st.subheader("Resume vs JD Skill Comparison")

    # ------------------------------
    # Optional Visual Upgrade
    # ------------------------------

    def highlight_row(row):

        if row["Present in Resume"] == "✓":
            return ["background-color:#0f5132"] * len(row)  # green row
        else:
            return ["background-color:#842029"] * len(row)  # red row

    styled = df.style.apply(highlight_row, axis=1)

    st.dataframe(styled, use_container_width="auto", hide_index=True)
