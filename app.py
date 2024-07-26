import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/home")
def home():
    return "<p>Got it!</p>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)