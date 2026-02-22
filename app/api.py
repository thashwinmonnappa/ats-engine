from fastapi import FastAPI, UploadFile, File
from app.main import run_pipeline
from app.bulk_ranker import BulkRanker
import shutil
import os

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Resume Screening API Running"}


@app.post("/score")
async def score_resume(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):

    resume_path = f"temp_{resume.filename}"
    jd_path = f"temp_{jd.filename}"

    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(jd.file, buffer)

    report = run_pipeline(resume_path, jd_path)

    os.remove(resume_path)
    os.remove(jd_path)

    return report


@app.post("/bulk_rank")
async def bulk_rank(jd: UploadFile = File(...)):

    jd_path = f"temp_{jd.filename}"

    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(jd.file, buffer)

    ranker = BulkRanker()
    ranked = ranker.rank_resumes("resumes/", jd_path)

    os.remove(jd_path)

    return ranked