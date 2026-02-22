# import re
# import spacy

# class DynamicSkillExtractor:

#     def __init__(self):
#         self.nlp = spacy.load("en_core_web_sm")

#         # Common technical patterns
#         self.tech_pattern = re.compile(
#             r"\b([A-Z][a-zA-Z0-9\+\-\.#]*(?:\s[A-Z][a-zA-Z0-9\+\-\.#]*)*)\b"
#         )

#     def extract(self, text: str, top_k: int = 30) -> list:
#         doc = self.nlp(text)

#         skills = set()

#         # 1️⃣ Proper nouns & tech-like tokens
#         for token in doc:
#             if token.pos_ == "PROPN":
#                 skills.add(token.text.lower())

#         # 2️⃣ Capitalized multi-word tech terms
#         capitalized_phrases = self.tech_pattern.findall(text)
#         for phrase in capitalized_phrases:
#             if len(phrase.split()) <= 4:
#                 skills.add(phrase.lower())

#         # 3️⃣ Important noun chunks
#         for chunk in doc.noun_chunks:
#             if len(chunk.text.split()) <= 3 and len(chunk.text) > 3:
#                 skills.add(chunk.text.lower())

#         # Clean
#         cleaned = [
#             s.strip()
#             for s in skills
#             if len(s) > 2 and not s.isdigit()
#         ]

#         return list(set(cleaned))[:top_k]

import re

class DynamicSkillExtractor:
    """
    Hybrid Technical Skill Extractor
    Rule-based + pattern-based + noise filtering
    Designed for B2B ATS-grade screening
    """

    def __init__(self):

        # Common technical keywords to boost detection
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
            "git", "docker", "kubernetes"
        ]

        # Words we do NOT want
        self.stop_words = [
            "team", "development", "experience",
            "business", "requirements", "solutions",
            "role", "responsibilities", "degree",
            "skills", "strong", "build", "assist",
            "collaborate", "best practices",
            "our team", "insightful visualizations"
        ]

        # Regex patterns
        self.acronym_pattern = re.compile(r"\b[A-Z]{2,}\b")
        self.camel_case_pattern = re.compile(r"\b[A-Z][a-z]+[A-Z][A-Za-z]*\b")
        self.hyphen_pattern = re.compile(r"\b[a-zA-Z]+[-][a-zA-Z]+\b")

    def extract(self, text: str, top_k: int = 50) -> list:

        text_lower = text.lower()
        skills = set()

        # 1️⃣ Direct keyword matching (strong signal)
        for keyword in self.tech_keywords:
            if keyword in text_lower:
                skills.add(keyword)

        # 2️⃣ Acronyms like AWS, NLP, LLM
        acronyms = self.acronym_pattern.findall(text)
        for acro in acronyms:
            skills.add(acro.lower())

        # 3️⃣ CamelCase words like LangChain, PyTorch
        camel_words = self.camel_case_pattern.findall(text)
        for word in camel_words:
            skills.add(word.lower())

        # 4️⃣ Hyphenated tools like scikit-learn
        hyphen_words = self.hyphen_pattern.findall(text)
        for word in hyphen_words:
            skills.add(word.lower())

        # 5️⃣ Remove noise
        cleaned = []
        for skill in skills:
            if len(skill) < 2:
                continue
            if skill in self.stop_words:
                continue
            if skill.isdigit():
                continue
            cleaned.append(skill.strip())

        return list(set(cleaned))[:top_k]