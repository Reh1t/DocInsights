import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extractors import (
    extract_text_from_pdf,
    extract_text_from_txt,
    extract_text_from_docx,
    extract_text_from_html
)

TEST_DIR = os.path.dirname(__file__)

def test_extract_text_from_txt():
    file_path = os.path.join(TEST_DIR, "sample.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Hello world!")
    result = extract_text_from_txt(file_path)
    assert "Hello world!" in result
    os.remove(file_path)

def test_extract_text_from_html():
    html_content = "<html><body><h1>Hello</h1><script>alert('x');</script></body></html>"
    file_path = os.path.join(TEST_DIR, "sample.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    result = extract_text_from_html(file_path)
    assert "Hello" in result and "alert" not in result
    os.remove(file_path)
