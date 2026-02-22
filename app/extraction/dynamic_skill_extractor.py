import re


class DynamicSkillExtractor:
    """
    Cloud-safe Hybrid Technical Skill Extractor
    - No spaCy dependency
    - Deterministic
    - Regex + controlled vocabulary
    - Designed for deployment stability
    """

    def __init__(self):

        # Strong technical keywords
        self.tech_keywords = [
            "python", "sql", "r", "java", "c++",
            "machine learning", "deep learning",
            "nlp", "llm", "generative ai",
            "pytorch", "tensorflow",
            "scikit-learn", "statsmodels",
            "pandas", "numpy", "matplotlib", "seaborn",
            "huggingface", "transformers",
            "langchain", "semantic kernel",
            "openai", "vertex ai",
            "aws", "azure", "gcp",
            "pyspark", "spark",
            "mlflow", "rag",
            "git", "docker", "kubernetes",
            "rest api", "api"
        ]

        # Non-technical words to filter out
        self.stop_words = {
            "team", "development", "experience",
            "business", "requirements", "solutions",
            "role", "responsibilities", "degree",
            "skills", "strong", "build", "assist",
            "collaborate", "best practices",
            "our team", "insightful visualizations",
            "problem-solving", "cutting-edge"
        }

        # Patterns
        self.acronym_pattern = re.compile(r"\b[A-Z]{2,}\b")
        self.camel_case_pattern = re.compile(r"\b[A-Z][a-z]+[A-Z][A-Za-z]*\b")
        self.hyphen_pattern = re.compile(r"\b[a-zA-Z]+-[a-zA-Z]+\b")

    def extract(self, text: str, top_k: int = 50):

        text_lower = text.lower()
        skills = set()

        # 1️⃣ Direct keyword detection
        for keyword in self.tech_keywords:
            if keyword in text_lower:
                skills.add(keyword)

        # 2️⃣ Acronyms (AWS, NLP, LLM)
        for match in self.acronym_pattern.findall(text):
            skills.add(match.lower())

        # 3️⃣ CamelCase tools (LangChain, PyTorch)
        for match in self.camel_case_pattern.findall(text):
            skills.add(match.lower())

        # 4️⃣ Hyphenated tech (scikit-learn)
        for match in self.hyphen_pattern.findall(text):
            skills.add(match.lower())

        # 5️⃣ Clean + filter
        cleaned = []
        for skill in skills:
            skill = skill.strip().lower()

            if len(skill) < 2:
                continue
            if skill in self.stop_words:
                continue
            if skill.isdigit():
                continue
            if not re.search(r"[a-zA-Z]", skill):
                continue

            cleaned.append(skill)

        return list(set(cleaned))[:top_k]