# PDF Resume Editor - Complete Usage Guide

## 📋 Project Overview

This tool automatically edits PDF resumes while preserving their original layout, fonts, and formatting.

## 🚀 Quick Start (3 Steps)

### Step 1: Setup
```bash
python setup.py
```

### Step 2: Download Sample Resumes
```bash
python download_resumes.py
```

### Step 3: Process All Resumes
```bash
python main.py
```

That's it! Check `output_resumes/` for edited PDFs.

---

## 📖 Detailed Documentation

### System Architecture

```
┌─────────────────────┐
│  pdf_analyzer.py    │  ← Analyzes PDF structure
│  - Extract text     │
│  - Identify sections│
│  - Get coordinates  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  pdf_editor.py      │  ← Edits PDFs
│  - Add experience   │
│  - Modify skills    │
│  - Add certs        │
│  - Preserve layout  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  main.py            │  ← Batch processor
│  - Process multiple │
│  - Generate reports │
│  - Config management│
└─────────────────────┘
```

### Configuration (edit_config.json)

Customize what gets added/modified:

```json
{
  "experience_to_add": [
    "Job Title | Company | Dates",
    "• Bullet point 1",
    "• Bullet point 2",
    "..."
  ],
  "skill_modifications": [
    {"old": "Python", "new": "Python (Expert)"}
  ],
  "certifications_to_add": [
    "AWS Certified Solutions Architect (2024)"
  ]
}
```

### Testing Individual Resumes

Test on a single resume before batch processing:

```bash
# Analyze structure
python test_phase1.py input.pdf

# Test editing
python test_phase2.py input.pdf output.pdf
```

### Advanced Usage

#### Custom Input/Output Directories
```bash
python main.py my_resumes/ my_outputs/
```

#### Modify Configuration Programmatically
```python
from main import ResumeEditConfig

config = ResumeEditConfig()
config.config["experience_to_add"].append("New line")
```

#### Process Single Resume
```python
from pdf_editor import PDFResumeEditor

editor = PDFResumeEditor("input.pdf", "output.pdf")
editor.add_experience(["Line 1", "Line 2", ...])
editor.modify_skill("Old Skill", "New Skill")
editor.add_certification("New Cert")
editor.save()
editor.close()
```

---

## 🔧 Troubleshooting

### Issue: "No sections found"
**Solution:** The PDF might have a unique layout. Check with:
```bash
python test_phase1.py problematic.pdf
```

### Issue: "Layout is broken after edit"
**Solutions:**
1. Reduce text length (shorter lines)
2. Adjust line spacing in pdf_editor.py
3. Use smaller font size

### Issue: "Skill not found"
**Solution:** Run test_phase1.py to see actual skill names in PDF

### Issue: "Font looks different"
**Solution:** Modify `_get_standard_font()` method to match original fonts better

---

## 📊 Output

### Generated Files

1. **Edited PDFs** - `output_resumes/edited_*.pdf`
2. **Processing Report** - `output_resumes/report_*.json`
3. **Configuration** - `edit_config.json`

### Report Structure
```json
{
  "filename": "resume1.pdf",
  "success": true,
  "experience_added": true,
  "skills_modified": 2,
  "certifications_added": 2,
  "output_path": "output_resumes/edited_resume1.pdf",
  "errors": []
}
```

---

## 🎯 Assignment Deliverables Checklist

- [ ] Script that preserves layout ✓ (pdf_editor.py)
- [ ] Code explanation ✓ (inline comments + this guide)
- [ ] Approach explanation ✓ (see Architecture section)
- [ ] 5 edited resume PDFs ✓ (run main.py)
- [ ] Experience added (5+ lines) ✓
- [ ] Skill modified ✓
- [ ] Certification added ✓

---

## 💡 Key Features

✅ **Layout Preservation**
- Coordinate-based text insertion
- Font matching system
- Spacing calculations

✅ **Multi-Format Support**
- One-column resumes
- Two-column resumes
- Complex layouts with graphics

✅ **Flexible Editing**
- Add multiple lines of text
- Modify existing content
- Create new sections

✅ **Batch Processing**
- Process 5+ resumes at once
- Automated reporting
- Configuration-driven

---

## 🔬 Testing Validation

After processing, verify:

1. **Layout Integrity**
   - No overlapping text
   - Consistent margins
   - Proper alignment

2. **Font Consistency**
   - Matching font families
   - Correct sizes
   - Proper styling (bold/italic)

3. **Content Accuracy**
   - All edits applied
   - No text loss
   - Proper formatting

---

## 📝 Code Quality

- Type hints throughout
- Comprehensive error handling
- Logging and reporting
- Modular architecture
- Production-ready structure

---

## 🚀 Extending the System

### Add New Edit Types

```python
# In pdf_editor.py
def add_project(self, project_lines: List[str]) -> bool:
    """Add project to Projects section"""
    # Similar to add_experience()
    pass
```

### Custom Section Detection

```python
# In pdf_analyzer.py
SECTION_KEYWORDS = [
    'your', 'custom', 'sections'
]
```

### Advanced Layout Detection

```python
# Detect columns
def detect_columns(self):
    # Analyze x-coordinates
    # Group text by column
    pass
```

---

## 📞 Support

For issues or questions:
1. Check test scripts output
2. Review error messages in reports
3. Examine PDF with test_phase1.py
4. Adjust configuration as needed

---

Generated by PDF Resume Editor v1.0
