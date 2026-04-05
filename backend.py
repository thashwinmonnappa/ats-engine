# backend.py

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import razorpay
import os
import json
import jwt
from datetime import datetime, timedelta
from supabase import create_client, Client
import httpx
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI()
security = HTTPBearer()

# -----------------------------------
# CONFIG FROM .env
# -----------------------------------
RAZORPAY_KEY_ID     = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
SUPABASE_URL        = os.getenv("SUPABASE_URL")
SUPABASE_KEY        = os.getenv("SUPABASE_KEY")
CALLBACK_URL        = os.getenv("CALLBACK_URL", "http://localhost:8501")
HF_TOKEN            = os.getenv("HF_TOKEN")
HF_MODEL            = os.getenv("HF_MODEL")
HF_URL              = os.getenv("HF_URL")
JWT_SECRET          = os.getenv("JWT_SECRET")
JWT_ALGORITHM       = "HS256"
JWT_EXPIRY_HOURS    = 24 * 7

# -----------------------------------
# CLIENTS
# -----------------------------------
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# -----------------------------------
# SUPABASE TABLES
# -----------------------------------
# Run these once in your Supabase SQL editor:
#
#   CREATE TABLE IF NOT EXISTS users (
#       email TEXT PRIMARY KEY,
#       created_at TIMESTAMPTZ DEFAULT NOW()
#   );
#
#   CREATE TABLE IF NOT EXISTS payments (
#       id SERIAL PRIMARY KEY,
#       email TEXT NOT NULL,
#       status TEXT NOT NULL,
#       paid_at TIMESTAMPTZ DEFAULT NOW()
#   );
#
#   CREATE TABLE IF NOT EXISTS analysis_results (
#       email TEXT PRIMARY KEY,
#       results JSONB NOT NULL,
#       saved_at TIMESTAMPTZ DEFAULT NOW()
#   );
# -----------------------------------


# -----------------------------------
# PYDANTIC MODELS
# -----------------------------------
class LoginRequest(BaseModel):
    email: EmailStr


class PaymentLinkRequest(BaseModel):
    email: EmailStr


class SaveResultsRequest(BaseModel):
    results: list


class InsightsRequest(BaseModel):
    matched_skills: list
    missing_skills: list
    jd_skills: list
    resume_skills: list
    final_score: float
    experience_alignment: float


