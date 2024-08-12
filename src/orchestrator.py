import os
from dotenv import load_dotenv
from src.classes import prompt, chroma, chain

load_dotenv()

def create_chatbot(name: str, mood: str, project_name: str) -> chain:
    chroma_client = chroma.init_chroma(project_name)
    chroma_client.upload_files()

    pr_obj = prompt.init_prompt(name, mood)
    pr_obj.create_prompt_text()

    chain_obj = chain.init_chain(chroma_client, pr_obj)

    return chain_obj
