import os
from dotenv import load_dotenv

load_dotenv()

class prompt():
    def __init__(
        self,
        name: str,
        mood: str
    ):
        super().__init__
        self.name = name
        self.mood = mood

    def create_prompt_text(self) -> str:
        prompt_text = f"You are a {self.mood} chatbot names {self.name}"
        return prompt_text

def init_prompt(
    name: str,
    mood: str
) -> prompt:
    global prompt_obj

    prompt_obj = prompt(name, mood)

    return prompt_obj

def get_prompt() -> prompt:
    return prompt_obj

if __name__ == "__main__":
    init_prompt()