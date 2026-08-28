document.addEventListener('DOMContentLoaded', () => {
    // ---- INDEX PAGE LOGIC ----
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        const dropArea = document.getElementById('dropArea');
        const fileInput = document.getElementById('file');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const removeFileBtn = document.getElementById('removeFileBtn');
        const uploadStatus = document.getElementById('uploadStatus');
        const quizConfigSection = document.getElementById('quizConfigSection');
        const documentIdInput = document.getElementById('documentId');
        const groqApiKeyInput = document.getElementById('groqApiKey');
        const toggleKeyBtn = document.getElementById('toggleKeyVisibility');

        // Restore saved key from localStorage if available
        const savedKey = localStorage.getItem('groq_api_key');
        if (savedKey && groqApiKeyInput) {
            groqApiKeyInput.value = savedKey;
        }

        if (groqApiKeyInput) {
            groqApiKeyInput.addEventListener('input', (e) => {
                const val = e.target.value.trim();
                if (val) {
                    localStorage.setItem('groq_api_key', val);
                } else {
                    localStorage.removeItem('groq_api_key');
                }
            });
        }

        if (toggleKeyBtn && groqApiKeyInput) {
            toggleKeyBtn.addEventListener('click', () => {
                if (groqApiKeyInput.type === 'password') {
                    groqApiKeyInput.type = 'text';
                    toggleKeyBtn.textContent = '🔒';
                } else {
                    groqApiKeyInput.type = 'password';
                    toggleKeyBtn.textContent = '👁️';
                }
            });
        }
        
        // Drag and drop handlers
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.add('dragover'), false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.remove('dragover'), false);
        });
        
        dropArea.addEventListener('drop', (e) => {
            let dt = e.dataTransfer;
            let files = dt.files;
            fileInput.files = files;
            updateFileInfo();
        });
        
        fileInput.addEventListener('change', updateFileInfo);
        
        removeFileBtn.addEventListener('click', () => {
            fileInput.value = '';
            updateFileInfo();
        });
        
        function updateFileInfo() {
            if (fileInput.files.length > 0) {
                fileName.textContent = fileInput.files[0].name;
                dropArea.classList.add('hidden');
                fileInfo.classList.remove('hidden');
            } else {
                dropArea.classList.remove('hidden');
                fileInfo.classList.add('hidden');
            }
        }
        
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (fileInput.files.length === 0) return;
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            showStatus(uploadStatus, 'Processing document & generating embeddings... Please wait.', 'success', true);
            const uploadBtn = document.getElementById('uploadBtn');
            uploadBtn.disabled = true;
            
            try {
                const res = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await res.json();
                if (res.ok) {
                    showStatus(uploadStatus, '✅ Document processed successfully into vector store!', 'success');
                    documentIdInput.value = data.document_id;
                    quizConfigSection.classList.remove('hidden');
                    quizConfigSection.scrollIntoView({ behavior: 'smooth' });
                } else {
                    showStatus(uploadStatus, data.error || 'Error processing file.', 'error');
                }
            } catch (error) {
                showStatus(uploadStatus, 'Network error while uploading document.', 'error');
            } finally {
                uploadBtn.disabled = false;
            }
        });
        
        const configForm = document.getElementById('configForm');
        const generateStatus = document.getElementById('generateStatus');
        
        configForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const num_questions = document.getElementById('num_questions').value;
            const difficulty = document.getElementById('difficulty').value;
            const topic = document.getElementById('topic').value;
            const doc_id = documentIdInput.value;
            const groq_api_key = groqApiKeyInput ? groqApiKeyInput.value.trim() : '';
            
            showStatus(generateStatus, '⚡ Groq is generating your quiz at lightning speed...', 'success', true);
            const generateBtn = document.getElementById('generateBtn');
            generateBtn.disabled = true;
            
            try {
                const res = await fetch('/api/generate-quiz', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        document_id: doc_id, 
                        num_questions, 
                        difficulty, 
                        topic,
                        groq_api_key
                    })
                });
                
                const data = await res.json();
                if (res.ok) {
                    localStorage.setItem('currentQuiz', JSON.stringify(data));
                    window.location.href = '/quiz';
                } else {
                    showStatus(generateStatus, `❌ ${data.error || 'Failed to generate quiz.'}`, 'error');
                    generateBtn.disabled = false;
                }
            } catch (error) {
                showStatus(generateStatus, 'Network error during quiz generation.', 'error');
                generateBtn.disabled = false;
            }
        });
    }
    
    // ---- QUIZ PAGE LOGIC ----
    const quizInterface = document.getElementById('quizInterface');
    if (quizInterface) {
        const loadingMsg = document.getElementById('loadingMsg');
        const quizDataStr = localStorage.getItem('currentQuiz');
        
        if (!quizDataStr) {
            window.location.href = '/';
            return;
        }
        
        const quizData = JSON.parse(quizDataStr);
        const questions = quizData.questions;
        
        if (!questions || questions.length === 0) {
            window.location.href = '/';
            return;
        }
        
        loadingMsg.classList.add('hidden');
        quizInterface.classList.remove('hidden');
        
        const questionsContainer = document.getElementById('questionsContainer');
        const currentQNum = document.getElementById('currentQNum');
        const totalQNum = document.getElementById('totalQNum');
        const progressBar = document.getElementById('progressBar');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const submitQuizBtn = document.getElementById('submitQuizBtn');
        
        totalQNum.textContent = questions.length;
        
        let currentIndex = 0;
        let userAnswers = {};
        
        function renderQuestion(index) {
            questionsContainer.innerHTML = '';
            const q = questions[index];
            
            const qBlock = document.createElement('div');
            qBlock.className = 'question-block fade-in';
            qBlock.innerHTML = `<h3 class="question-text">${index + 1}. ${q.question}</h3>`;
            
            const options = Object.entries(q.options);
            options.forEach(([key, val]) => {
                const label = document.createElement('label');
                label.className = `option-label ${userAnswers[index] === key ? 'selected' : ''}`;
                
                const input = document.createElement('input');
                input.type = 'radio';
                input.name = `q_${index}`;
                input.value = key;
                if (userAnswers[index] === key) input.checked = true;
                
                input.addEventListener('change', (e) => {
                    userAnswers[index] = e.target.value;
                    document.querySelectorAll('.option-label').forEach(l => l.classList.remove('selected'));
                    label.classList.add('selected');
                });
                
                label.appendChild(input);
                label.appendChild(document.createTextNode(` ${key}) ${val}`));
                qBlock.appendChild(label);
            });
            
            questionsContainer.appendChild(qBlock);
            currentQNum.textContent = index + 1;
            progressBar.style.width = `${((index + 1) / questions.length) * 100}%`;
            
            // Buttons
            prevBtn.classList.toggle('hidden', index === 0);
            
            if (index === questions.length - 1) {
                nextBtn.classList.add('hidden');
                submitQuizBtn.classList.remove('hidden');
            } else {
                nextBtn.classList.remove('hidden');
                submitQuizBtn.classList.add('hidden');
            }
        }
        
        renderQuestion(0);
        
        prevBtn.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--;
                renderQuestion(currentIndex);
            }
        });
        
        nextBtn.addEventListener('click', () => {
            if (currentIndex < questions.length - 1) {
                currentIndex++;
                renderQuestion(currentIndex);
            }
        });
        
        document.getElementById('quizForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const payloadAnswers = {};
            for (let i = 0; i < questions.length; i++) {
                payloadAnswers[i.toString()] = userAnswers[i] || "";
            }
            
            quizInterface.classList.add('hidden');
            const submitLoading = document.createElement('div');
            submitLoading.className = 'loading-container fade-in';
            submitLoading.innerHTML = '<div class="spinner"></div><p>Submitting answers & calculating score...</p>';
            document.querySelector('.container').appendChild(submitLoading);
            
            try {
                const res = await fetch('/api/submit-quiz', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ answers: payloadAnswers })
                });
                
                const data = await res.json();
                if (res.ok) {
                    localStorage.setItem('quizResult', JSON.stringify(data));
                    window.location.href = '/result';
                } else {
                    alert(data.error || 'Failed to submit quiz.');
                    submitLoading.remove();
                    quizInterface.classList.remove('hidden');
                }
            } catch (err) {
                alert('Network error while evaluating quiz.');
                submitLoading.remove();
                quizInterface.classList.remove('hidden');
            }
        });
    }
    
    // ---- RESULT PAGE LOGIC ----
    const resultInterface = document.getElementById('resultInterface');
    if (resultInterface) {
        const loadingMsg = document.getElementById('loadingMsg');
        const resultDataStr = localStorage.getItem('quizResult');
        
        if (!resultDataStr) {
            window.location.href = '/';
            return;
        }
        
        const result = JSON.parse(resultDataStr);
        loadingMsg.classList.add('hidden');
        resultInterface.classList.remove('hidden');
        
        document.getElementById('scoreText').textContent = result.score;
        document.getElementById('scorePercent').textContent = `${result.percentage}%`;
        
        const scoreCircle = document.querySelector('.score-circle');
        scoreCircle.style.background = `conic-gradient(var(--primary) ${result.percentage}%, var(--input-bg) 0%)`;
        
        const passStatus = document.getElementById('passStatus');
        passStatus.textContent = result.pass_status;
        passStatus.className = `mt-10 ${result.pass_status === 'Pass' ? 'status-pass' : 'status-fail'}`;
        
        document.getElementById('correctAnswers').textContent = result.correct_answers;
        document.getElementById('totalQuestions').textContent = result.total_questions;
        
        const reviewContainer = document.getElementById('reviewContainer');
        result.review.forEach((item, index) => {
            const el = document.createElement('div');
            el.className = `review-item ${item.is_correct ? 'correct' : 'wrong'}`;
            
            let optionsHtml = '';
            Object.entries(item.options).forEach(([k, v]) => {
                optionsHtml += `<p class="review-ans">- ${k}) ${v}</p>`;
            });
            
            el.innerHTML = `
                <div class="review-q">${index + 1}. ${item.question}</div>
                <div class="mb-10">${optionsHtml}</div>
                <p><strong>Your Answer:</strong> <span class="${item.is_correct ? 'text-success' : 'text-danger'}">${item.user_answer || 'None'}</span></p>
                <p><strong>Correct Answer:</strong> <span class="text-success">${item.correct_answer}</span></p>
                <div class="explanation-box">
                    <strong>Explanation:</strong> ${item.explanation}
                </div>
            `;
            reviewContainer.appendChild(el);
        });
    }
    
    function showStatus(element, msg, type, keepAlive=false) {
        element.textContent = msg;
        element.className = `status-msg fade-in status-${type}`;
        element.classList.remove('hidden');
        if (!keepAlive) {
            setTimeout(() => {
                element.classList.add('hidden');
            }, 5000);
        }
    }
});
