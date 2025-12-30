
import fitz  # PyMuPDF
import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class TextBlock:
    """Represents a text block with its properties"""
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    font_name: str
    font_size: float
    color: tuple
    page_num: int

    def to_dict(self):
        return asdict(self)

    @property
    def bbox(self):
        return (self.x0, self.y0, self.x1, self.y1)

    @property
    def width(self):
        return self.x1 - self.x0

    @property
    def height(self):
        return self.y1 - self.y0

@dataclass
class Section:
    """Represents a resume section"""
    name: str
    start_block: TextBlock
    content_blocks: List[TextBlock]
    page_num: int
    y_start: float
    y_end: float
    x_start: float
    x_end: float

class PDFResumeAnalyzer:
    """Analyzes PDF resume structure and extracts sections"""

    # Common section headers in resumes
    SECTION_KEYWORDS = [
        'experience', 'work experience', 'professional experience',
        'education', 'academic background',
        'skills', 'technical skills', 'core competencies',
        'certifications', 'certificates', 'licenses',
        'projects', 'personal projects',
        'achievements', 'accomplishments',
        'summary', 'profile', 'objective'
    ]

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.text_blocks: List[TextBlock] = []
        self.sections: Dict[str, Section] = {}

    def extract_text_blocks(self) -> List[TextBlock]:
        """Extract all text blocks with their properties"""
        all_blocks = []

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]

            # Get text blocks with detailed information
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if block.get("type") == 0:  # Text block
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            text_block = TextBlock(
                                text=span["text"].strip(),
                                x0=span["bbox"][0],
                                y0=span["bbox"][1],
                                x1=span["bbox"][2],
                                y1=span["bbox"][3],
                                font_name=span["font"],
                                font_size=span["size"],
                                color=span.get("color", 0),
                                page_num=page_num
                            )
                            if text_block.text:
                                all_blocks.append(text_block)

        self.text_blocks = all_blocks
        return all_blocks

    def identify_sections(self) -> Dict[str, Section]:
        """Identify resume sections based on headers"""
        if not self.text_blocks:
            self.extract_text_blocks()

        sections = {}
        current_section = None
        section_blocks = []

        for i, block in enumerate(self.text_blocks):
            text_lower = block.text.lower().strip()

            # Check if this is a section header
            is_section_header = False
            section_name = None

            for keyword in self.SECTION_KEYWORDS:
                if keyword in text_lower:
                    # Check if it's likely a header (larger font or bold)
                    avg_font_size = sum(b.font_size for b in self.text_blocks) / len(self.text_blocks)
                    if block.font_size >= avg_font_size * 0.9:
                        is_section_header = True
                        section_name = keyword.title()
                        break

            if is_section_header:
                # Save previous section
                if current_section and section_blocks:
                    sections[current_section] = self._create_section(
                        current_section, section_blocks
                    )

                # Start new section
                current_section = section_name
                section_blocks = [block]
            elif current_section:
                section_blocks.append(block)

        # Save last section
        if current_section and section_blocks:
            sections[current_section] = self._create_section(
                current_section, section_blocks
            )

        self.sections = sections
        return sections

    def _create_section(self, name: str, blocks: List[TextBlock]) -> Section:
        """Create a Section object from blocks"""
        if not blocks:
            return None

        return Section(
            name=name,
            start_block=blocks[0],
            content_blocks=blocks[1:],
            page_num=blocks[0].page_num,
            y_start=min(b.y0 for b in blocks),
            y_end=max(b.y1 for b in blocks),
            x_start=min(b.x0 for b in blocks),
            x_end=max(b.x1 for b in blocks)
        )

    def get_layout_info(self) -> Dict:
        """Get comprehensive layout information"""
        if not self.text_blocks:
            self.extract_text_blocks()

        font_sizes = [b.font_size for b in self.text_blocks]
        fonts = list(set(b.font_name for b in self.text_blocks))

        return {
            'total_pages': len(self.doc),
            'total_blocks': len(self.text_blocks),
            'unique_fonts': fonts,
            'avg_font_size': sum(font_sizes) / len(font_sizes) if font_sizes else 0,
            'min_font_size': min(font_sizes) if font_sizes else 0,
            'max_font_size': max(font_sizes) if font_sizes else 0,
            'sections_found': list(self.sections.keys()) if self.sections else []
        }

    def close(self):
        """Close the PDF document"""
        self.doc.close()
