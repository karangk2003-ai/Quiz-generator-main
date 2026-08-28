import os
from flask import Blueprint, request, jsonify, current_app, session
from utils.helpers import validate_upload, generate_unique_filename
from services.document_service import DocumentService
from services.quiz_service import QuizService

api_bp = Blueprint('api', __name__)
quiz_service = QuizService()

# In-memory document store (bypassing slow vector DB)
document_store = {}

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "API is running with Groq backend."})

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400
        
    file = request.files['file']
    is_valid, error_msg = validate_upload(file)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
        
    filename = generate_unique_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Extract text
        text = DocumentService.extract_text(filepath)
        
        # Clean up temporary upload file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Store raw text in memory instead of slow vector DB
        document_id = filename.split('.')[0]
        
        # Limit text to ~25,000 characters to ensure it fits in prompt perfectly safely
        document_store[document_id] = text[:25000]
        
        return jsonify({"message": "Document processed successfully.", "document_id": document_id})
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": f"Failed to process document: {str(e)}"}), 500

@api_bp.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.json or {}
    document_id = data.get('document_id')
    num_questions = int(data.get('num_questions', 5))
    difficulty = data.get('difficulty', 'Medium')
    topic = data.get('topic', '')
    groq_api_key = data.get('groq_api_key', '').strip()
    
    if not document_id:
        return jsonify({"error": "Missing document_id."}), 400
        
    try:
        context = document_store.get(document_id)
        if not context:
            return jsonify({"error": "No content found for the given document. It may have expired."}), 404
            
        quiz_data = quiz_service.generate_quiz(
            context=context,
            num_questions=num_questions,
            difficulty=difficulty,
            topic=topic,
            custom_api_key=groq_api_key if groq_api_key else None
        )
        
        # Store quiz data in session for evaluation later
        session['current_quiz'] = quiz_data
        
        return jsonify(quiz_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    user_answers = (request.json or {}).get('answers', {})
    quiz_data = session.get('current_quiz')
    
    if not quiz_data:
        return jsonify({"error": "No active quiz found. Please generate a quiz first."}), 400
        
    try:
        result = quiz_service.evaluate_quiz(quiz_data, user_answers)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
