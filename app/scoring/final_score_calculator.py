class FinalScoreCalculator:

    def __init__(self):

        self.weights = {
            "skill_match": 0.35,
            "experience": 0.25,
            "semantic": 0.20,
            "section": 0.20
        }

    def compute_final_score(self, scores):

        final_score = (
            scores["skill_match"] * self.weights["skill_match"] +
            scores["experience"] * self.weights["experience"] +
            scores["semantic"] * self.weights["semantic"] +
            scores["section"] * self.weights["section"]
        )

        return round(final_score * 100, 2)