# from langchain_community.vectorstores import Chroma

from langchain_chroma import Chroma
import os
from models import embedding_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_file_name(file_path):
    return os.path.basename(file_path)


class VectorDBHandler:
    def __init__(self, persist_directory="./chroma_vector_store"):
        self.persist_directory = persist_directory
        self.embedding = embedding_model
        self.vectorstore = None

        # Create directory if missing
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)

        # Load existing DB if present
        if os.listdir(self.persist_directory):  # Check if it already has data
            self.vectorstore = Chroma(
                collection_name="development",
                persist_directory=self.persist_directory,
                embedding_function=self.embedding
            )
            print("Loaded existing Chroma vector store.")
        else:
            print("No existing vector DB found. A new one will be created.")


    def ingest_uploaded_file(self, file_path):
        """Ingest a single uploaded PDF dynamically"""
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = splitter.split_documents(docs)
        # print("split docs", split_docs)
        file_name = get_file_name(file_path)
        print("file name", file_name)
        if self.vectorstore is None:
            print("CREATING A NEW VECTOR DB AND INSERTING DOCUMENT")
            self.vectorstore = Chroma.from_documents(
                split_docs,
                self.embedding,
                persist_directory=self.persist_directory
            )
        else:
            print("INSERTING DOCUMENT IN EXISTING VECTOR DB")
            self.vectorstore.add_documents(split_docs)

        print(f" Uploaded and ingested {len(split_docs)} new chunks.")

    def get_retriever(self):
        """Return retriever for querying the vector store"""
        # .as_retriever(search_type="mmr", search_kwargs={"k": 3})
        if self.vectorstore is None:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding
            )
        return self.vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 1, "fetch_k": 5})



