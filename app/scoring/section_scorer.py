class SectionScorer:

    @staticmethod
    def skill_match(resume_skills: list, jd_skills: list):
        if not jd_skills:
            return 0.0, []

        resume_set = set(resume_skills)
        jd_set = set(jd_skills)

        matched = resume_set.intersection(jd_set)
        missing = jd_set - resume_set

        score = len(matched) / len(jd_set)

        return score, list(missing)

    @staticmethod
    def experience_match(resume_years: float, jd_years: float) -> float:
        if jd_years == 0:
            return 1.0
        return min(resume_years / jd_years, 1.0)