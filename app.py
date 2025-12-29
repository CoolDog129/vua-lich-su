@app.route("/question", methods=["GET", "POST"])
def question():
    if "index" not in session:
        session["index"] = 0
        session["score"] = 0

    idx = session["index"]

    if idx >= len(QUESTIONS):
        return redirect(url_for("result"))

    q = QUESTIONS[idx]

    options = {
        "A": q["A"],
        "B": q["B"],
        "C": q["C"],
        "D": q["D"],
    }

    return render_template(
        "index.html",   # ← MUST EXIST in /templates
        question=q["question"],
        options=options,
        current=idx + 1,
        total=len(QUESTIONS),
    )
