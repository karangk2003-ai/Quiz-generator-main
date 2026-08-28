import pytest
from services.quiz_service import QuizService

def test_evaluate_quiz():
    qs = QuizService()
    
    mock_quiz_data = {
        "questions": [
            {
                "question": "What is the capital of France?",
                "options": {"A": "Berlin", "B": "Madrid", "C": "Paris", "D": "Rome"},
                "correct_answer": "C",
                "explanation": "Paris is the capital of France."
            },
            {
                "question": "What is 2 + 2?",
                "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
                "correct_answer": "B",
                "explanation": "2 + 2 equals 4."
            }
        ]
    }
    
    user_answers_all_correct = {"0": "C", "1": "B"}
    result = qs.evaluate_quiz(mock_quiz_data, user_answers_all_correct)
    
    assert result["total_questions"] == 2
    assert result["correct_answers"] == 2
    assert result["score"] == 2
    assert result["percentage"] == 100.0
    assert result["pass_status"] == "Pass"
    
    user_answers_partial = {"0": "A", "1": "B"}
    result = qs.evaluate_quiz(mock_quiz_data, user_answers_partial)
    
    assert result["correct_answers"] == 1
    assert result["wrong_answers"] == 1
    assert result["percentage"] == 50.0
    assert result["pass_status"] == "Pass"
    
    user_answers_fail = {"0": "A", "1": "A"}
    result = qs.evaluate_quiz(mock_quiz_data, user_answers_fail)
    
    assert result["pass_status"] == "Fail"
