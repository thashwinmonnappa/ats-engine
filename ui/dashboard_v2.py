# ui/dashboard_v2.py

import sys
import os
import tempfile
import streamlit as st
import requests
import time

from skill_comparison_table import show_skill_comparison

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pipeline.ats_pipeline_v2 import ATSPipelineV2
from score_cards import show_score_cards
from radar_chart import radar_chart
from skill_gap_panel import show_skill_gap
from ai_insights import show_ai_insights

# -----------------------------------
# CONFIG
# -----------------------------------
# BACKEND_URL = "http://127.0.0.1:8000"  # Local backend (for development)
# BACKEND_URL = (
#     "https://ats-engine-production.up.railway.app"  # Deployed backend (for production)
# )

PRIMARY_BACKEND = "https://ats-engine-production.up.railway.app"
FALLBACK_BACKEND = "http://127.0.0.1:8000"
def get_backend_url():
    try:
        res = requests.get(f"{PRIMARY_BACKEND}/docs", timeout=2)
        if res.status_code == 200:
            return PRIMARY_BACKEND
    except:
        pass
    return FALLBACK_BACKEND
BACKEND_URL = get_backend_url()

st.set_page_config(page_title="AI Resume ATS Analyzer", layout="wide")

st.markdown(
    """
<style>
.header-box {
    background: linear-gradient(135deg, #114523, #111827);
    padding: 25px 30px;
    border-radius: 14px;
    border: 1px solid #2a2f3a;
    box-shadow: 0 6px 25px rgba(0,0,0,0.4);
    margin-bottom: 25px;
    text-align: center;
}

.header-title {
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 10px;
}

.header-sub {
    color: #9ca3af;
    font-size: 15px;
    font-weight: 500;
}

/* Logout button styling */
div[data-testid="stButton"] > button {
    # background-color: #3b161b;
    color: white;
    border: slategray 2px solid;
    padding: 10px 15px;
    border-radius: 15px;
    font-size: 15px;
    cursor: pointer;
}

div[data-testid="stButton"] > button:hover {
    background-color: #0d4d38;
}
            
.login-card {
    background: linear-gradient(135deg, #520202, #111d27);
    padding: 30px;
    border-radius: 16px;
    border: 1px solid #2a2f3a;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    margin-bottom: 20px;
    text-align: center;
}

.login-title {
    font-size: 25px;
    font-weight: 600;
    margin-bottom: 10px;
}
            
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def load_pipeline():
    return ATSPipelineV2()


pipeline = load_pipeline()


# -----------------------------------
# SESSION STATE INIT
# -----------------------------------
for key, default in {
    "user_email": None,
    "token": None,
    "paid_user": False,
    "analysis_done": False,
    "results": None,
    "payment_link": None,
    "last_input": "",
    "last_check_time": 0,
    "returning_from_payment": False,
    "payment_warning": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# -----------------------------------
# AUTH HEADER HELPER
# -----------------------------------
def auth_headers() -> dict:
    return {"Authorization": f"Bearer {st.session_state['token']}"}


# -----------------------------------
# RESTORE SESSION FROM URL (after Razorpay redirect)
# -----------------------------------
# Razorpay redirects back to:
#   http://localhost:8501?token=xxx&email=yyy
#
# We restore token + email, then fetch saved results from Supabase
# so the report renders immediately without re-uploading files.
params = st.query_params

if not st.session_state["token"] and "token" in params:
    token = params["token"]
    email = params["email"]

    st.session_state["token"] = token
    st.session_state["user_email"] = email
    st.session_state["returning_from_payment"] = True

    # Fetch previously saved results from Supabase
    try:
        res = requests.get(
            f"{BACKEND_URL}/get-results", headers={"Authorization": f"Bearer {token}"}
        )
        if res.status_code == 200:
            saved = res.json().get("results")
            if saved:
                st.session_state["results"] = saved
                st.session_state["analysis_done"] = True
    except Exception:
        pass  # Non-critical — user just needs to re-upload if this fails

    st.query_params.clear()
    st.rerun()


# -----------------------------------
# LOGIN
# -----------------------------------
if not st.session_state["token"]:

    # Center using columns (REAL fix)
    col1, col2, col3 = st.columns([2, 3, 2])

    with col2:
        st.markdown(
            """
        <div class="login-card">
            <div class="header-title"> 🤖 AI Resume ATS Analyzer </div>
            <div class="login-title">🔐 Login to continue</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        email = st.text_input("Enter your email")

        if st.button("Login"):
            if not email:
                st.warning("Please enter your email")
                st.stop()

            try:
                res = requests.post(f"{BACKEND_URL}/login", json={"email": email})

                if res.status_code == 200:
                    data = res.json()
                    st.session_state["user_email"] = data["email"]
                    st.session_state["token"] = data["token"]
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error(f"Login failed: {res.text}")

            except Exception as e:
                st.error(f"Backend not reachable: {str(e)}")

    st.stop()


# -----------------------------------
# CHECK PAYMENT
# -----------------------------------
try:
    res = requests.get(f"{BACKEND_URL}/check-payment", headers=auth_headers())

    if res.status_code == 200:
        st.session_state["paid_user"] = res.json()["paid"]

    elif res.status_code == 401:
        if st.session_state.get("token"):  # only clear if we actually had a token
            st.warning("Session expired. Please log in again.")
            st.session_state.clear()
            st.rerun()

except Exception as e:
    st.error(f"Could not reach backend: {str(e)}")

# -----------------------------------
# HEADER + LOGOUT
# -----------------------------------
with st.container():

    col1, col2 = st.columns([6, 1])

    with col1:
        st.markdown(
            f"""
        <div class="header-box">
            <div class="header-title"> 🤖 AI Resume ATS Analyzer </div>
            <div class="header-sub">Logged in as 👤: {st.session_state['user_email']} </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        if st.button("🚪 Logout", key="logout_button"):
            st.session_state.clear()
            st.rerun()

# -----------------------------------
# SIDEBAR INPUTS
# -----------------------------------
with st.sidebar:
    resume_files = st.file_uploader(
        "Upload Resume(s)", type=["pdf", "docx", "txt"], accept_multiple_files=True
    )

    jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"])
    jd_text = st.text_area("Or Paste Job Description")
    analyze_btn = st.button("Analyze Resumes")


# -----------------------------------
# RESET IF INPUTS CHANGE
# -----------------------------------
# Skip this entire block if returning from payment.
# The file uploaders are empty because the browser cleared them
# on redirect — the user didn't actually change anything.
current_input = str(resume_files) + str(jd_file) + jd_text

if st.session_state["returning_from_payment"]:
    # One-time flag — clear it and preserve existing results
    st.session_state["returning_from_payment"] = False

elif st.session_state["last_input"] != current_input:
    # Genuine input change — reset analysis
    st.session_state["analysis_done"] = False
    st.session_state["results"] = None
    st.session_state["payment_link"] = None
    st.session_state["last_input"] = current_input


# -----------------------------------
# PAYMENT FLOW
# -----------------------------------
def show_payment():
    if st.button("Get Full Report (PAID)"):
        try:
            res = requests.post(
                f"{BACKEND_URL}/create-payment-link",
                json={"email": st.session_state["user_email"]},
                headers=auth_headers(),
            )
            data = res.json()
            if "payment_url" not in data:
                st.error("Could not generate payment link")
                return
            st.session_state["payment_link"] = data["payment_url"]
        except Exception as e:
            st.error(f"Payment error: {str(e)}")

    if st.session_state["payment_link"]:
        st.markdown(
            f'<a href="{st.session_state["payment_link"]}" target="_blank">'
            f"Pay ₹19 (Razorpay)</a>",
            unsafe_allow_html=True,
        )
        st.info("After completing payment, click the button below.")

        if st.button("I have paid — unlock full report"):
            try:
                res = requests.get(
                    f"{BACKEND_URL}/check-payment", headers=auth_headers()
                )
                if res.status_code == 200 and res.json()["paid"]:
                    st.session_state["payment_warning"] = None
                    st.session_state["returning_from_payment"] = True
                    st.rerun()
                else:
                    st.session_state["payment_warning"] = (
                        "Payment not confirmed yet. Please complete the payment and try again."
                    )
            except Exception as e:
                st.session_state["payment_warning"] = (
                    f"Could not verify payment: {str(e)}"
                )

        # Show warning if it exists — persists across reruns
        if st.session_state.get("payment_warning"):
            st.warning(st.session_state["payment_warning"])


# -----------------------------------
# ANALYSIS TRIGGER
# -----------------------------------
if analyze_btn:
    st.session_state["analysis_done"] = True
    st.session_state["results"] = None  # clear old results on fresh analysis


# -----------------------------------
# ANALYSIS
# -----------------------------------
if st.session_state["analysis_done"]:

    # Results already in session — skip pipeline, go straight to display.
    # This happens when returning from Razorpay redirect (loaded from Supabase).
    if st.session_state["results"] is None:

        if not resume_files:
            st.warning("Please upload at least one resume")
            st.stop()

        if not jd_file and not jd_text:
            st.warning("Please add a Job Description")
            st.stop()

        # Handle JD input
        if jd_file:
            suffix = os.path.splitext(jd_file.name)[1].lower()
            temp_jd = tempfile.NamedTemporaryFile(delete=False, suffix=suffix).name
            with open(temp_jd, "wb") as f:
                f.write(jd_file.read())
            jd_input = temp_jd
        else:
            jd_input = jd_text

        # Process each resume
        results = []

        for file in resume_files:
            suffix = os.path.splitext(file.name)[1].lower()
            temp_resume = tempfile.NamedTemporaryFile(delete=False, suffix=suffix).name
            with open(temp_resume, "wb") as f:
                f.write(file.read())

            try:
                report = pipeline.analyze(temp_resume, jd_input)
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
                continue

            results.append(
                {"name": file.name, "score": report["final_score"], "report": report}
            )

        if not results:
            st.error("No valid results. Check your files and try again.")
            st.stop()

        results = sorted(results, key=lambda x: x["score"], reverse=True)
        st.session_state["results"] = results

        # Save to Supabase so results survive the Razorpay redirect
        try:
            requests.post(
                f"{BACKEND_URL}/save-results",
                json={"results": results},
                headers=auth_headers(),
            )
        except Exception:
            pass  # Non-critical

    # Render from session — works both after fresh analysis and after redirect
    preview = st.session_state["results"][0]["report"]

    # --- PREVIEW (visible to all users) ---
    st.metric("ATS Score", f"{round(preview['final_score'], 2)}%")
    st.plotly_chart(radar_chart(preview), use_container_width=True, width='stretch')

    st.subheader("**🎯 Key missing skills impacting your score:**")
    
    missing_skills = preview["missing_skills"][:5]
    cols = st.columns(len(missing_skills))
    for idx, skill in enumerate(missing_skills):
        with cols[idx]:
            st.info(f"{skill}😞")

    if preview["final_score"] < 70:
        st.error("Your resume may get filtered out by ATS systems")
    elif preview["final_score"] < 90 and preview["final_score"] >= 70:
        st.warning("Your resume is moderately ATS-friendly")
    else:
        st.success("Your resume is highly ATS-friendly")

    # --- PAYMENT GATE ---
    if not st.session_state["paid_user"]:
        show_payment()
        st.stop()

    # --- FULL REPORT (paid users only) ---
    st.subheader("Full Analysis")
 
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Score Cards",
        "🎯 Skill Gap",
        "📈 Comparison",
        "🤖 AI Insights"
    ])
 
    with tab1:
        show_score_cards(preview)
 
    with tab2:
        show_skill_gap(preview)
 
    with tab3:
        show_skill_comparison(preview)
 
    with tab4:
        show_ai_insights(preview, BACKEND_URL, auth_headers())
 