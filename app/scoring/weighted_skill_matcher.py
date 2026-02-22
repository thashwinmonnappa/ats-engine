class WeightedSkillMatcher:

    SECTION_WEIGHTS = {
        "requirements": 1.0,
        "technical_skills": 0.9,
        "responsibilities": 0.7
    }

    def calculate(self, resume_skills, jd_sections, skill_extractor, normalizer):

        total_weight = 0
        matched_weight = 0
        missing_skills = []

        for section, weight in self.SECTION_WEIGHTS.items():
            if section in jd_sections:

                raw_skills = skill_extractor.extract(jd_sections[section])
                skills = normalizer.normalize(raw_skills)
                skills = normalizer.expand_with_synonyms(skills)

                for skill in skills:
                    total_weight += weight

                    if skill in resume_skills:
                        matched_weight += weight
                    else:
                        missing_skills.append(skill)

        if total_weight == 0:
            return 0.0, []

        score = matched_weight / total_weight

        return score, list(set(missing_skills))