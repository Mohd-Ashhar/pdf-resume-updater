#!/usr/bin/env python3
"""
Setup script for PDF Resume Editor
"""
import os
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    packages = [
        "pymupdf",
        "pillow",
        "reportlab"
    ]

    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    dirs = ["input_resumes", "output_resumes", "logs"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Created {dir_name}/")

def create_readme():
    """Create README file"""
    readme_content = """# PDF Resume Editor - Quick Start Guide

## Setup Complete! 🎉

Your PDF Resume Editor is ready to use.

## Quick Start

1. **Add your resume PDFs** to the `input_resumes/` folder
2. **Run the processor**: `python main.py`
3. **Check outputs** in `output_resumes/` folder

## File Structure

- `pdf_analyzer.py` - Analyzes PDF structure
- `pdf_editor.py` - Edits PDFs with layout preservation
- `main.py` - Batch processor for multiple resumes
- `edit_config.json` - Configuration for edits
- `input_resumes/` - Place your PDFs here
- `output_resumes/` - Edited PDFs will be saved here

## Configuration

Edit `edit_config.json` to customize:
- Experience entries to add
- Skills to modify
- Certifications to add

## Testing Single Resume

```bash
python test_phase2.py input.pdf output.pdf
```

## Need Help?

Check the inline documentation in each Python file.
"""
    with open("README.md", "w") as f:
        f.write(readme_content)
    print("✅ Created README.md")

def main():
    print("="*60)
    print("🚀 PDF Resume Editor - Setup")
    print("="*60)

    check_python_version()

    if install_dependencies():
        create_directories()
        create_readme()

        print("\n" + "="*60)
        print("✅ SETUP COMPLETE!")
        print("="*60)
        print("\nNext steps:")
        print("1. Download the 5 resume PDFs from the assignment")
        print("2. Place them in the input_resumes/ folder")
        print("3. Run: python main.py")
        print("\n📖 Check README.md for detailed instructions")
    else:
        print("\n❌ Setup failed. Please install dependencies manually:")
        print("pip install pymupdf pillow reportlab")

if __name__ == "__main__":
    main()
