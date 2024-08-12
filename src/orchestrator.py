import os
from dotenv import load_dotenv
from src.classes import prompt, chroma, chain
from werkzeug.datastructures import ImmutableMultiDict

load_dotenv()
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

def create_chatbot(user_form: ImmutableMultiDict(), file_list: list()) -> chain:
    project_name = user_form["project-name"]
    name = user_form["name"]
    mood = user_form["mood"]
    for uploaded_file in file_list:
        uploaded_file.save(f"{UPLOAD_FOLDER}/{uploaded_file.filename}")

    chroma_client = chroma.init_chroma(project_name)
    chroma_client.upload_files()
    if user_form["url"]:
        chroma_client.load_url(user_form['url'])
    pr_obj = prompt.init_prompt(name, mood)
    pr_obj.create_prompt_text()

    chain_obj = chain.init_chain(chroma_client, pr_obj)

    return chain_obj
