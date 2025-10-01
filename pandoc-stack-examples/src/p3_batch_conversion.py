#!/usr/bin/env python
"""
Pandoc Stack Example 3: Batch Document Conversion
Converts multiple Markdown files to various formats simultaneously.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
DATA = ROOT / "data"
MARKDOWN_DIR = DATA / "markdown"

# Conversion configurations
CONVERSIONS = [
    {
        "input": "sample_report.md",
        "outputs": [
            {"format": "pdf", "options": ["--pdf-engine=pdflatex", "--toc"]},
            {"format": "docx", "options": ["--toc"]},
            {"format": "html", "options": ["--standalone", "--toc"]},
        ]
    },
    {
        "input": "complex_report.md",
        "outputs": [
            {"format": "pdf", "options": ["--pdf-engine=pdflatex", "--toc", "--number-sections"]},
            {"format": "docx", "options": ["--toc"]},
            {"format": "html", "options": ["--standalone", "--toc", "--css=github.css"]},
        ]
    }
]


def create_sample_documents() -> List[Path]:
    """Create sample documents for batch conversion."""
    MARKDOWN_DIR.mkdir(exist_ok=True, parents=True)

    # Sample report
    sample_content = """
---
title: "Sample Report"
author: "Batch Processing System"
date: "2024"
---

# Sample Report

This is a sample document for batch conversion testing.

## Section 1

Content for section 1.

## Section 2

Content for section 2.

### Subsection

More detailed content.
"""

    # Complex report
    complex_content = """
---
title: "Complex Technical Report"
author: "Advanced Systems"
date: "2024"
---

# Complex Technical Report

## Introduction

This report covers advanced technical topics.

## Technical Details

### Architecture

The system architecture includes multiple components.

### Implementation

Implementation details are provided below.

```python
def hello_world():
    print("Hello, World!")
    return True
```

## Results

Results show significant improvements.
"""

    files_created = []

    # Create sample report
    sample_file = MARKDOWN_DIR / "sample_report.md"
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    files_created.append(sample_file)

    # Create complex report
    complex_file = MARKDOWN_DIR / "complex_report.md"
    with open(complex_file, 'w', encoding='utf-8') as f:
        f.write(complex_content)
    files_created.append(complex_file)

    return files_created


def convert_single_file(input_path: Path, output_format: str, options: List[str]) -> Path:
    """
    Convert a single file to specified format.

    Args:
        input_path: Input Markdown file
        output_format: Target format (pdf, docx, html, etc.)
        options: Additional Pandoc options

    Returns:
        Path to output file
    """
    output_file = BUILD / f"{input_path.stem}_to_{output_format}.{output_format}"
    output_file.parent.mkdir(exist_ok=True, parents=True)

    cmd = [
        "pandoc",
        str(input_path),
        "-o", str(output_file),
        f"--to={output_format}"
    ] + options

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.returncode == 0:
            print(f"✅ Converted {input_path.name} → {output_file.name}")
            return output_file
        else:
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to convert {input_path.name}: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        raise


def batch_convert_documents(conversions: List[Dict], max_workers: int = 4) -> List[Path]:
    """
    Convert multiple documents in parallel.

    Args:
        conversions: List of conversion configurations
        max_workers: Maximum number of parallel conversions

    Returns:
        List of output file paths
    """
    print(f"🚀 Starting batch conversion with {max_workers} workers...")

    all_outputs = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all conversion tasks
        future_to_conversion = {}

        for conv_config in conversions:
            input_file = MARKDOWN_DIR / conv_config["input"]
            if not input_file.exists():
                print(f"⚠️  Skipping {conv_config['input']} - file not found")
                continue

            for output_config in conv_config["outputs"]:
                future = executor.submit(
                    convert_single_file,
                    input_file,
                    output_config["format"],
                    output_config["options"]
                )
                future_to_conversion[future] = (input_file, output_config["format"])

        # Collect results
        for future in as_completed(future_to_conversion):
            input_file, output_format = future_to_conversion[future]
            try:
                output_path = future.result()
                all_outputs.append(output_path)
            except Exception as e:
                print(f"❌ Conversion failed for {input_file.name} → {output_format}: {e}")

    return all_outputs


def generate_conversion_report(outputs: List[Path]) -> Path:
    """Generate a summary report of all conversions."""
    report_file = BUILD / "conversion_report.txt"

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("Batch Conversion Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total conversions: {len(outputs)}\n\n")

        # Group by input file
        by_input = {}
        for output in outputs:
            input_name = output.name.split('_to_')[0] + '.md'
            if input_name not in by_input:
                by_input[input_name] = []
            by_input[input_name].append(output)

        for input_file, output_files in by_input.items():
            f.write(f"Input: {input_file}\n")
            for output_file in output_files:
                f.write(f"  → {output_file.name}\n")
            f.write("\n")

        f.write("Conversion completed successfully!\n")

    print(f"📋 Conversion report saved: {report_file}")
    return report_file


def main():
    """Entry point"""
    try:
        # Create sample documents
        sample_files = create_sample_documents()
        print(f"📝 Created {len(sample_files)} sample documents")

        # Run batch conversion
        outputs = batch_convert_documents(CONVERSIONS)

        # Generate report
        report = generate_conversion_report(outputs)

        print("\n🎉 Batch conversion completed!")
        print(f"   Documents processed: {len(sample_files)}")
        print(f"   Files generated: {len(outputs)}")
        print(f"   Report: {report}")

        # Show summary
        print("\n📁 Generated files:")
        for output in sorted(outputs):
            print(f"   • {output.name}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
