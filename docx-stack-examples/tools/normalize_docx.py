import re, zipfile
from pathlib import Path

VOLATILE_PATTERNS = [
    r'w:rsid[A-Za-z]*="[^"]+"',
    r'w14:paraId="[^"]+"',
    r'w14:textId="[^"]+"',
    r'w:paraId="[^"]+"',
    r'w:paraIdDel="[^"]+"',
    r'w:paraIdParent="[^"]+"',
    r'wp:docPr\s+id="[^"]+"',
    r'pic:cNvPr\s+id="[^"]+"',
    r'cx:uid="[^"]+"',
]

def normalize_xml(xml: str) -> str:
    for pat in VOLATILE_PATTERNS:
        xml = re.sub(pat, "", xml)
    xml = re.sub(r"\s+", " ", xml).strip()
    return xml

def extract_main_xml(docx_path: Path) -> str:
    with zipfile.ZipFile(docx_path, "r") as z:
        xml = z.read("word/document.xml").decode("utf-8", errors="ignore")
    return xml

def normalize_docx_to_string(docx_path: Path) -> str:
    return normalize_xml(extract_main_xml(docx_path))
