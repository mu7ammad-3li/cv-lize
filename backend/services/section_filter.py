"""
Service to filter resume sections based on user selection
"""

import re
from typing import List, Set


class SectionFilter:
    """Filter resume sections dynamically"""

    @staticmethod
    def filter_markdown_sections(markdown: str, included_sections: Set[str]) -> str:
        """
        Filter markdown content to only include selected sections

        Args:
            markdown: Full markdown resume
            included_sections: Set of section names to include

        Returns:
            Filtered markdown with only included sections
        """
        if not included_sections:
            return markdown

        lines = markdown.split("\n")
        filtered_lines = []
        current_section = None
        include_current = True
        header_lines = []

        # First, capture the header (name and contact info)
        in_header = True

        for line in lines:
            # Check if it's a section header (## Section Name)
            section_match = re.match(r"^##\s+(.+)$", line)

            if section_match:
                in_header = False
                section_name = section_match.group(1).strip()
                current_section = section_name

                # Check if this section should be included
                # Match flexibly (e.g., "Technical Skills" matches "Skills")
                include_current = any(
                    included.lower() in section_name.lower()
                    or section_name.lower() in included.lower()
                    for included in included_sections
                )

                if include_current:
                    filtered_lines.append(line)
            elif in_header:
                # Always include header content (name, contact, etc.)
                header_lines.append(line)
            elif include_current and current_section:
                # Include content of current section
                filtered_lines.append(line)

        # Combine header and filtered sections
        result = "\n".join(header_lines + filtered_lines)

        # Clean up extra blank lines
        result = re.sub(r"\n{3,}", "\n\n", result)

        return result.strip()

    @staticmethod
    def get_section_names(markdown: str) -> List[str]:
        """Extract all section names from markdown"""
        sections = []
        for line in markdown.split("\n"):
            match = re.match(r"^##\s+(.+)$", line)
            if match:
                sections.append(match.group(1).strip())
        return sections


# Create singleton
section_filter = SectionFilter()
