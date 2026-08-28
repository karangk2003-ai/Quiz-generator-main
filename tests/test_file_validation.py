import pytest
from utils.helpers import allowed_file, validate_upload

class MockFile:
    def __init__(self, filename):
        self.filename = filename

def test_allowed_file():
    assert allowed_file("test.pdf") == True
    assert allowed_file("test.docx") == True
    assert allowed_file("test.txt") == True
    assert allowed_file("test.jpg") == False
    assert allowed_file("test") == False

def test_validate_upload():
    valid_file = MockFile("test.pdf")
    is_valid, err = validate_upload(valid_file)
    assert is_valid == True
    assert err == ""

    invalid_file = MockFile("test.png")
    is_valid, err = validate_upload(invalid_file)
    assert is_valid == False
    assert "Unsupported file format" in err

    empty_file = MockFile("")
    is_valid, err = validate_upload(empty_file)
    assert is_valid == False
    assert "No selected file" in err
