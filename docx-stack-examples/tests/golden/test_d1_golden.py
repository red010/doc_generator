import os
from pathlib import Path
from importlib import import_module

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "golden"
GOLDEN.mkdir(exist_ok=True, parents=True)

norm = import_module("tools.normalize_docx")

CASES = [
    ("src.a1_docxtpl_basic", "out_a1_basic.docx", "a1_basic.xml"),
    ("src.a2_richtext", "out_a2_richtext.docx", "a2_richtext.xml"),
    ("src.a3_images", "out_a3_images.docx", "a3_images.xml"),
]

def run_and_get_xml(mod_name: str, out_name: str) -> str:
    mod = import_module(mod_name)
    out_path = mod.render()
    return norm.normalize_docx_to_string(out_path)

def test_examples_against_golden():
    update = os.getenv("UPDATE_GOLDEN") == "1"
    for mod_name, out_name, golden_xml in CASES:
        xml = run_and_get_xml(mod_name, out_name)
        gfile = GOLDEN / golden_xml
        if update or not gfile.exists():
            gfile.write_text(xml, encoding="utf-8")
        else:
            expected = gfile.read_text(encoding="utf-8")
            assert xml == expected, f"Differenza rispetto al golden: {golden_xml}"
