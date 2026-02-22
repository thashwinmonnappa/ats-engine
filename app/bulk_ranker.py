import os
from app.main import run_pipeline


class BulkRanker:
    """
    Bulk Resume Ranking Engine

    - Iterates through a folder of resumes
    - Runs ATS scoring pipeline
    - Sorts candidates by final score
    - Returns ranked list
    """

    SUPPORTED_FORMATS = (".pdf", ".docx", ".txt")

    def rank_resumes(self, resume_folder: str, jd_input: str):

        if not os.path.exists(resume_folder):
            raise FileNotFoundError(f"Folder not found: {resume_folder}")

        results = []

        for file_name in os.listdir(resume_folder):

            if not file_name.lower().endswith(self.SUPPORTED_FORMATS):
                continue

            resume_path = os.path.join(resume_folder, file_name)

            try:
                report = run_pipeline(resume_path, jd_input)

                results.append({
                    "resume_file": file_name,
                    "final_score": report["final_score"],
                    "experience_alignment": report["experience_alignment"],
                    "skill_coverage": report["skill_coverage"],
                    "semantic_fit": report["semantic_fit"]
                })

            except Exception as e:
                results.append({
                    "resume_file": file_name,
                    "error": str(e)
                })

        # Sort by final_score (descending), ignore error entries
        ranked = sorted(
            [r for r in results if "final_score" in r],
            key=lambda x: x["final_score"],
            reverse=True
        )

        # Append failed files at bottom
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