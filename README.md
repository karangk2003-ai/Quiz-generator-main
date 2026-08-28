# AI-Powered Quiz Generator (Groq ⚡ Edition)

A modern, responsive web application that generates multiple-choice questions (MCQs) from uploaded documents (PDF, DOCX, TXT) using **Groq Cloud LLMs** (`llama-3.3-70b-versatile`) and **ChromaDB Vector Database**.

## Features
- **Ultra-Fast Generation:** Powered by Groq's high-speed inference engine.
- **Document Support:** Upload PDF, DOCX, and TXT files.
- **Local Vector Storage:** Extracts text chunks and stores embeddings in a persistent ChromaDB database (no local Ollama server needed!).
- **MCQ Generation:** Generates 5, 10, 15, or 20 multiple-choice questions with 4 options, the single correct answer, and an explanation.
- **Interactive Quiz Taking & Evaluation:** Instant evaluation, score percentage, pass/fail status, and question-by-question review.
- **Flexible API Key Setup:** Enter your Groq API key directly in the web UI or configure it in `.env`.

## Architecture
- **Backend:** Python 3.10+, Flask
- **LLM Inference:** Groq Cloud API (`llama-3.3-70b-versatile`) via `groq` & `langchain-groq`
- **Vector Database:** ChromaDB (Built-in ONNX embeddings)
- **Frontend:** HTML5, CSS3 (Glassmorphism Dark Theme), JavaScript

## Quick Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get a Free Groq API Key:**
   - Sign up at [https://console.groq.com/keys](https://console.groq.com/keys).
   - Create a free API key (starts with `gsk_...`).

3. **Configure Environment (Optional):**
   You can add your key in `.env` or simply paste it in the UI when using the app:
   ```env
   GROQ_API_KEY=gsk_your_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```

5. **Open in Browser:**
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Troubleshooting
- **Missing API Key:** Enter your Groq API Key in the box on the home page or set `GROQ_API_KEY` in `.env`.
- **Upload Errors:** Ensure the uploaded document contains readable text and is under 16MB.
