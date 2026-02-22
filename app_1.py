from app.main import run_pipeline

RESUME_PATH = r"C:\Users\ADMIN\Downloads\SIDE_HUSTLE(21.02.26)\resume_ats_engine_b2b\resumes\Thashwin Monnappa M M - Resume - Draft2.pdf"
JD_PATH = r"C:\Users\ADMIN\Downloads\SIDE_HUSTLE(21.02.26)\resume_ats_engine_b2b\JD\dentsu_JD.pdf"

report = run_pipeline(
    RESUME_PATH, JD_PATH
)
print(report)