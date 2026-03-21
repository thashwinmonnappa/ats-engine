from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcher:
    """
    Computes semantic similarity between JD skills and Resume skills
    using SentenceTransformer embeddings.

    Optimized:
    - Batch encoding (fast)
    - Cosine similarity matrix (efficient)
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def compute_similarity(self, resume_skills, jd_skills):

        # -----------------------------
        # Safety checks
        # -----------------------------
        if not resume_skills or not jd_skills:
            return []

        # Convert to list (in case sets are passed)
        resume_skills = list(resume_skills)
        jd_skills = list(jd_skills)

        # -----------------------------
        # Step 1: Encode all skills at once (FAST)
        # -----------------------------
        resume_embeddings = self.model.encode(resume_skills)
        jd_embeddings = self.model.encode(jd_skills)

        # -----------------------------
        # Step 2: Compute similarity matrix
        # -----------------------------
        similarity_matrix = cosine_similarity(jd_embeddings, resume_embeddings)

        # -----------------------------
        # Step 3: Get best match per JD skill
        # -----------------------------
        results = []

        for i, jd_skill in enumerate(jd_skills):

            scores = similarity_matrix[i]

            best_score = float(max(scores))

            results.append({"skill": jd_skill, "similarity": best_score})

        return results
