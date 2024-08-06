import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from src.orchestrator import create_chatbot
from src.classes import chain

load_dotenv()

app = Flask(__name__)

moods = ["happy", "angry", "sad"]

@app.route("/")
def home_page():
    return render_template("home.html", options = moods)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        created_chain = create_chatbot(name = request.form['name'], mood = request.form['mood'])
        return render_template("chatbot.html")
    elif request.method == 'GET':
        return render_template("home.html", options = moods)

@app.route("/query", methods=['POST'])
def query():
    created_chain = chain.get_chain()
    question = request.form['question']
    answer = created_chain.invoke_chain(question)
    return answer

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)