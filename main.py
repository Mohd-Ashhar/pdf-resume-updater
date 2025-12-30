
import os
import json
from pathlib import Path
from typing import Dict, List
from pdf_editor import PDFResumeEditor
from datetime import datetime

class ResumeEditConfig:
    """Configuration for resume edits"""

    def __init__(self, config_file: str = "edit_config.json"):
        self.config_file = config_file
        self.config = self._load_or_create_config()

    def _load_or_create_config(self) -> Dict:
        """Load config or create default"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Create default configuration
            default_config = {
                "experience_to_add": [
                    "Senior Full Stack Developer | TechCorp Solutions | Jan 2024 - Present",
                    "• Architected and deployed scalable SaaS platform serving 50,000+ users",
                    "• Led team of 8 engineers in agile development of AI-powered features",
                    "• Implemented microservices architecture reducing latency by 45%",
                    "• Integrated multiple AI APIs (OpenAI, Anthropic) for intelligent automation",
                    "• Technologies: React, Node.js, Python, Docker, PostgreSQL, AWS",
                    "• Achieved 99.9% uptime through robust monitoring and DevOps practices"
                ],
                "skill_modifications": [
                    {"old": "Python", "new": "Python (Expert - 5+ years)"},
                    {"old": "JavaScript", "new": "JavaScript/TypeScript (Advanced)"},
                    {"old": "React", "new": "React & Next.js (Production)"}
                ],
                "certifications_to_add": [
                    "AWS Certified Solutions Architect - Professional (2024)",
                    "Google Cloud Professional Developer (2024)"
                ]
            }

            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)

            print(f"✅ Created default configuration: {self.config_file}")
            return default_config

    def get_experience_lines(self) -> List[str]:
        return self.config.get("experience_to_add", [])

    def get_skill_modifications(self) -> List[Dict]:
        return self.config.get("skill_modifications", [])

    def get_certifications(self) -> List[str]:
        return self.config.get("certifications_to_add", [])

class BatchResumeProcessor:
    """Process multiple resumes with same edits"""

    def __init__(self, input_dir: str = "input_resumes", output_dir: str = "output_resumes"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.config = ResumeEditConfig()

        # Create directories if they don't exist
        self.output_dir.mkdir(exist_ok=True)

        # Results tracking
        self.results = []

    def process_all_resumes(self):
        """Process all PDF resumes in input directory"""
        print("\n" + "="*70)
        print("🚀 BATCH RESUME PROCESSOR")
        print("="*70)

        # Find all PDF files
        pdf_files = list(self.input_dir.glob("*.pdf"))

        if not pdf_files:
            print(f"\n⚠️  No PDF files found in {self.input_dir}")
            print("Please add your resume PDFs to the input_resumes folder")
            return

        print(f"\n📁 Found {len(pdf_files)} PDF file(s) to process")
        print(f"📂 Output directory: {self.output_dir}")

        # Process each resume
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"\n{'='*70}")
            print(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
            print('='*70)

            result = self.process_single_resume(pdf_file)
            self.results.append(result)

        # Generate report
        self._generate_report()

    def process_single_resume(self, input_pdf: Path) -> Dict:
        """Process a single resume"""
        result = {
            "filename": input_pdf.name,
            "success": False,
            "experience_added": False,
            "skills_modified": 0,
            "certifications_added": 0,
            "errors": []
        }

        try:
            # Create output filename
            output_pdf = self.output_dir / f"edited_{input_pdf.name}"

            # Initialize editor
            print("\n🔧 Initializing editor...")
            editor = PDFResumeEditor(str(input_pdf), str(output_pdf))

            # Add Experience
            print("\n📝 Adding Experience...")
            experience_lines = self.config.get_experience_lines()
            if editor.add_experience(experience_lines, position="top"):
                result["experience_added"] = True
                print(f"✅ Added {len(experience_lines)} lines of experience")
            else:
                result["errors"].append("Failed to add experience")

            # Modify Skills
            print("\n🔄 Modifying Skills...")
            skill_mods = self.config.get_skill_modifications()
            for skill_mod in skill_mods:
                if editor.modify_skill(skill_mod["old"], skill_mod["new"]):
                    result["skills_modified"] += 1
                    print(f"✅ Modified: {skill_mod['old']} → {skill_mod['new']}")

            if result["skills_modified"] == 0:
                print("ℹ️  No skills were modified (may not exist in resume)")

            # Add Certifications
            print("\n🎓 Adding Certifications...")
            certifications = self.config.get_certifications()
            for cert in certifications:
                if editor.add_certification(cert):
                    result["certifications_added"] += 1
                    print(f"✅ Added: {cert}")

            # Save
            print("\n💾 Saving changes...")
            if editor.save():
                result["success"] = True
                result["output_path"] = str(output_pdf)

            editor.close()

        except Exception as e:
            result["errors"].append(str(e))
            print(f"\n❌ Error processing {input_pdf.name}: {str(e)}")

        return result

    def _generate_report(self):
        """Generate processing report"""
        print("\n" + "="*70)
        print("📊 PROCESSING REPORT")
        print("="*70)

        total = len(self.results)
        successful = sum(1 for r in self.results if r["success"])

        print(f"\n✅ Successfully processed: {successful}/{total}")

        for result in self.results:
            print(f"\n{'─'*70}")
            print(f"📄 {result['filename']}")

            if result["success"]:
                print(f"  ✅ Status: SUCCESS")
                print(f"  📝 Experience: {'✓' if result['experience_added'] else '✗'}")
                print(f"  🔄 Skills Modified: {result['skills_modified']}")
                print(f"  🎓 Certifications Added: {result['certifications_added']}")
                print(f"  📂 Output: {result.get('output_path', 'N/A')}")
            else:
                print(f"  ❌ Status: FAILED")
                if result["errors"]:
                    print(f"  Errors: {', '.join(result['errors'])}")

        # Save report to file
        report_file = self.output_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n💾 Detailed report saved: {report_file}")
        print("\n" + "="*70)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "output_resumes"
    else:
        input_dir = "input_resumes"
        output_dir = "output_resumes"

    processor = BatchResumeProcessor(input_dir, output_dir)
    processor.process_all_resumes()
