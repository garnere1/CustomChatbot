import os
from dotenv import load_dotenv
from src.classes import prompt, chain

load_dotenv()

def create_chatbot(name: str, mood: str) -> chain:
    pr_obj = prompt.init_prompt(name, mood)
    prompt_text = pr_obj.create_prompt_text()
    chain_obj = chain.init_chain(prompt_text)
    return chain_obj