
import sys
from pdf_analyzer import PDFResumeAnalyzer
import json

def test_pdf_analysis(pdf_path: str):
    """Test PDF analysis functionality"""
    print(f"\n{'='*60}")
    print(f"Analyzing: {pdf_path}")
    print('='*60)

    try:
        analyzer = PDFResumeAnalyzer(pdf_path)

        # Extract text blocks
        print("\n📄 Extracting text blocks...")
        blocks = analyzer.extract_text_blocks()
        print(f"✅ Found {len(blocks)} text blocks")

        # Show sample blocks
        print("\n📝 Sample Text Blocks (first 5):")
        for i, block in enumerate(blocks[:5]):
            print(f"{i+1}. '{block.text[:50]}...' | Font: {block.font_name} | Size: {block.font_size:.1f}")

        # Identify sections
        print("\n🔍 Identifying sections...")
        sections = analyzer.identify_sections()
        print(f"✅ Found {len(sections)} sections")

        for section_name, section in sections.items():
            print(f"  - {section_name}: {len(section.content_blocks)} blocks | Page {section.page_num}")

        # Get layout info
        print("\n📊 Layout Information:")
        layout_info = analyzer.get_layout_info()
        print(json.dumps(layout_info, indent=2))

        analyzer.close()

        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 PDF Resume Analyzer - Phase 1 Testing")
    print("=" * 60)

    # Test with a sample PDF
    # You'll need to download one of the provided PDFs first
    print("\n⚠️  To test, download a resume PDF and run:")
    print("python test_phase1.py path/to/resume.pdf")

    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        test_pdf_analysis(pdf_path)
    else:
        print("\n📋 Usage: python test_phase1.py <pdf_path>")
        print("\nExample:")
        print("python test_phase1.py resume1.pdf")
