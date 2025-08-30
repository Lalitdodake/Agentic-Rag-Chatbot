from langchain_community.vectorstores import Chroma
import os
from models import embedding_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter



class VectorDBHandler:
    def __init__(self, persist_directory="./vector_store"):
        self.persist_directory = persist_directory
        self.embedding = embedding_model
        self.vectorstore = None

        # Create directory if missing
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)

        # Load existing DB if present
        if os.listdir(self.persist_directory):  # Check if it already has data
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding
            )
            print(" Loaded existing Chroma vector store.")
        else:
            print(" No existing vector DB found. A new one will be created.")

    def ingest_documents(self, docs_dir="./docs"):
        docs = []
        for file in os.listdir(docs_dir):
            if file.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(docs_dir, file))
                docs.extend(loader.load())

        if not docs:
            print(" No documents found to ingest!")
            return

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        split_docs = splitter.split_documents(docs)

        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                split_docs,
                self.embedding,
                persist_directory=self.persist_directory
            )
        else:
            self.vectorstore.add_documents(split_docs)

        self.vectorstore.persist()
        print(f" Ingested {len(split_docs)} chunks into ChromaDB.")

    def ingest_uploaded_file(self, file_path):
        "Ingest a single uploaded PDF dynamically"
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        split_docs = splitter.split_documents(docs)

        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                split_docs,
                self.embedding,
                persist_directory=self.persist_directory
            )
        else:
            self.vectorstore.add_documents(split_docs)

        self.vectorstore.persist()
        print(f" Uploaded and ingested {len(split_docs)} new chunks.")

    def get_retriever(self):
        "Return retriever for querying the vector store"
        if self.vectorstore is None:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding
            )
        return self.vectorstore.as_retriever(search_type="mmr",search_kwargs={"k": 3})



