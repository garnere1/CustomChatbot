import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from src.orchestrator import create_chatbot, upload_files
from src.classes import chain

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

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
        upload_files(request.form['project-name'])
        created_chain = create_chatbot(name = request.form['name'], mood = request.form['mood'])
        return render_template("chatbot.html")
    elif request.method == 'GET':
        return render_template("home.html", options = moods)

@app.route("/get")
def get_bot_response():
    created_chain = chain.get_chain()
    userText = request.args.get('msg')
    answer = created_chain.invoke_chain(userText)
    return answer

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)