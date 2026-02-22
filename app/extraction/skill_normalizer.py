import re


class SkillNormalizer:
    """
    Controlled Technical Skill Normalizer
    No external WordNet expansion.
    Deterministic and B2B-safe.
    """

    def __init__(self):

        self.canonical_map = {
            "hugging face": "huggingface",
            "huggingface transformers": "huggingface",
            "llm-based": "llm",
            "gen ai": "generative ai",
            "ml": "machine learning",
            "ai": "artificial intelligence",
            "deep-learning": "deep learning",
            "pyspark": "spark",
            "aws cloud": "aws",
            "google cloud": "gcp"
        }

        # Controlled synonym groups
        self.synonym_groups = {
            "generative ai": ["llm", "rag", "large language model"],
            "machine learning": ["ml", "predictive modeling"],
            "deep learning": ["neural networks", "pytorch", "tensorflow"],
            "cloud": ["aws", "azure", "gcp"],
            "huggingface": ["transformers"],
            "spark": ["pyspark"],
        }

    def normalize(self, skills: list) -> list:
        normalized = set()

        for skill in skills:
            skill = skill.lower().strip()
            skill = re.sub(r"\s+", " ", skill)

            if skill in self.canonical_map:
                skill = self.canonical_map[skill]

            normalized.add(skill)

        return list(normalized)

    def expand_with_synonyms(self, skills: list) -> list:
        expanded = set(skills)

        for skill in skills:
            for canonical, group in self.synonym_groups.items():
                if skill == canonical or skill in group:
                    expanded.add(canonical)
                    expanded.update(group)

        return list(expanded)