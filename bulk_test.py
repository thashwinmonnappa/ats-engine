from app.bulk_ranker import BulkRanker

if __name__ == "__main__":

    ranker = BulkRanker()

    ranked = ranker.rank_resumes(
        resume_folder="resumes/",
        jd_input="jd.pdf"
    )

    print("\n=== Ranked Candidates ===\n")

    for r in ranked:
        print(f"{r['resume_file']} → {r['final_score']}")