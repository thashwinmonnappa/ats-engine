import re


class SkillNormalizer:
    """
    Multi-domain Skill Normalizer.
    Covers DS/ML, SWE, DevOps, Product, Finance, Marketing.
    """

    def __init__(self):

        self.canonical_map = {
            # AI / ML
            "hugging face": "huggingface",
            "huggingface transformers": "huggingface",
            "llm-based": "llm",
            "gen ai": "generative ai",
            "genai": "generative ai",
            "ml": "machine learning",
            "ai": "artificial intelligence",
            "deep-learning": "deep learning",
            "dl": "deep learning",
            "cv": "computer vision",
            "nlp": "natural language processing",
            "rag": "retrieval augmented generation",
            "fine-tuning": "fine tuning",
            "llms": "llm",

            # Cloud
            "pyspark": "spark",
            "aws cloud": "aws",
            "google cloud": "gcp",
            "gcp cloud": "gcp",
            "azure cloud": "azure",
            "amazon web services": "aws",
            "microsoft azure": "azure",

            # Engineering
            "node": "node.js",
            "nodejs": "node.js",
            "reactjs": "react",
            "react.js": "react",
            "vuejs": "vue",
            "vue.js": "vue",
            "nextjs": "next.js",
            "ts": "typescript",
            "js": "javascript",
            "postgres": "postgresql",
            "mongo": "mongodb",
            "k8s": "kubernetes",
            "ci/cd pipelines": "ci/cd",
            "restful api": "rest api",
            "restful apis": "rest api",
            "rest apis": "rest api",
            "golang": "go",

            # Data
            "power bi": "powerbi",
            "ms excel": "excel",
            "microsoft excel": "excel",
            "statistical modeling": "statistical analysis",
            "stats": "statistical analysis",

            # Product
            "product mgmt": "product management",
            "pm": "product management",
            "ux": "user experience",
            "ui": "user interface",
            "gtm": "go to market",
            "a/b test": "a/b testing",

            # Finance
            "fin modeling": "financial modeling",
            "quant": "quantitative finance",

            # Marketing
            "paid social": "social media marketing",
            "paid search": "sem",
            "seo/sem": "seo",
            "ga": "google analytics",
            "ga4": "google analytics",
        }

        self.synonym_groups = {
            # AI / ML
            "generative ai": ["llm", "rag", "large language model", "chatgpt", "gpt"],
            "machine learning": ["ml", "predictive modeling", "statistical modeling"],
            "deep learning": ["neural networks", "pytorch", "tensorflow", "keras"],
            "natural language processing": ["nlp", "text mining", "text analytics"],
            "computer vision": ["image processing", "object detection", "image recognition"],
            "huggingface": ["transformers", "bert", "gpt"],

            # Cloud
            "cloud": ["aws", "azure", "gcp"],
            "aws": ["amazon web services", "ec2", "s3", "lambda"],
            "azure": ["microsoft azure", "azure devops"],
            "gcp": ["google cloud", "bigquery", "vertex ai"],

            # Data
            "spark": ["pyspark", "apache spark"],
            "sql": ["postgresql", "mysql", "sqlite", "oracle"],
            "data visualization": ["tableau", "power bi", "looker", "plotly"],

            # DevOps
            "devops": ["ci/cd", "docker", "kubernetes", "terraform"],
            "kubernetes": ["k8s", "helm", "container orchestration"],

            # Engineering
            "backend engineering": ["python", "java", "go", "rest api", "microservices"],
            "frontend engineering": ["react", "angular", "vue", "javascript", "typescript"],

            # Product
            "product management": ["product strategy", "roadmap", "backlog management"],
            "agile": ["scrum", "kanban", "sprint planning"],

            # Finance
            "financial modeling": ["dcf", "lbo", "valuation", "excel"],
            "risk management": ["credit risk", "market risk", "compliance"],

            # Marketing
            "digital marketing": ["seo", "sem", "content marketing", "email marketing"],
            "crm": ["salesforce", "hubspot", "marketo"],
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
