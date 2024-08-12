import os
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from src.orchestrator import create_chatbot
from src.classes import chain

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
try:
    files = os.listdir(UPLOAD_FOLDER)
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        print("All files deleted successfully.")
except OSError:
    print("Error occurred while deleting files.")
    
global chain_obj

moods = ["Happy", "Angry", "Sad"]

@app.route("/")
def home_page():
    return render_template("home.html", options = moods)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        files = request.files.getlist("file")
        global chain_obj
        chain_obj = create_chatbot(user_form=request.form, file_list=files)
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
    try:
        files = os.listdir(UPLOAD_FOLDER)
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            print("All files deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")
    return "Exit"

@app.errorhandler(404)
def catch_all(err):
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)