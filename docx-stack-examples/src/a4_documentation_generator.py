"""
Documentation Generator - Markdown to DOCX
Converts structured markdown documentation into professional Word documents.
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from docxtpl import DocxTemplate, RichText

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)

TEMPLATE = ROOT / "templates" / "a4_documentation_template.docx"
SOURCE_MD = ROOT / "guide" / "docx_docxtpl_docxcompose.md"
OUT = BUILD / "out_a4_documentation.docx"


class MarkdownParser:
    """Parse markdown content into structured data for DOCX generation."""

    def __init__(self, markdown_content: str):
        self.content = markdown_content
        self.lines = markdown_content.split('\n')

    def extract_frontmatter(self) -> Dict[str, Any]:
        """Extract YAML frontmatter from markdown."""
        frontmatter = {}
        in_frontmatter = False

        for line in self.lines:
            line = line.strip()
            if line == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            elif in_frontmatter:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    frontmatter[key] = value

        return frontmatter

    def parse_sections(self) -> List[Dict[str, Any]]:
        """Parse markdown sections and their content."""
        sections = []
        current_section = None
        current_items = []
        current_code_blocks = []

        i = 0
        while i < len(self.lines):
            line = self.lines[i].strip()

            # Skip frontmatter and title
            if line.startswith('---') or line.startswith('# ') or line.startswith('>'):
                i += 1
                continue

            # Section headers
            if line.startswith('## '):
                # Save previous section
                if current_section:
                    current_section['items'] = current_items
                    current_section['codeblocks'] = current_code_blocks
                    sections.append(current_section)

                # Start new section
                current_section = {
                    'sectiontitle': line[3:].strip(),
                    'items': [],
                    'codeblocks': []
                }
                current_items = []
                current_code_blocks = []

            # List items
            elif line.startswith('* ') or line.startswith('- '):
                if current_section:
                    itemcontent = line[2:].strip()
                    # Handle links in markdown format
                    itemcontent = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', itemcontent)
                    current_items.append({'itemcontent': itemcontent, 'type': 'list_item'})

            # Code blocks
            elif line.startswith('```'):
                code_lines = []
                i += 1
                while i < len(self.lines) and not self.lines[i].strip().startswith('```'):
                    code_lines.append(self.lines[i])
                    i += 1

                if code_lines and current_section:
                    code_content = '\n'.join(code_lines).strip()
                    # Create RichText for code formatting
                    rt = RichText()
                    rt.add(code_content, font='Courier New', size=20)  # Monospace font
                    current_code_blocks.append({'codeblockcontent': rt, 'type': 'code'})

            # Regular paragraphs
            elif line and not line.startswith('#') and current_section:
                # Skip section separators
                if line.startswith('---'):
                    pass
                else:
                    current_items.append({'itemcontent': line, 'type': 'paragraph'})

            i += 1

        # Add final section
        if current_section:
            current_section['items'] = current_items
            current_section['codeblocks'] = current_code_blocks
            sections.append(current_section)

        return sections


def parse_markdown_to_docx_data(markdown_path: Path) -> Dict[str, Any]:
    """Convert markdown file to data structure for DOCX template."""
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()

    parser = MarkdownParser(content)
    frontmatter = parser.extract_frontmatter()
    sections = parser.parse_sections()

    # Format authors
    authors = frontmatter.get('authors', '')
    if authors:
        # Remove markdown list formatting
        authors = re.sub(r'^\* ', '', authors, flags=re.MULTILINE)
        authors = authors.replace('\n* ', '\n').strip()

    return {
        'documenttitle': frontmatter.get('title', 'Documentation'),
        'documentdescription': frontmatter.get('description', ''),
        'documentauthors': authors,
        'documentobjective': 'Obiettivo: creare documenti Word editabili partendo da template DOCX (Jinja) e assemblare più sezioni/moduli in un unico fascicolo, preservando stili, header/footer e interruzioni.',
        'sections': sections
    }


def render(output_path: Optional[Path] = None) -> Path:
    """
    Generate documentation DOCX from markdown source.

    Args:
        output_path: Optional custom output path. Defaults to OUT.

    Returns:
        Path to the generated document.
    """
    if output_path is None:
        output_path = OUT

    # Validate template exists
    if not TEMPLATE.exists():
        raise FileNotFoundError(
            f"Template mancante: {TEMPLATE}\n"
            "Crea il template manualmente seguendo la guida:\n"
            "docx-stack-examples/guide/create_manual_template_guide.md"
        )

    # Validate source markdown exists
    if not SOURCE_MD.exists():
        raise FileNotFoundError(f"File markdown mancante: {SOURCE_MD}")

    print(f"📄 Caricamento template: {TEMPLATE.name}")
    print(f"📖 Lettura documentazione: {SOURCE_MD.name}")

    # Parse markdown to structured data
    print("🔍 Analisi contenuto markdown...")
    docx_data = parse_markdown_to_docx_data(SOURCE_MD)

    # Debug sections structure
    print("=== DEBUG SEZIONI ===")
    for i, section in enumerate(docx_data['sections'][:3]):  # Debug solo prime 3 sezioni
        print(f"Sezione {i+1}: {section.get('sectiontitle', 'NO TITLE')}")
        print(f"  Items: {len(section.get('items', []))} (type: {type(section.get('items', []))})")
        print(f"  Codeblocks: {len(section.get('codeblocks', []))} (type: {type(section.get('codeblocks', []))})")

        # Check if items/codeblocks are iterable
        try:
            list(section.get('items', []))
            print("  Items: ITERABILE")
        except:
            print("  Items: NON ITERABILE")

        try:
            list(section.get('codeblocks', []))
            print("  Codeblocks: ITERABILE")
        except:
            print("  Codeblocks: NON ITERABILE")

        # Debug item values
        if section.get('items'):
            for j, item in enumerate(section['items'][:2]):  # Debug solo primi 2 item
                print(f"    Item {j+1}: {item}")
                print(f"    Keys: {list(item.keys()) if isinstance(item, dict) else 'NOT_DICT'}")
                if isinstance(item, dict) and 'itemcontent' in item:
                    print(f"    itemcontent: {repr(item['itemcontent'])} (type: {type(item['itemcontent'])})")

    # Load template and render
    print(f"⚙️ Rendering documentazione...")
    doc = DocxTemplate(str(TEMPLATE))
    doc.render(docx_data)
    doc.save(str(output_path))

    print(f"✅ Documentazione generata: {output_path}")
    print(f"   Sezioni: {len(docx_data['sections'])}")
    print(f"   Titolo: {docx_data['documenttitle']}")

    return output_path


if __name__ == "__main__":
    try:
        result = render()
        print(f"\n🎉 Successo! Documentazione creata: {result}")
        print("Il documento contiene la guida completa DOCX trasformata in formato Word professionale!")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        exit(1)
