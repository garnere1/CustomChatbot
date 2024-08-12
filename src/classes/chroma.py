import os
from dotenv import load_dotenv
import chromadb
from langchain_community.document_loaders import TextLoader, Docx2txtLoader, UnstructuredCSVLoader, PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
load_dotenv()

class chroma():
    def __init__(
        self,
        custom_name: str
    ):
        super().__init__
        self.custom_name = custom_name
        self.vector_store = Chroma(
                collection_name=custom_name,
                embedding_function=embeddings,
        )

    def upload_files(self) -> str:
        upload_folder = os.getenv("UPLOAD_FOLDER")
        for file_name in os.listdir(upload_folder):
            file_upload = os.path.join(upload_folder, file_name)
            if file_upload.endswith(".txt"):
                loader = TextLoader(file_upload)
                docs = loader.load()
            elif file_upload.endswith(".docx"):
                loader = Docx2txtLoader(file_upload)
                docs = loader.load()
            elif file_upload.endswith(".pdf"):
                loader = PyPDFLoader(file_upload)
                docs = loader.load()
            elif file_upload.endswith(".csv"):
                loader = UnstructuredCSVLoader(file_upload)
                docs = loader.load()
            self.vector_store.add_documents(docs)


def init_chroma(
    custom_name: str
) -> chroma:
    global chroma_obj

    chroma_obj = chroma(custom_name)

    return chroma_obj

def get_chroma() -> chroma:
    return chroma_obj

if __name__ == "__main__":
    init_chroma()