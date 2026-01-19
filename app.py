
from flask import Flask, render_template_string, request
from datetime import datetime
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Our Love Story ❤️</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>

<audio autoplay loop>
  <source src="/static/love-song.mp3" type="audio/mpeg">
</audio>

{% if not started %}
<div class="container">
  <h1>Happy Valentine’s Day My Love 💖</h1>
  <p>Enter the date our forever began</p>
  <form method="post">
    <input type="date" name="anniversary" required>
    <button type="submit">Begin Our Story ❤️</button>
  </form>
</div>
{% else %}

<div class="container">
  <h1>Our Months Together 💕</h1>

  {% for month, photos in gallery.items() %}
  <div class="month-card">
    <h2>Month {{ month }} 💘</h2>
    <p>{{ messages.get(month, "Another month loving you ❤️") }}</p>

    {% for photo in photos %}
      <img src="/static/images/{{ photo }}">
    {% endfor %}
  </div>
  {% endfor %}
</div>

<div class="container">
  <h1>I’d still choose you in every lifetime 💍</h1>
  <p class="letter">
    My love,<br><br>
    From December 18, I didn’t know what forever would look like,
    but somehow it found me in you.<br><br>
    Loving you feels easy. Being with you feels safe.
    You are my home, my happiness, my person.<br><br>
    No matter how many months pass,
    I will always choose you.<br><br>
    Always yours ❤️
  </p>
</div>

{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entered = datetime.strptime(request.form["anniversary"], "%Y-%m-%d")
        anniversary = datetime(2024, 12, 18)

        if entered != anniversary:
            return "<h1 style='text-align:center;color:red'>Wrong date 😘 Try again</h1>"

        today = datetime.today()
        months = (today.year - anniversary.year) * 12 + today.month - anniversary.month + 1

        images = os.listdir("static/images")
        gallery = {}

        for img in images:
            if img.startswith("month"):
                month_num = int(img.split("_")[0].replace("month", ""))
                if month_num <= months:
                    gallery.setdefault(month_num, []).append(img)

        messages = {
            1: "The month everything changed ❤️",
            2: "Laughing with you feels like home 💕",
            3: "Comfort, love, and us 💖"
        }

        return render_template_string(
            HTML,
            started=True,
            gallery=dict(sorted(gallery.items())),
            messages=messages
        )

    return render_template_string(HTML, started=False)

if __name__ == "__main__":
    app.run()