
import sys
from pdf_editor import PDFResumeEditor

def test_pdf_editing(input_pdf: str, output_pdf: str):
    """Test PDF editing functionality"""
    print(f"\n{'='*60}")
    print(f"Testing PDF Editor")
    print('='*60)
    print(f"Input: {input_pdf}")
    print(f"Output: {output_pdf}")

    try:
        # Initialize editor
        print("\n🔧 Initializing editor...")
        editor = PDFResumeEditor(input_pdf, output_pdf)

        # Test 1: Add Experience
        print("\n📝 Test 1: Adding Experience Entry...")
        experience_lines = [
            "Senior Software Engineer | Tech Company Inc. | Jan 2024 - Present",
            "• Led development of AI-powered automation platform using Python and Node.js",
            "• Architected microservices infrastructure serving 10,000+ users",
            "• Implemented CI/CD pipelines reducing deployment time by 60%",
            "• Mentored team of 5 junior developers on best practices",
            "• Technologies: React, Node.js, Docker, AWS, PostgreSQL"
        ]
        success = editor.add_experience(experience_lines, position="top")

        if success:
            print("✅ Experience added successfully")

        # Test 2: Modify Skill
        print("\n🔄 Test 2: Modifying Skill...")
        # You'll need to replace these with actual skills from the resume
        success = editor.modify_skill("Python", "Python (Advanced)")

        if success:
            print("✅ Skill modified successfully")
        else:
            print("ℹ️  Try another skill - check the resume content first")

        # Test 3: Add Certification
        print("\n🎓 Test 3: Adding Certification...")
        success = editor.add_certification(
            "AWS Certified Solutions Architect - Professional (2024)"
        )

        if success:
            print("✅ Certification added successfully")

        # Save the edited PDF
        print("\n💾 Saving edited PDF...")
        editor.save()
        editor.close()

        print("\n" + "="*60)
        print("✅ TESTING COMPLETE")
        print("="*60)
        print(f"\n📄 Check the output file: {output_pdf}")
        print("👀 Verify that:")
        print("  1. Layout is preserved")
        print("  2. Fonts match the original")
        print("  3. No text overlapping")
        print("  4. All edits are visible")

        return True

    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 PDF Resume Editor - Phase 2 Testing")
    print("=" * 60)

    if len(sys.argv) >= 3:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2]
        test_pdf_editing(input_pdf, output_pdf)
    else:
        print("\n📋 Usage: python test_phase2.py <input_pdf> <output_pdf>")
        print("\nExample:")
        print("python test_phase2.py resume1.pdf resume1_edited.pdf")
