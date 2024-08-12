import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from src.orchestrator import create_chatbot
from src.classes import chain

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
global chain_obj

moods = ["happy", "angry", "sad"]

@app.route("/")
def home_page():
    return render_template("home.html", options = moods)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for uploaded_file in files:
            uploaded_file.save(f"{UPLOAD_FOLDER}/{uploaded_file.filename}")
        global chain_obj
        chain_obj = create_chatbot(name = request.form['name'], mood = request.form['mood'], project_name=request.form['project-name'])
        return render_template("chatbot.html", name = request.form['name'])
    elif request.method == 'GET':
        return render_template("home.html", options = moods)

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    answer = chain_obj.invoke_chain(userText, chain_obj.chroma_obj.project_name)
    return answer

@app.route("/exit", methods=['GET', 'POST'])
def exit():

    return "Exit"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)