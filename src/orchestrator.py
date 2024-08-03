import os
from dotenv import load_dotenv
from src.classes import prompt

load_dotenv()

def create_chatbot(name: str, mood: str):
    pr_obj = prompt.init_prompt(name, mood)
