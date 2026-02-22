# from app.parsing.document_parser import DocumentParser
# from app.parsing.section_segmenter import SectionSegmenter
# from app.extraction.dynamic_skill_extractor import DynamicSkillExtractor
# from app.extraction.experience_extractor import ExperienceExtractor
# from app.embeddings.embedding_model import EmbeddingModel
# from app.embeddings.similarity_engine import SimilarityEngine
# from app.scoring.section_scorer import SectionScorer
# from app.scoring.weighted_scorer import WeightedScorer
# from app.extraction.skill_normalizer import SkillNormalizer
# from app.scoring.weighted_skill_matcher import WeightedSkillMatcher
# from app.reporting.explanation_generator import ExplanationGenerator

# def run_pipeline(resume_input: str, jd_input: str):
#     """
#     Accepts:
#     - resume_input: file path (.pdf, .docx, .txt) or raw text
#     - jd_input: file path (.pdf, .docx, .txt) or raw text
#     """

#     # Initialize components
#     parser = DocumentParser()
#     segmenter = SectionSegmenter()
#     skill_extractor = DynamicSkillExtractor()
#     exp_extractor = ExperienceExtractor()
#     embedder = EmbeddingModel()
#     similarity_engine = SimilarityEngine()
#     normalizer = SkillNormalizer()
#     weighted_matcher = WeightedSkillMatcher()
#     explainer = ExplanationGenerator()

#     # Extract text (supports file path or raw text)
#     resume_text = parser.extract_text(resume_input)
#     jd_text = parser.extract_text(jd_input)

#     # Section segmentation
#     resume_sections = segmenter.segment(resume_text)
#     jd_sections = segmenter.segment(jd_text)

#     # # Dynamic skill extraction
#     # resume_skills = skill_extractor.extract(resume_text)
#     # jd_skills = skill_extractor.extract(jd_text)
#     resume_skills_raw = skill_extractor.extract(resume_text)
#     jd_skills_raw = skill_extractor.extract(jd_text)

#     resume_skills = normalizer.normalize(resume_skills_raw)
#     jd_skills = normalizer.normalize(jd_skills_raw)

#     resume_skills = normalizer.expand_with_synonyms(resume_skills)
#     jd_skills = normalizer.expand_with_synonyms(jd_skills)

#     # Experience extraction
#     resume_years = exp_extractor.extract_years(resume_text)
#     jd_years = exp_extractor.extract_years(jd_text)

#     # Skill matching + missing detection
#     skill_score, missing_skills = weighted_matcher.calculate(
#         resume_skills,
#         jd_sections,
#         skill_extractor,
#         normalizer
#     )

#     # Experience alignment
#     exp_score = SectionScorer.experience_match(
#         resume_years,
#         jd_years
#     )

#     # # Section-aware semantic scoring
#     # resume_exp_section = resume_sections.get("experience", resume_text)
#     # jd_req_section = jd_sections.get("requirements", jd_text)

#     # embeddings = embedder.encode([resume_exp_section, jd_req_section])
#     # semantic_score = similarity_engine.compute(
#     #     embeddings[0],
#     #     embeddings[1]
#     # )
#     semantic_pairs = []

#     if "experience" in resume_sections and "requirements" in jd_sections:
#         semantic_pairs.append(
#             (resume_sections["experience"], jd_sections["requirements"])
#         )

#     if "skills" in resume_sections and "technical_skills" in jd_sections:
#         semantic_pairs.append(
#             (resume_sections["skills"], jd_sections["technical_skills"])
#         )

#     scores = []

#     for r, j in semantic_pairs:
#         emb = embedder.encode([r, j])
#         score = similarity_engine.compute(emb[0], emb[1])
#         scores.append(score)

#     semantic_score = sum(scores) / len(scores) if scores else 0

#     # Final weighted score
#     final_score = WeightedScorer.compute(
#         exp_score,
#         skill_score,
#         semantic_score
#     )

#     confidence = min(
#         1.0,
#         (len(resume_skills) / 30)
#     )

