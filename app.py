from flask import Flask, render_template, request, redirect, url_for, session
import csv
import random
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for session

CSV_FILE = "questions.csv"
TOTAL_QUESTIONS = 14

# Load and shuffle questions
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
            if correct_letter not in ("A","B","C","D"):
                continue
            options = [row["A"], row["B"], row["C"], row["D"]]
            zipped = list(zip(options, ["A","B","C","D"]))
            random.shuffle(zipped)
            shuffled_options, letters = zip(*zipped)
            correct_index = letters.index(correct_letter)
            questions.append({
                "question": row["question"],
                "options": shuffled_options,
                "answer": correct_index
            })
    return questions

@app.route("/")
def index():
    # Initialize session
    all_qs = load_questions()
    session["questions"] = random.sample(all_qs, min(TOTAL_QUESTIONS, len(all_qs)))
    session["index"] = 0
    session["score"] = 0
    return redirect(url_for("question"))

@app.route("/question", methods=["GET", "POST"])
def question():
    if "questions" not in session:
        return redirect(url_for("index"))

    questions = session["questions"]
    index = session.get("index", 0)

    if index >= len(questions):
        return redirect(url_for("result"))

    q = questions[index]

    if request.method == "POST":
        selected = int(request.form.get("answer", -1))
        correct = q["answer"]
        if selected == correct:
            session["score"] += 1
        session["selected"] = selected
        session["correct"] = correct
        return redirect(url_for("feedback"))

    return render_template("index.html", question=q, index=index, total=len(questions))

@app.route("/feedback")
def feedback():
    index = session.get("index", 0)
    q = session["questions"][index]
    selected = session.get("selected", None)
    correct = session.get("correct", None)
    return render_template("feedback.html", question=q, selected=selected, correct=correct, index=index, total=len(session["questions"]))

@app.route("/next")
def next_question():
    session["index"] += 1
    if session["index"] >= len(session["questions"]):
        return redirect(url_for("result"))
    return redirect(url_for("question"))

@app.route("/result")
def result():
    score = session.get("score", 0)
    total = len(session.get("questions", []))
    return render_template("result.html", score=score, total=total)

if __name__ == "__main__":
    app.run(debug=True)