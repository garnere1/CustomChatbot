import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2, openai_api_key=openai_key)
class chain():
    def __init__(
        self,
        prompt: str
    ):
        super().__init__
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    prompt,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        self.llmchain = chat_prompt | chat
    
    def invoke_chain(self, message: str) -> str:
        answer = self.llmchain.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=message
                    )
                ],
            }
        )
        print(answer)
        return answer


def init_chain(
    prompt: str
) -> chain:
    global chain_obj

    chain_obj = chain(prompt)

    return chain_obj

def get_chain() -> chain:
    return chain_obj

if __name__ == "__main__":
    init_chain()