import re

class ExperienceExtractor:

    YEAR_PATTERN = r"(\d+(\.\d+)?)\+?\s*(?:years|yrs)"
    RANGE_PATTERN = r"(\d+(\.\d+)?)\s*-\s*(\d+(\.\d+)?)\s*(?:years|yrs)"

    def extract_years(self, text: str) -> float:
        text = text.lower()

        # Match ranges like 3-5 years
        range_match = re.findall(self.RANGE_PATTERN, text)
        if range_match:
            values = []
            for match in range_match:
                low = float(match[0])
                high = float(match[2])
                values.append((low + high) / 2)
            return max(values)

        # Match normal patterns like 2.9 years, 4+ years
        matches = re.findall(self.YEAR_PATTERN, text)
        if matches:
            years = [float(m[0]) for m in matches]
            return max(years)

        return 0.0