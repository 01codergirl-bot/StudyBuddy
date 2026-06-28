StudyBuddy 📚✨

StudyBuddy is an AI-powered study assistant web app that turns your notes into a short summary and an interactive multiple-choice quiz. It is built using Flask and integrates the Groq API to generate study material from user input.

🚀 Features
- Paste notes and generate an AI summary
- Automatically create multiple-choice quiz questions
- Instant feedback on answers
- Score tracking during the quiz
- Clean and simple user interface

🧠 How it works
1. User enters study notes on the homepage
2. Flask sends the notes to the Groq AI API
3. The AI returns a structured JSON response containing a summary and quiz questions
4. The frontend displays the quiz and tracks user performance

🛠️ Tech Stack
- Python (Flask)
- HTML, CSS, JavaScript
- Groq API (LLaMA model)
- JSON for data handling

📁 Project Structure
StudyBuddy/
├── app.py
├── templates/
│   ├── index.html
│   └── quiz.html
├── requirements.txt
└── README.md

⚙️ Setup
1. Install dependencies:
   pip install flask groq

2. Set your API key:
   export GROQ_API_KEY="your_api_key_here"

3. Run the app:
   python app.py

🌱 Future Improvements
- Add user accounts and saved progress
- Add XP/streak system like Duolingo
- Add review mistakes mode
- Improve mobile design

👩‍💻 Author
Built as a beginner-friendly AI learning project exploring full-stack development and AI integration.
