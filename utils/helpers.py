import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """Generate a secure, unique filename to avoid collisions."""
    ext = filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name

def validate_upload(file):
    """
    Validate the uploaded file.
    Returns (is_valid, error_message)
    """
    if file.filename == '':
        return False, "No selected file."
    
    if not allowed_file(file.filename):
        return False, "Unsupported file format. Please upload PDF, DOCX, or TXT."
        
    return True, ""
