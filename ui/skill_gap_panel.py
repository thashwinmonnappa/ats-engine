import streamlit as st


def skill_tags(skills, color):

    html = ""

    for s in skills:
        html += f"""
        <span style="
            background:{color};
            padding:6px 10px;
            margin:4px;
            border-radius:8px;
            display:inline-block;
            color:white;
            font-size:12px;
        ">
        {s}
        </span>
        """

    st.markdown(html, unsafe_allow_html=True)


def show_skill_gap(report):

    st.subheader("Skill Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Matched Skills")
        skill_tags(report["matched_skills"], "#00C853")

    with col2:
        st.markdown("### ❌ Missing Skills")
        skill_tags(report["missing_skills"], "#FF5252")