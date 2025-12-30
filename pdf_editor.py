
import fitz  # PyMuPDF
import copy
from typing import Dict, List, Tuple, Optional
from pdf_analyzer import PDFResumeAnalyzer, TextBlock, Section

class PDFResumeEditor:
    """Edit PDF resumes while preserving layout"""

    def __init__(self, input_pdf_path: str, output_pdf_path: str):
        self.input_path = input_pdf_path
        self.output_path = output_pdf_path
        self.doc = fitz.open(input_pdf_path)
        self.analyzer = PDFResumeAnalyzer(input_pdf_path)

        # Analyze the PDF structure
        self.analyzer.extract_text_blocks()
        self.analyzer.identify_sections()

    def add_experience(self, experience_lines: List[str], position: str = "top") -> bool:
        """
        Add experience entry to the Experience section

        Args:
            experience_lines: List of text lines to add (minimum 5)
            position: Where to add ("top" or "bottom" of experience section)

        Returns:
            bool: Success status
        """
        try:
            # Find Experience section
            experience_section = None
            for section_name, section in self.analyzer.sections.items():
                if 'experience' in section_name.lower():
                    experience_section = section
                    break

            if not experience_section:
                print("⚠️  Experience section not found")
                return False

            # Get the page and section details
            page = self.doc[experience_section.page_num]

            # Determine insertion point
            if position == "top":
                # Insert right after the section header
                insert_y = experience_section.start_block.y1 + 10
                reference_block = experience_section.start_block
            else:
                # Insert at the bottom
                insert_y = experience_section.y_end + 5
                reference_block = experience_section.content_blocks[-1] if experience_section.content_blocks else experience_section.start_block

            # Get font properties from existing content
            if experience_section.content_blocks:
                ref_block = experience_section.content_blocks[0]
            else:
                ref_block = experience_section.start_block

            font_size = ref_block.font_size
            font_name = self._get_standard_font(ref_block.font_name)
            x_position = experience_section.x_start

            # Calculate line spacing
            line_spacing = font_size * 1.2

            # Insert text maintaining layout
            current_y = insert_y
            for line in experience_lines:
                # Insert text at calculated position
                text_rect = fitz.Rect(
                    x_position,
                    current_y,
                    experience_section.x_end,
                    current_y + font_size + 5
                )

                page.insert_text(
                    point=(x_position, current_y + font_size),
                    text=line,
                    fontname=font_name,
                    fontsize=font_size,
                    color=(0, 0, 0)
                )

                current_y += line_spacing

            print(f"✅ Added {len(experience_lines)} lines to Experience section")
            return True

        except Exception as e:
            print(f"❌ Error adding experience: {str(e)}")
            return False

    def modify_skill(self, old_skill: str, new_skill: str) -> bool:
        """
        Modify a skill in the Skills section

        Args:
            old_skill: Skill text to find and replace
            new_skill: New skill text

        Returns:
            bool: Success status
        """
        try:
            # Find Skills section
            skills_section = None
            for section_name, section in self.analyzer.sections.items():
                if 'skill' in section_name.lower():
                    skills_section = section
                    break

            if not skills_section:
                print("⚠️  Skills section not found")
                return False

            page = self.doc[skills_section.page_num]

            # Find the skill to modify
            for block in skills_section.content_blocks:
                if old_skill.lower() in block.text.lower():
                    # Create a white rectangle to cover old text
                    cover_rect = fitz.Rect(block.bbox)
                    page.draw_rect(cover_rect, color=(1, 1, 1), fill=(1, 1, 1))

                    # Insert new text at same position
                    font_name = self._get_standard_font(block.font_name)
                    page.insert_text(
                        point=(block.x0, block.y0 + block.font_size),
                        text=block.text.replace(old_skill, new_skill),
                        fontname=font_name,
                        fontsize=block.font_size,
                        color=(0, 0, 0)
                    )

                    print(f"✅ Modified skill: '{old_skill}' → '{new_skill}'")
                    return True

            print(f"⚠️  Skill '{old_skill}' not found")
            return False

        except Exception as e:
            print(f"❌ Error modifying skill: {str(e)}")
            return False

    def add_certification(self, certification_text: str) -> bool:
        """
        Add a certification to the Certifications section

        Args:
            certification_text: Certification text to add

        Returns:
            bool: Success status
        """
        try:
            # Find Certifications section
            cert_section = None
            for section_name, section in self.analyzer.sections.items():
                if 'certif' in section_name.lower():
                    cert_section = section
                    break

            if not cert_section:
                print("⚠️  Certifications section not found, creating one...")
                return self._create_certification_section(certification_text)

            page = self.doc[cert_section.page_num]

            # Get font properties from existing certifications
            if cert_section.content_blocks:
                ref_block = cert_section.content_blocks[0]
            else:
                ref_block = cert_section.start_block

            font_size = ref_block.font_size
            font_name = self._get_standard_font(ref_block.font_name)

            # Insert at the end of certifications section
            insert_y = cert_section.y_end + (font_size * 1.2)
            x_position = cert_section.x_start

            # Add bullet point if other certs have them
            if any('•' in b.text or '●' in b.text for b in cert_section.content_blocks):
                certification_text = f"• {certification_text}"

            page.insert_text(
                point=(x_position, insert_y + font_size),
                text=certification_text,
                fontname=font_name,
                fontsize=font_size,
                color=(0, 0, 0)
            )

            print(f"✅ Added certification: '{certification_text}'")
            return True

        except Exception as e:
            print(f"❌ Error adding certification: {str(e)}")
            return False

    def _create_certification_section(self, certification_text: str) -> bool:
        """Create a new Certifications section if it doesn't exist"""
        try:
            # Find a good place to add it (usually after Skills or Education)
            target_section = None
            for section_name in ['Skills', 'Education', 'Projects']:
                for name, section in self.analyzer.sections.items():
                    if section_name.lower() in name.lower():
                        target_section = section
                        break
                if target_section:
                    break

            if not target_section:
                print("⚠️  Could not find suitable location for Certifications section")
                return False

            page = self.doc[target_section.page_num]

            # Insert section header
            insert_y = target_section.y_end + 20
            x_position = target_section.x_start

            header_font_size = target_section.start_block.font_size
            content_font_size = header_font_size * 0.85

            # Add header
            page.insert_text(
                point=(x_position, insert_y + header_font_size),
                text="CERTIFICATIONS",
                fontname="helv-bold",
                fontsize=header_font_size,
                color=(0, 0, 0)
            )

            # Add certification
            insert_y += header_font_size * 1.5
            page.insert_text(
                point=(x_position, insert_y + content_font_size),
                text=f"• {certification_text}",
                fontname="helv",
                fontsize=content_font_size,
                color=(0, 0, 0)
            )

            print(f"✅ Created Certifications section and added: '{certification_text}'")
            return True

        except Exception as e:
            print(f"❌ Error creating certification section: {str(e)}")
            return False

    def _get_standard_font(self, font_name: str) -> str:
        """Map extracted font to standard PDF font"""
        font_lower = font_name.lower()

        if 'bold' in font_lower:
            return "helv-bold"
        elif 'italic' in font_lower:
            return "helv-ital"
        elif 'times' in font_lower:
            return "times"
        else:
            return "helv"

    def save(self) -> bool:
        """Save the edited PDF"""
        try:
            self.doc.save(self.output_path, garbage=4, deflate=True)
            print(f"\n💾 Saved edited PDF to: {self.output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving PDF: {str(e)}")
            return False

    def close(self):
        """Close all resources"""
        self.doc.close()
        self.analyzer.close()
