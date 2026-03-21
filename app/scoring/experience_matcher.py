class ExperienceMatcher:

    def calculate_score(self, resume_years, jd_years):

        if jd_years == 0:
            return 1.0

        score = min(resume_years / jd_years, 1)

        return round(score, 2)