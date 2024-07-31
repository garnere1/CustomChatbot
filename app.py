import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

moods = ["happy", "angry", "sad"]

@app.route("/")
def home_page():
    return render_template("home.html", options = moods)

@app.route("/submit_mood", methods=['GET', 'POST'])
def submit_mood():
    if request.method == 'POST':
        print(request.form)
        return "<p>Got it!</p>"
    elif request.method == 'GET':
        return "<p>Get!</p>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)