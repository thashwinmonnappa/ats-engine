class CandidateRanker:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def rank_candidates(self, resumes, jd_text):

        results = []

        for resume in resumes:

            score = self.pipeline.analyze(resume, jd_text)

            results.append({
                "resume": resume,
                "score": score
            })

        ranked = sorted(results, key=lambda x: x["score"], reverse=True)

        return ranked