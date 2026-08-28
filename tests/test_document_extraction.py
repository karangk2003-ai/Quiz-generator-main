import os
import pytest
from services.document_service import DocumentService

def test_extract_txt(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.txt"
    p.write_text("Hello World!")
    
    content = DocumentService.extract_text(str(p))
    assert content == "Hello World!"

def test_invalid_extension():
    with pytest.raises(ValueError):
        DocumentService.extract_text("test.png")