# -----------------------------------
# JWT HELPERS
# -----------------------------------
def create_jwt(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired, please login again")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    return verify_jwt(credentials.credentials)


# -----------------------------------
# LOGIN
# -----------------------------------
@app.post("/login")
async def login(body: LoginRequest):
    email = body.email
    supabase.table("users").upsert({"email": email}).execute()
    token = create_jwt(email)
    print(f"Login: {email}")
    return {"status": "ok", "email": email, "token": token}


# -----------------------------------
# CREATE PAYMENT LINK
# -----------------------------------
@app.post("/create-payment-link")
async def create_payment_link(
    body: PaymentLinkRequest, current_user: str = Depends(get_current_user)
):
    email = body.email

    if current_user != email:
        raise HTTPException(status_code=403, detail="Email mismatch")

    # Append JWT token to callback URL so Streamlit can restore session
    token = create_jwt(email)
    callback_with_token = f"{CALLBACK_URL}?token={token}&email={email}"

    payment_link = razorpay_client.payment_link.create(
        {
            "amount": 1900,
            "currency": "INR",
            "description": "ATS Resume Analysis - Full Report",
            "notes": {"email": email},
            "callback_url": callback_with_token,
            "callback_method": "get",
        }
    )

    print(f"Payment link created for {email}: {payment_link['short_url']}")
    return {"payment_url": payment_link["short_url"]}


# -----------------------------------
# CHECK PAYMENT
# -----------------------------------
@app.get("/check-payment")
async def check_payment(current_user: str = Depends(get_current_user)):
    result = (
        supabase.table("payments")
        .select("*")
        .eq("email", current_user)
        .eq("status", "success")
        .execute()
    )
    paid = len(result.data) > 0
    print(f"Payment check for {current_user}: {'paid' if paid else 'not paid'}")
    return {"paid": paid}


# -----------------------------------
# SAVE ANALYSIS RESULTS
# -----------------------------------
# Saves results to Supabase so they survive a page reload
# (e.g. after Razorpay redirects back to the app).
# Uses upsert so re-analyzing simply overwrites old results.
@app.post("/save-results")
async def save_results(
    body: SaveResultsRequest, current_user: str = Depends(get_current_user)
):
    supabase.table("analysis_results").upsert(
        {"email": current_user, "results": json.dumps(body.results)}
    ).execute()

    print(f"Results saved for {current_user}")
    return {"status": "ok"}


# -----------------------------------
# GET ANALYSIS RESULTS
# -----------------------------------
# Called after a redirect to reload previously saved results.
@app.get("/get-results")
async def get_results(current_user: str = Depends(get_current_user)):
    result = (
        supabase.table("analysis_results")
        .select("results")
        .eq("email", current_user)
        .execute()
    )

    if result.data:
        return {"results": json.loads(result.data[0]["results"])}

    return {"results": None}


# -----------------------------------
# RAZORPAY WEBHOOK
# -----------------------------------
@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    print(f"Webhook received: {body.get('event')}")

    if body.get("event") == "payment.captured":
        payment = body["payload"]["payment"]["entity"]
        email = payment.get("notes", {}).get("email")
        print(f"Webhook email: {email}")

        if not email:
            print("No email in notes, skipping")
            return {"status": "error", "reason": "missing email"}

        supabase.table("payments").insert(
            {"email": email, "status": "success"}
        ).execute()

        print(f"Payment recorded for {email}")

    return {"status": "ok"}


# -----------------------------------
# DEBUG (remove before going live)
# -----------------------------------
@app.get("/debug-payments")
def debug_payments():
    result = supabase.table("payments").select("*").execute()
    return {"data": result.data}


from fastapi.responses import HTMLResponse


@app.get("/payment-success", response_class=HTMLResponse)
async def payment_success():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Successful</title>
        <style>
            body {
                font-family: sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background: #0e1117;
                color: white;
            }
            .checkmark { font-size: 64px; margin-bottom: 16px; }
            .countdown { font-size: 18px; color: #888; margin-top: 12px; }
        </style>
    </head>
    <body>
        <div class="checkmark">✅</div>
        <h2>Payment Successful!</h2>
        <p>You can now go back to the analyzer tab.</p>
        <p class="countdown">This tab will close in <span id="count">3</span> seconds...</p>
        <script>
            let count = 3;
            const el = document.getElementById('count');
            const timer = setInterval(() => {
                count--;
                el.textContent = count;
                if (count <= 0) {
                    clearInterval(timer);
                    window.close();
                }
            }, 1000);
        </script>
    </body>
    </html>
    """

@app.post("/generate-insights")
async def generate_insights(
    body: InsightsRequest, current_user: str = Depends(get_current_user)
):
    """
    Calls HuggingFace Inference API (meta-llama/Meta-Llama-3-8B-Instruct)
    to generate personalised resume improvement advice.
    """

    prompt = f"""<s>[INST]
    You are an expert ATS resume coach. Analyse the following resume match data and give concise, actionable advice.
    
    ATS Score: {body.final_score}%
    Experience Alignment: {round(body.experience_alignment * 100)}%
    
    Matched Skills: {", ".join(body.matched_skills[:15]) or "None"}
    Missing Skills: {", ".join(body.missing_skills[:15]) or "None"}
    JD Required Skills: {", ".join(body.jd_skills[:15]) or "None"}
    
    Write a structured report with these exact sections:
    1. **Overall Assessment** — 2 sentences on the match quality
    2. **Top Skills to Add** — 3-5 specific missing skills with one-line explanation each
    3. **JD Highlights** — 3 key things the employer is looking for
    4. **Resume Improvements** — 3 actionable tips to improve ATS score
    5. **Quick Wins** — 2 things the candidate can do immediately
    
    Be specific, direct and concise. No generic advice.
    [/INST]"""

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": HF_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0,
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            res = await client.post(HF_URL, json=payload, headers=headers)

        if res.status_code == 200:
            data = res.json()

            # ✅ NEW FORMAT (chat completions)
            text = data["choices"][0]["message"]["content"]

            return {"insights": text.strip()}

        elif res.status_code == 503:
            return {
                "insights": "Model is loading. Please wait 20 seconds and try again."
            }

        else:
            raise HTTPException(status_code=500, detail=f"HF API error: {res.text}")

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="HuggingFace API timed out")
