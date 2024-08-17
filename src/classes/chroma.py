import os
from dotenv import load_dotenv
import chromadb
from langchain_community.document_loaders import TextLoader, Docx2txtLoader, UnstructuredCSVLoader, PyPDFLoader, SeleniumURLLoader
from langchain_community.document_loaders.image import UnstructuredImageLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL")

embeddings = OpenAIEmbeddings(model=embedding_model)
load_dotenv()

class chroma():
    def __init__(
        self,
        custom_name: str
    ):
        super().__init__
        self.project_name = custom_name
        self.vector_store = Chroma(
            collection_name=custom_name,
            embedding_function=embeddings,
        )
        self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})


    def upload_files(self) -> str:
        upload_folder = os.getenv("UPLOAD_FOLDER")
        all_docs = list()
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
            elif file_upload.endswith(".png"):
                loader = UnstructuredImageLoader(file_upload)
                docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200, add_start_index=True
            )
            splits = text_splitter.split_documents(docs)
            all_docs.extend(splits)
            self.add_vector_store(all_docs)
    
    def load_url(self, url: str):
        url_list = [url]
        loader = SeleniumURLLoader(urls = url_list)
        docs = loader.load()
        self.add_vector_store(docs)

    def add_vector_store(self, docs: list) -> None:
        self.vector_store.add_documents(documents=docs)

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