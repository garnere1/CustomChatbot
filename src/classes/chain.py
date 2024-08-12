import os
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder, ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
from src.classes import chroma, prompt

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, openai_api_key=openai_key)

class chain():
    def __init__(
        self,
        chroma_obj: chroma,
        prompt_obj: prompt
    ):
        super().__init__
        self.store = {}
        self.chroma_obj = chroma_obj
        self.retriever = chroma_obj.retriever
        self.prompt_obj = prompt_obj
        self.context_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.prompt_obj.system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        self.history_retriever = create_history_aware_retriever(
            llm, self.retriever, self.context_prompt
        )

        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_obj.prompt_text),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        self.qa_chain = create_stuff_documents_chain(llm, self.qa_prompt)

        self.ra_chain = create_retrieval_chain(self.history_retriever, self.qa_chain)

        self.ultimate_chain = RunnableWithMessageHistory(
            self.ra_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def clear_convo(self, session_id: str) -> str:
        if session_id in self.store:
            self.store[session_id].clear()
            return("Success")
        return "Session ID not in store"

    def invoke_chain(self, question: str, session_id: str):
        chain_response = self.ultimate_chain.invoke(
            {"input": question},
            config = {
                "configurable": {"session_id": session_id}
            },
        )
        return chain_response['answer']
    
    def invoke_fake_chain(self, question:str):
        rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt_obj.prompt_template
            | llm
            | StrOutputParser()
        )

        print(rag_chain.invoke(question))
        

def init_chain(
    chroma_obj: chroma,
    prompt_obj: prompt
) -> chain:
    global chain_obj

    chain_obj = chain(chroma_obj, prompt_obj)

    return chain_obj

def get_chain() -> chain:
    return chain_obj

if __name__ == "__main__":
    init_chain()