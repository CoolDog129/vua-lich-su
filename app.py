<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Đáp án</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>

<div class="card">
    <h1>👑 VUA LỊCH SỬ</h1>
    <div class="progress">Câu {{ current }}/{{ total }}</div>

    <div class="question">{{ question }}</div>

    {% for key, value in options.items() %}
        <div class="option
            {% if key == correct %}correct{% endif %}
            {% if key == selected and key != correct %}wrong{% endif %}
        ">
            {{ value }}
        </div>
    {% endfor %}

    <a href="{{ url_for('next_question') }}" class="restart">Tiếp theo ➜</a>
</div>

</body>
</html>
