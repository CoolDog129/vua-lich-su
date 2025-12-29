from flask import Flask, render_template, request, redirect, url_for, session
import csv
import random
import os

app = Flask(__name__)
app.secret_key = "vua-lich-su-secret"

CSV_FILE = "questions.csv"
TOTAL_QUESTIONS = 14


def load_questions():
    questions = []
    with open(CSV_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            options = {
                "A": row["A"],
                "B": row["B"],
                "C": row["C"],
                "D": row["D"],
            }
            questions.append({
                "question": row["question"],
                "options": options,
                "answer": row["answer"].strip().upper()
            })
    random.shuffle(questions)
    return questions[:TOTAL_QUESTIONS]


QUESTIONS = load_questions()


@app.route("/")
def start():
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

    if request.method == "POST":
        selected = request.form.get("option")
        session["selected"] = selected
        session["correct"] = q["answer"]

        if selected == q["answer"]:
            session["score"] += 1

        return redirect(url_for("feedback"))

    return render_template(
        "index.html",
        question=q["question"],
        options=q["options"],
        current=index + 1,
        total=len(QUESTIONS)
    )


@app.route("/feedback")
def feedback():
    index = session["index"]
    q = QUESTIONS[index]

    return render_template(
        "feedback.html",
        question=q["question"],
        options=q["options"],
        selected=session["selected"],
        correct=session["correct"],
        current=index + 1,
        total=len(QUESTIONS)
    )


@app.route("/next")
def next_question():
    session["index"] += 1
    return redirect(url_for("question"))


@app.route("/result")
def result():
    return render_template(
        "result.html",
        score=session["score"],
        total=len(QUESTIONS)
    )


if __name__ == "__main__":
    app.run(debug=True)
