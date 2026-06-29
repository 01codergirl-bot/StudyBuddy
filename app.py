import json
from flask import Flask, render_template, request, redirect, session, url_for
from groq import Groq

app = Flask(__name__)
app.secret_key = "dev_secret_key"

client = Groq(api_key="your key")


@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# SAFE AI CALL
# -------------------------------
def call_ai(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    if not response.choices:
        return ""

    return response.choices[0].message.content


# -------------------------------
# JSON EXTRACTION SAFETY
# -------------------------------
def extract_json(text):
    if not text:
        return None

    text = text.strip()
    text = text.replace("```json", "").replace("```", "")

    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        return None

    try:
        return json.loads(text[start:end])
    except:
        return None


# -------------------------------
# MAIN ROUTE
# -------------------------------
@app.route("/process", methods=["POST"])
def process():
    notes = request.form["notes"]

    # 🔥 STRONG PROMPT (forces REAL answers, not A/B/C nonsense)
    prompt = f"""
You are a professional teacher creating study quizzes.

Return ONLY valid JSON.

IMPORTANT RULES:
- Each option MUST be a FULL answer sentence (not just "A", "B", etc.)
- Each option must be meaningful and different
- Answer must match one of the options exactly
- No shortcuts like "A/B/C/D"
- No empty or vague answers

FORMAT:
{{
  "summary": "4-6 sentence explanation",
  "quiz": [
    {{
      "question": "clear question",
      "options": [
        "Full answer choice 1",
        "Full answer choice 2",
        "Full answer choice 3",
        "Full answer choice 4"
      ],
      "answer": "exact full correct option"
    }}
  ]
}}

Create EXACTLY 10 questions.

NOTES:
{notes}
"""

    # -------------------------------
    # TRY 1
    # -------------------------------
    raw = call_ai(prompt)
    data = extract_json(raw)

    # -------------------------------
    # TRY 2 (retry if broken)
    # -------------------------------
    if not data:
        print("Retrying AI...")
        raw = call_ai(prompt)
        data = extract_json(raw)

    # -------------------------------
    # FALLBACK (never break UI)
    # -------------------------------
    if not data:
        print("Using fallback quiz")

        data = {
            "summary": "We could not generate a full quiz from your notes, but here is a sample question to keep you going.",
            "quiz": [
                {
                    "question": "What is photosynthesis?",
                    "options": [
                        "Process where plants use sunlight to make food",
                        "A type of animal reproduction process",
                        "A weather pattern involving clouds",
                        "A chemical reaction in rocks"
                    ],
                    "answer": "Process where plants use sunlight to make food"
                }
            ]
        }

    quiz = data.get("quiz", [])
    summary = data.get("summary", "")

    # -------------------------------
    # VALIDATION (extra safety layer)
    # -------------------------------
    clean_quiz = []
    for q in quiz:
        if (
            isinstance(q, dict)
            and "question" in q
            and "options" in q
            and "answer" in q
            and len(q["options"]) == 4
        ):
            clean_quiz.append(q)

    if not clean_quiz:
        clean_quiz = data["quiz"]

    # -------------------------------
    # SAVE SESSION
    # -------------------------------
    session["summary"] = summary
    session["quiz"] = clean_quiz

    return redirect(url_for("quiz_page"))


@app.route("/quiz")
def quiz_page():
    summary = session.get("summary")
    quiz = session.get("quiz")

    if not quiz:
        return redirect(url_for("home"))

    return render_template("quiz.html", summary=summary, quiz=quiz)


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
