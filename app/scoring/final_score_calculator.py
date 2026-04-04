class FinalScoreCalculator:
    """
    Computes the final ATS score from component scores.

    Weights:
    - skill_match  40% — exact + ontology skill overlap (most important)
    - semantic     30% — embedding similarity between resume and JD
    - experience   20% — years of experience alignment
    - section      10% — resume structure completeness
                         (currently passed as 1.0 by pipeline,
                          hook this up to a real section scorer later)

    All input scores should be in range [0, 1].
    Output is a percentage in range [0, 100].
    """

    def __init__(self):
        self.weights = {
            "skill_match": 0.40,
            "semantic":    0.30,
            "experience":  0.20,
            "section":     0.10,
        }

    def compute_final_score(self, scores: dict) -> float:
        """
        Args:
            scores: dict with keys skill_match, semantic, experience, section
                    all values should be floats in [0, 1]
        Returns:
            float: final score as a percentage [0, 100]
        """
        # Clamp all scores to [0, 1] to prevent runaway values
        clamped = {k: max(0.0, min(1.0, v)) for k, v in scores.items()}

        final = (
            clamped["skill_match"] * self.weights["skill_match"] +
            clamped["semantic"]    * self.weights["semantic"]    +
            clamped["experience"]  * self.weights["experience"]  +
            clamped["section"]     * self.weights["section"]
        )

        return round(final * 100, 2)
