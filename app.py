from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os
import random

app = Flask(__name__)
app.secret_key = "vua-lich-su-secret-key"

CSV_FILE = "questions.csv"
TOTAL_QUESTIONS = 14


def load_questions():
    questions = []
    file_path = os.path.join(os.path.dirname(__file__), CSV_FILE)

    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row or not row.get("answer"):
                continue

            answer = row["answer"].strip().upper()
            if answer not in "ABCD":
                continue

            options = [row["A"], row["B"], row["C"], row["D"]]
            zipped = list(zip(options, "ABCD"))
            random.shuffle(zipped)
            shuffled, letters = zip(*zipped)

            questions.append({
                "question": row["question"],
                "options": list(shuffled),
                "answer": letters.index(answer)
            })

    random.shuffle(questions)
    return questions[:TOTAL_QUESTIONS]


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

    if index >= len(questions):
        return redirect(url_for("result"))

    q = questions[index]

    if request.method == "POST":
        selected = int(request.form["answer"])
        correct = q["answer"]

        if selected == correct:
            session["score"] += 1

        session["index"] += 1

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
    total = len(session.get("questions", []))

    if total == 0:
        return redirect(url_for("index"))

    return render_template("result.html", score=score, total=total)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
