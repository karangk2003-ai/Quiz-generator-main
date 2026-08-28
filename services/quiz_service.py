import os
import json
from groq import Groq

class QuizService:
    def __init__(self):
        self.default_model = 'llama-3.1-8b-instant'

    def generate_quiz(self, context, num_questions, difficulty, topic, custom_api_key=None):
        """Generate MCQs using Groq cloud LLM."""
        api_key = custom_api_key or os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError(
                "Groq API Key is missing! Please enter your Groq API key in the web interface or set GROQ_API_KEY in the .env file."
            )
            
        client = Groq(api_key=api_key)
        topic_instruction = f"Focus specifically on the topic: '{topic}'." if topic else "Cover key concepts thoroughly."
        
        system_prompt = (
            "You are an expert AI quiz generator. You generate high-quality, unambiguous multiple-choice questions (MCQs) "
            "based strictly on the provided document context. Respond ONLY with a valid JSON object matching the requested schema."
        )
        
        user_prompt = f"""Based ONLY on the provided document context, generate exactly {num_questions} multiple-choice questions (MCQs) at a {difficulty} difficulty level.
{topic_instruction}

Rules:
- Generate questions and options ONLY from the provided context. Do NOT invent facts.
- Generate exactly four options (A, B, C, D) for each question.
- Ensure there is exactly one unequivocally correct answer per question.
- Include a short, clear explanation citing why the answer is correct based on the context.

Required JSON Schema:
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": {{
        "A": "Option A text",
        "B": "Option B text",
        "C": "Option C text",
        "D": "Option D text"
      }},
      "correct_answer": "A",
      "explanation": "Explanation text based on the document"
    }}
  ]
}}

Context:
{context}
"""
        
        try:
            completion = client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            raw_response = completion.choices[0].message.content.strip()
            
            # Clean possible markdown wrapping
            if raw_response.startswith("```json"):
                raw_response = raw_response[7:]
            if raw_response.startswith("```"):
                raw_response = raw_response[3:]
            if raw_response.endswith("```"):
                raw_response = raw_response[:-3]
                
            quiz_data = json.loads(raw_response.strip())
            
            if "questions" not in quiz_data or not isinstance(quiz_data["questions"], list):
                raise ValueError("Invalid format: 'questions' list missing in model response.")
                
            return quiz_data
        except Exception as e:
            raise Exception(f"Groq API Error: {str(e)}")

    def evaluate_quiz(self, quiz_data, user_answers):
        """
        Evaluate user answers against the generated quiz data.
        Returns a detailed result object.
        """
        questions = quiz_data.get('questions', [])
        total_questions = len(questions)
        correct_count = 0
        
        review = []
        
        for i, q in enumerate(questions):
            q_id = str(i)
            user_ans = user_answers.get(q_id)
            correct_ans = q.get('correct_answer')
            
            is_correct = (user_ans == correct_ans)
            if is_correct:
                correct_count += 1
                
            review.append({
                "question": q.get('question'),
                "options": q.get('options'),
                "user_answer": user_ans,
                "correct_answer": correct_ans,
                "is_correct": is_correct,
                "explanation": q.get('explanation')
            })
            
        score = correct_count
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        pass_status = "Pass" if percentage >= 50 else "Fail"
        
        return {
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "wrong_answers": total_questions - correct_count,
            "score": score,
            "percentage": round(percentage, 2),
            "pass_status": pass_status,
            "review": review
        }
