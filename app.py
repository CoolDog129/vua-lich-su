from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os
import random

app = Flask(__name__)
app.secret_key = "vua-lich-su-secret-key"

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
    questions = session.get("questions", [])
    index = session.get("index", 0)

    if not questions or index >= len(questions):
        return redirect(url_for("result"))

    q = questions[index]

    if request.method == "POST":
        selected = int(request.form["answer"])
        correct = q["answer"]

        if selected == correct:
            session["score"] = session.get("score", 0) + 1

        session["index"] = index + 1

        return render_template(
            "feedback.html",
            question=q["question"],
            options=q["options"],
            selected=selected,
            correct=correct,
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
    questions = session.get("questions", [])
    total = len(questions)

    # absolute safety: never crash
    if total == 0:
        return redirect(url_for("index"))

    return render_template(
        "result.html",
        score=score,
        total=total
    )


# ========= RUN =========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
