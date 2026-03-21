import re

class JDSkillExtractor:

    def extract(self, jd_text):

        jd_text = jd_text.lower()

        # simple pattern: bullet skills
        patterns = [
            r"skills?:([\s\S]*?)\n\n",
            r"requirements?:([\s\S]*?)\n\n"
        ]

        skills = []

        for pattern in patterns:

            match = re.search(pattern, jd_text)

            if match:

                block = match.group(1)

                lines = block.split("\n")

                for line in lines:

                    line = line.strip("-• ").strip()

                    if len(line) > 2 and len(line) < 40:
                        skills.append(line)

        return list(dict.fromkeys(skills))