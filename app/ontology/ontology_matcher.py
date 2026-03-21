class OntologyMatcher:

    def __init__(self, ontology):

        self.ontology = ontology

    def match_skills(self, resume_skills, jd_skills):

        matches = []

        for jd_skill in jd_skills:

            if jd_skill in resume_skills:
                matches.append(jd_skill)

            else:

                if jd_skill in self.ontology:

                    children = self.ontology[jd_skill]

                    for child in children:

                        if child in resume_skills:
                            matches.append(jd_skill)

        return matches