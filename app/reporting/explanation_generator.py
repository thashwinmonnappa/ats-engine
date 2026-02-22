class ExplanationGenerator:

    def generate(self, report):

        explanation = {}

        if report["experience_alignment"] < 80:
            explanation["experience_gap"] = (
                f"Candidate has {report['resume_years_detected']} years "
                f"while JD requires {report['jd_years_required']} years."
            )
        else:
            explanation["experience_gap"] = "Experience meets requirement."

        explanation["verdict"] = self._verdict_logic(report["final_score"])

        return explanation

    def _verdict_logic(self, score):

        if score >= 75:
            return "Strong Match — Recommended for Interview"
        elif score >= 60:
            return "Moderate Match — Review Recommended"
        elif score >= 45:
            return "Partial Match — Consider for Screening"
        else:
            return "Low Match — Not Recommended"