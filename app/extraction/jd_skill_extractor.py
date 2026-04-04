import re


# -------------------------------------------------------------------
# Master skill whitelist — shared with DynamicSkillExtractor.
# Any candidate extracted from the JD must match one of these
# (or be a substring match) to be accepted.
# -------------------------------------------------------------------
KNOWN_SKILLS = {
    # DS / ML / AI
    "python", "r", "julia", "sql", "nosql",
    "machine learning", "deep learning", "reinforcement learning",
    "supervised learning", "unsupervised learning",
    "nlp", "natural language processing", "computer vision",
    "llm", "large language model", "generative ai", "gen ai",
    "pytorch", "tensorflow", "keras", "jax",
    "scikit-learn", "xgboost", "lightgbm", "catboost",
    "statsmodels", "scipy", "statistics", "mathematics",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "huggingface", "transformers", "bert", "gpt",
    "langchain", "semantic kernel", "llamaindex",
    "openai", "anthropic", "vertex ai", "bedrock", "sagemaker",
    "rag", "retrieval augmented generation",
    "vector database", "pinecone", "weaviate", "chroma",
    "mlflow", "wandb", "feature engineering",
    "model deployment", "model monitoring",
    "a/b testing", "hypothesis testing", "statistical analysis",
    "time series", "forecasting", "anomaly detection",
    "recommendation systems", "fine tuning",

    # Data Engineering
    "spark", "pyspark", "airflow", "kafka", "etl", "dbt",
    "hadoop", "hive", "flink",
    "snowflake", "bigquery", "redshift", "databricks",
    "data pipeline", "data warehouse", "data lake",
    "data processing", "data cleaning", "data wrangling",
    "data analysis", "data analytics", "data science",
    "data visualization",

    # Cloud
    "aws", "azure", "gcp", "google cloud",
    "lambda", "ec2", "s3", "cloud functions", "serverless",
    "cloud platforms", "cloud infrastructure",

    # Software Engineering
    "java", "c++", "c#", "c", "go", "golang", "rust", "scala",
    "javascript", "typescript", "node.js", "nodejs",
    "react", "angular", "vue", "next.js", "svelte",
    "html", "css", "sass", "tailwind",
    "django", "flask", "fastapi", "spring boot", "express",
    "graphql", "rest api", "grpc", "websockets",
    "microservices", "system design", "distributed systems",
    "unit testing", "integration testing", "tdd",
    "postgresql", "mysql", "sqlite", "mongodb", "redis",
    "elasticsearch", "cassandra", "rabbitmq",
    "git", "github", "gitlab",
    "agile", "scrum", "kanban", "jira",
    "object oriented programming", "functional programming",
    "design patterns", "solid principles",

    # DevOps
    "docker", "kubernetes", "helm", "terraform", "ansible",
    "ci/cd", "jenkins", "github actions", "circleci",
    "linux", "bash", "shell scripting",
    "monitoring", "grafana", "prometheus", "datadog",
    "networking", "security", "devsecops", "sre",

    # Product
    "product management", "product strategy", "product roadmap",
    "user research", "ux research", "wireframing", "figma",
    "okrs", "kpis", "metrics", "go to market",
    "backlog management", "sprint planning",
    "mixpanel", "amplitude", "product analytics",
    "competitive analysis", "stakeholder management",

    # Finance
    "financial modeling", "financial analysis", "valuation",
    "dcf", "lbo", "equity research", "risk management",
    "credit risk", "portfolio management",
    "bloomberg", "capital iq", "excel", "vba",
    "accounting", "ifrs", "gaap", "audit", "compliance",
    "quantitative finance", "algorithmic trading",

    # Marketing
    "digital marketing", "seo", "sem", "google ads",
    "content marketing", "email marketing",
    "social media marketing", "google analytics",
    "crm", "salesforce", "hubspot", "marketo",
    "conversion rate optimization", "lead generation",
    "brand management", "marketing automation",

    # General
    "leadership", "communication", "problem solving",
    "project management", "program management",
    "microsoft office", "powerpoint", "tableau", "power bi",
    "business analysis", "critical thinking",
    "collaboration", "mentoring", "presentation",
}


class JDSkillExtractor:
    """
    JD Skill Extractor — whitelist-validated approach.

    1. Extracts candidate phrases from JD text using section headers
       and bullet point parsing.
    2. Validates each candidate against KNOWN_SKILLS whitelist.
    3. Falls back to full-text keyword scan if section parsing yields nothing.

    This ensures only real skills appear in the output — no sentences,
    no connector phrases, no garbled text.
    """

    def __init__(self):
        self.section_headers = [
            r"skills?\s*required",
            r"required\s*skills?",
            r"technical\s*skills?",
            r"key\s*skills?",
            r"core\s*skills?",
            r"must.have\s*skills?",
            r"requirements?",
            r"qualifications?",
            r"what\s*you.ll\s*(need|bring|have)",
            r"what\s*we.re\s*looking\s*for",
            r"you\s*should\s*have",
            r"you\s*will\s*have",
            r"proficiency\s*in",
        ]

    def _clean(self, text: str) -> str:
        """Strip unicode garbage and normalize whitespace."""
        text = re.sub(r"[^\x00-\x7F]+", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _validate(self, candidate: str) -> list:
        """
        Check candidate against KNOWN_SKILLS.
        Returns list of matched skills found within the candidate string.
        A single candidate line may contain multiple skills (e.g. "Python and SQL").
        """
        candidate = candidate.lower().strip()
        found = []
        for skill in KNOWN_SKILLS:
            # Word-boundary match — avoid partial matches like "r" in "requirements"
            if re.search(r"\b" + re.escape(skill) + r"\b", candidate):
                found.append(skill)
        return found

    def extract(self, jd_text: str) -> list:
        jd_text = self._clean(jd_text)
        skills = set()

        section_pattern = "(" + "|".join(self.section_headers) + ")"
        section_regex = re.compile(section_pattern, re.IGNORECASE)

        # --------------------------------
        # Strategy 1: Section-based parsing
        # --------------------------------
        section_hits = list(section_regex.finditer(jd_text))

        for match in section_hits:
            start = match.end()
            block = jd_text[start:start + 1000]
            lines = block.split("\n")

            for line in lines:
                if section_regex.search(line) and line != lines[0]:
                    break

                # Strip bullet characters
                line = re.sub(r"^[\s\-\•\*\–\>\·]+", "", line).strip()

                # Split on commas — one line may list multiple skills
                parts = [line] if "," not in line else [p.strip() for p in line.split(",")]

                for part in parts:
                    matched = self._validate(part)
                    skills.update(matched)

        # --------------------------------
        # Strategy 2: Full-text keyword scan (always runs as safety net)
        # --------------------------------
        for skill in KNOWN_SKILLS:
            if re.search(r"\b" + re.escape(skill) + r"\b", jd_text.lower()):
                skills.add(skill)

        return sorted(list(skills))
