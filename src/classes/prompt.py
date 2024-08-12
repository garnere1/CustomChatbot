import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

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
        self.system_prompt = """Given a chat history and the latest user question \
            which might reference context in the chat history, formulate a standalone question \
            which can be understood without the chat history. Do NOT answer the question, \
            just reformulate it if needed and otherwise return it as is."""

        self.first_sentence = f"You are a {self.mood} chatbot named {self.name}."

    def create_prompt_text(self) -> str:
        self.prompt_text = self.first_sentence + """
        Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
        {context}

        Question: {input}
        """
        
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)

        return self.prompt_text

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