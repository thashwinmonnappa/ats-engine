# import re

# class SectionSegmenter:

#     SECTION_HEADERS = [
#         "experience", "work experience", "professional experience",
#         "skills", "technical skills", "projects",
#         "education", "summary", "profile"
#     ]

#     def segment(self, text: str) -> dict:
#         sections = {}
#         lower_text = text.lower()

#         for header in self.SECTION_HEADERS:
#             pattern = rf"{header}(.*?)(?=\n[A-Z ]{{3,}}|$)"
#             match = re.search(pattern, lower_text, re.DOTALL)
#             if match:
#                 sections[header] = match.group(1).strip()

#         return sections

import re


class SectionSegmenter:

    SECTION_PATTERNS = {
        "experience": r"(experience.*?)(?=\n[A-Z][A-Z ]+\n|$)",
        "skills": r"(skills.*?)(?=\n[A-Z][A-Z ]+\n|$)",
        "education": r"(education.*?)(?=\n[A-Z][A-Z ]+\n|$)",
        "requirements": r"(required qualifications.*?)(?=\n[A-Z][A-Z ]+\n|$)",
        "technical_skills": r"(technical skills.*?)(?=\n[A-Z][A-Z ]+\n|$)",
        "responsibilities": r"(core responsibilities.*?)(?=\n[A-Z][A-Z ]+\n|$)"
    }

    def segment(self, text: str) -> dict:
        sections = {}
        lower_text = text.lower()

        for name, pattern in self.SECTION_PATTERNS.items():
            match = re.search(pattern, lower_text, re.DOTALL)
            if match:
                sections[name] = match.group(1)

        return sections