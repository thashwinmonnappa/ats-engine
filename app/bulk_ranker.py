import os
from app.pipeline.ats_pipeline_v2 import ATSPipelineV2


class BulkRanker:

    SUPPORTED_FORMATS = (".pdf", ".docx", ".txt")

    def __init__(self):
        self.pipeline = ATSPipelineV2()

    def rank_resumes(self, resume_folder: str, jd_input: str):

        if not os.path.exists(resume_folder):
            raise FileNotFoundError(f"Folder not found: {resume_folder}")

        results = []

        for file_name in os.listdir(resume_folder):

            if not file_name.lower().endswith(self.SUPPORTED_FORMATS):
                continue

            resume_path = os.path.join(resume_folder, file_name)

            try:

                # Run Version-2 pipeline
                report = self.pipeline.analyze(resume_path, jd_input)

                results.append({
                    "resume_file": file_name,
                    "final_score": report["final_score"],
                    "experience_alignment": report["experience_alignment"],
                    "semantic_fit": report["semantic_fit"]
                })

            except Exception as e:

                results.append({
                    "resume_file": file_name,
                    "error": str(e)
                })

        ranked = sorted(
            [r for r in results if "final_score" in r],
            key=lambda x: x["final_score"],
            reverse=True
        )

        failed = [r for r in results if "error" in r]

        return ranked + failed

    def save_to_csv(self, ranked_results, filename="ranked_results.csv"):
        import csv

        if not ranked_results:
            return

        keys = ranked_results[0].keys()

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(ranked_results)

        return filename