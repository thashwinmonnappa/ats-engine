from app.config.scoring_weights import (
    EXPERIENCE_WEIGHT,
    SKILL_WEIGHT,
    SEMANTIC_WEIGHT,
)

class WeightedScorer:

    @staticmethod
    def compute(exp_score: float, skill_score: float, semantic_score: float) -> float:
        final = (
            EXPERIENCE_WEIGHT * exp_score +
            SKILL_WEIGHT * skill_score +
            SEMANTIC_WEIGHT * semantic_score
        )
        return round(final * 100, 2)