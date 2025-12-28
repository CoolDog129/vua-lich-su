from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os
import random

app = Flask(__name__)
app.secret_key = "vua-lich-su-secret-key"  # required for session

CSV_FILE = "questions.csv"
TOTAL_QUESTIONS = 14


# ========= LOAD QUESTIONS =========
def load_questions():
    questions = []

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, CSV_FILE)

    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row or row.get("answer") is None:
                continue

            correct_letter = row["answer"].strip().upper()
            if correct_letter not in ("A", "B", "C", "D"):
                continue

            options = [row["A"], row["B"], row["C"], row["D"]]

            zipped = list(zip(options, ["A", "B", "C", "D"]))
            random.shuffle(zipped)
            shuffled_options, letters = zip(*zipped)

            questions.append({
                "question": row["question"],
                "options": list(shuffled_options),
                "answer": letters.index(correct_letter)
            })

    random.shuffle(questions)
    return questions[:TOTAL_QUESTIONS]


# ========= ROUTES =========
@app.route("/")
def index():
    session.clear()
    session["questions"] = load_questions()
    session["index"] = 0
    session["score"] = 0
    return redirect(url_for("question"))


@app.route("/question", methods=["GET", "POST"])
def question():
    questions = session.get("questions")
    index = session.get("index", 0)

    if not questions or index >= len(questions):
        return redirect(url_for("result"))

    q = questions[index]
    feedback = None
    selected = None

    if request.method == "POST":
        selected = int(request.form["answer"])
        correct = q["answer"]

        if selected == correct:
            session["score"] += 1
            feedback = "correct"
        else:
            feedback = "wrong"

        session["index"] += 1

        return render_template(
            "feedback.html",
            question=q["question"],
            options=q["options"],
            selected=selected,
            correct=correct,
            feedback=feedback,
            index=index + 1,
            total=len(questions)
        )

    return render_template(
        "index.html",
        question=q["question"],
        options=q["options"],
        index=index + 1,
        total=len(questions)
    )


@app.route("/result")
def result():
    score = session.get("score", 0)
    total = len(session.get("questions", []))
    return render_template("result.html", score=score, total=total)


# ========= RUN =========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
