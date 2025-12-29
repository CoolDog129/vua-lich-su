from flask import Flask, render_template, request, redirect, url_for, session
import csv
import random
import os

app = Flask(__name__)
app.secret_key = "vua-lich-su-secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "questions.csv")

def load_questions():
    questions = []
    with open(CSV_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            correct = row["answer"].strip().upper()
            options = {
                "A": row["A"],
                "B": row["B"],
                "C": row["C"],
                "D": row["D"],
            }

            # shuffle options
            items = list(options.items())
            random.shuffle(items)
            shuffled = dict(items)

            correct_key = None
            for k, v in shuffled.items():
                if options[correct] == v:
                    correct_key = k

            questions.append({
                "question": row["question"],
                "options": shuffled,
                "answer": correct_key
            })

    return questions


QUESTIONS = load_questions()


@app.route("/")
def home():
    session.clear()
    session["index"] = 0
    session["score"] = 0
    return redirect(url_for("question"))


@app.route("/question", methods=["GET", "POST"])
def question():
    index = session.get("index", 0)

    if index >= len(QUESTIONS):
        return redirect(url_for("result"))

    q = QUESTIONS[index]

    feedback = None
    correct_answer = None

    if request.method == "POST":
        selected = request.form.get("option")
        correct_answer = q["answer"]

        if selected == correct_answer:
            session["score"] += 1
            feedback = "correct"
        else:
            feedback = "wrong"

        session["index"] += 1

    return render_template(
        "index.html",
        question=q["question"],
        options=q["options"],
        feedback=feedback,
        correct_answer=correct_answer,
        current=index + 1,
        total=len(QUESTIONS)
    )


@app.route("/result")
def result():
    return render_template(
        "result.html",
        score=session.get("score", 0),
        total=len(QUESTIONS)
    )


if __name__ == "__main__":
    app.run(debug=True)
