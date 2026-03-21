from ranking.resume_loader import ResumeLoader
from ranking.candidate_ranker import CandidateRanker

class RankingEngine:

    def __init__(self, pipeline):

        self.loader = ResumeLoader()
        self.ranker = CandidateRanker(pipeline)

    def run_ranking(self, resume_folder, jd_text):

        resumes = self.loader.load_resumes(resume_folder)

        ranked_candidates = self.ranker.rank_candidates(resumes, jd_text)

        return ranked_candidates