#     # Structured report
#     report = {
#         "experience_alignment": round(exp_score * 100, 2),
#         "skill_coverage": round(skill_score * 100, 2),
#         "semantic_fit": round(semantic_score * 100, 2),
#         "final_score": final_score,
#         "resume_years_detected": resume_years,
#         "jd_years_required": jd_years,
#         "missing_skills": missing_skills,
#         "resume_skills_detected": resume_skills,
#         "jd_skills_detected": jd_skills
#     }
#     # explanation = explainer.generate(report)
#     # report["explanation"] = explanation
#     report["explanation"] = explainer.generate(report)

#     return {
#         "final_score": report["final_score"],
#         "experience_alignment": report["experience_alignment"],
#         "skill_coverage": report["skill_coverage"],
#         "semantic_fit": report["semantic_fit"],
#         "top_missing_skills": report["missing_skills"][:10],
#         "confidence": round(confidence * 100, 2),
#         "explanation": report["explanation"]
#     }

from app.parsing.document_parser import DocumentParser
from app.parsing.section_segmenter import SectionSegmenter
from app.extraction.dynamic_skill_extractor import DynamicSkillExtractor
from app.extraction.experience_extractor import ExperienceExtractor
from app.embeddings.embedding_model import EmbeddingModel
from app.embeddings.similarity_engine import SimilarityEngine
from app.scoring.section_scorer import SectionScorer
from app.scoring.weighted_scorer import WeightedScorer
from app.extraction.skill_normalizer import SkillNormalizer
from app.scoring.weighted_skill_matcher import WeightedSkillMatcher
from app.reporting.explanation_generator import ExplanationGenerator


def run_pipeline(resume_input: str, jd_input: str):

    parser = DocumentParser()
    segmenter = SectionSegmenter()
    skill_extractor = DynamicSkillExtractor()
    exp_extractor = ExperienceExtractor()
    embedder = EmbeddingModel()
    similarity_engine = SimilarityEngine()
    normalizer = SkillNormalizer()
    weighted_matcher = WeightedSkillMatcher()
    explainer = ExplanationGenerator()

    # Extract text
    resume_text = parser.extract_text(resume_input)
    jd_text = parser.extract_text(jd_input)

    # Segment sections
    resume_sections = segmenter.segment(resume_text)
    jd_sections = segmenter.segment(jd_text)

    # Skill extraction + normalization
    resume_skills_raw = skill_extractor.extract(resume_text)
    jd_skills_raw = skill_extractor.extract(jd_text)

    resume_skills = normalizer.expand_with_synonyms(
        normalizer.normalize(resume_skills_raw)
    )

    jd_skills = normalizer.expand_with_synonyms(
        normalizer.normalize(jd_skills_raw)
    )

    # Experience extraction
    resume_years = exp_extractor.extract_years(resume_text)
    jd_years = exp_extractor.extract_years(jd_text)

    # Weighted skill matching
    skill_score, missing_skills = weighted_matcher.calculate(
        resume_skills,
        jd_sections,
        skill_extractor,
        normalizer
    )

    # Experience alignment
    exp_score = SectionScorer.experience_match(
        resume_years,
        jd_years
    )

    # Section-aware semantic scoring
    semantic_pairs = []

    if "experience" in resume_sections and "requirements" in jd_sections:
        semantic_pairs.append(
            (resume_sections["experience"], jd_sections["requirements"])
        )

    if "skills" in resume_sections and "technical_skills" in jd_sections:
        semantic_pairs.append(
            (resume_sections["skills"], jd_sections["technical_skills"])
        )

    scores = []

    for r, j in semantic_pairs:
        emb = embedder.encode([r, j])
        score = similarity_engine.compute(emb[0], emb[1])
        scores.append(score)

    semantic_score = sum(scores) / len(scores) if scores else 0

    # Final weighted score
    final_score = WeightedScorer.compute(
        exp_score,
        skill_score,
        semantic_score
    )

    confidence = min(1.0, len(resume_skills) / 30)

    report = {
        "final_score": final_score,
        "experience_alignment": round(exp_score * 100, 2),
        "skill_coverage": round(skill_score * 100, 2),
        "semantic_fit": round(semantic_score * 100, 2),
        "resume_years_detected": resume_years,
        "jd_years_required": jd_years,
        "missing_skills": missing_skills,
        "resume_skills_detected": resume_skills,
        "jd_skills_detected": jd_skills,
        "confidence": round(confidence * 100, 2)
    }

    report["explanation"] = explainer.generate(report)

    return report