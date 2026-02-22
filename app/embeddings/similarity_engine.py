from sklearn.metrics.pairwise import cosine_similarity

class SimilarityEngine:

    @staticmethod
    def compute(vec1, vec2) -> float:
        return float(cosine_similarity([vec1], [vec2])[0][0])