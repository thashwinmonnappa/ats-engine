class ExplanationBuilder:

    @staticmethod
    def build(exp_score, skill_score, semantic_score, final_score):
        return {
            "experience_alignment": round(exp_score * 100, 2),
            "skill_coverage": round(skill_score * 100, 2),
            "semantic_fit": round(semantic_score * 100, 2),
            "final_score": final_score
        }