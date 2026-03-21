import os

from app.parsing.resume_parser import ResumeParser
from app.extraction.dynamic_skill_extractor import DynamicSkillExtractor
from app.extraction.experience_extractor import ExperienceExtractor

from app.ontology.ontology_loader import OntologyLoader
from app.ontology.ontology_matcher import OntologyMatcher

from app.scoring.semantic_matcher import SemanticMatcher
from app.scoring.experience_matcher import ExperienceMatcher
from app.scoring.final_score_calculator import FinalScoreCalculator
from app.extraction.jd_skill_extractor import JDSkillExtractor

class ATSPipelineV2:

    """
    ATS Pipeline Version 2

    Flow:
    Resume File
        ↓
    Parse Resume
        ↓
    Extract Skills
        ↓
    Extract Experience
        ↓
    JD Parsing
        ↓
    Exact Skill Match
    Ontology Match
    Semantic Match
        ↓
    Experience Alignment
        ↓
    Final ATS Score
    """

    def __init__(self):

        # Parsers
        self.resume_parser = ResumeParser()

        # Extractors
        self.skill_extractor = DynamicSkillExtractor()
        self.experience_extractor = ExperienceExtractor()
        self.jd_skill_extractor = JDSkillExtractor()
        # Ontology
        ontology = OntologyLoader("app/ontology/skill_ontology.json").ontology
        self.ontology_matcher = OntologyMatcher(ontology)

        # Scoring modules
        self.semantic_matcher = SemanticMatcher()
        self.experience_matcher = ExperienceMatcher()
        self.final_score_calculator = FinalScoreCalculator()

    def normalize_skill(self,skill: str):
        return " ".join(skill.lower().replace("-", " ").split())


    def analyze(self, resume_path: str, jd_input: str):

        # -----------------------------
        # STEP 1: Parse Resume
        # -----------------------------
        resume_text = self.resume_parser.extract_text(resume_path)

        # -----------------------------
        # STEP 2: Extract Resume Skills
        # -----------------------------
        resume_skills = self.skill_extractor.extract(resume_text)
        resume_skills = set([self.normalize_skill(s) for s in resume_skills])

        # -----------------------------
        # STEP 3: Extract Resume Experience
        # -----------------------------
        resume_exp = self.experience_extractor.extract_years(resume_text)

        # -----------------------------
        # STEP 4: Handle JD Input
        # -----------------------------
        if os.path.exists(jd_input):
            jd_text = self.resume_parser.extract_text(jd_input)
        else:
            jd_text = jd_input

        # -----------------------------
        # STEP 5: Extract JD Skills
        # -----------------------------
        jd_skills = self.jd_skill_extractor.extract(jd_text)

        if not jd_skills:
            jd_skills = self.skill_extractor.extract(jd_text)

        jd_skills = set([self.normalize_skill(s) for s in jd_skills])

        # -----------------------------
        # STEP 6: Exact Match
        # -----------------------------
        exact_matches = resume_skills.intersection(jd_skills)
        exact_score = len(exact_matches) / max(len(jd_skills), 1)

        # -----------------------------
        # STEP 7: Ontology Matching
        # -----------------------------
        ontology_matches = self.ontology_matcher.match_skills(
            resume_skills,
            jd_skills
        )

        ontology_matches = set([self.normalize_skill(s) for s in ontology_matches])

        ontology_score = len(ontology_matches) / max(len(jd_skills), 1)

        ontology_display = [
            skill for skill in ontology_matches
            if skill not in exact_matches
        ]

        # -----------------------------
        # STEP 8: Skill Gap (FIXED)
        # -----------------------------
        matched_skills = exact_matches.union(ontology_matches)

        # Normalize again to be 100% safe
        matched_skills = set([self.normalize_skill(s) for s in matched_skills])
        jd_skills = set([self.normalize_skill(s) for s in jd_skills])

        missing_skills = jd_skills - matched_skills

        # -----------------------------
        # STEP 9: Semantic Matching (SAFE)
        # -----------------------------
        semantic_results = self.semantic_matcher.compute_similarity(
            list(resume_skills),
            list(jd_skills)
        )

        semantic_score = 0.0
        count = 0

        if isinstance(semantic_results, (list, set)):

            for r in semantic_results:

                if isinstance(r, dict) and "similarity" in r:
                    try:
                        semantic_score += float(r["similarity"])
                        count += 1
                    except:
                        continue

        if count > 0:
            semantic_score = semantic_score / count
        else:
            semantic_score = 0.0

        # -----------------------------
        # STEP 10: Experience Matching
        # -----------------------------
        jd_exp = self.experience_extractor.extract_years(jd_text)

        experience_score = self.experience_matcher.calculate_score(
            resume_exp,
            jd_exp
        )

        # -----------------------------
        # STEP 11: Final Score
        # -----------------------------
        skill_score = (exact_score + ontology_score) / 2

        final_score = self.final_score_calculator.compute_final_score({
            "skill_match": skill_score,
            "semantic": semantic_score,
            "experience": experience_score,
            "section": 1
        })

        # -----------------------------
        # STEP 12: Sort for UI
        # -----------------------------
        matched_skills = sorted(list(matched_skills))
        missing_skills = sorted(list(missing_skills))
        exact_matches = sorted(list(exact_matches))
        ontology_display = sorted(list(ontology_display))

        # -----------------------------
        # FINAL OUTPUT
        # -----------------------------
        return {

            "final_score": final_score,

            "resume_skills": list(resume_skills),
            "jd_skills": list(jd_skills),

            "matched_skills": matched_skills,
            "exact_matches": exact_matches,

            "ontology_matches": ontology_display,

            "missing_skills": missing_skills,

            "semantic_fit": semantic_score,
            "experience_alignment": experience_score
        }