from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

@views_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@views_bp.route('/quiz', methods=['GET'])
def quiz():
    return render_template('quiz.html')

@views_bp.route('/result', methods=['GET'])
def result():
    return render_template('result.html')
