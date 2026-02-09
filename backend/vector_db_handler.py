from langchain_chroma import Chroma
import os
from models import embedding_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
import datetime

def get_file_name(file_path):
    return os.path.basename(file_path)


class VectorDBHandler:
    def __init__(self, persist_directory="./chroma_vector_store"):
        print("Loading Vector DB---------------------------------------")
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
        for doc in docs:
            doc.metadata["file_name"] = file_path
            doc.metadata['ingested_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        semantic_chunker = SemanticChunker(self.embedding, breakpoint_threshold_type="percentile")
        semantic_chunks = semantic_chunker.create_documents([d.page_content for d in docs])
        for semantic_chunk in semantic_chunks:
            print(semantic_chunk.page_content)
            print(len(semantic_chunk.page_content))



        try:

            if self.vectorstore is None:
                print("CREATING A NEW VECTOR DB AND INSERTING DOCUMENT")
                self.vectorstore = Chroma.from_documents(
                    semantic_chunks,
                    self.embedding,
                    persist_directory=self.persist_directory
                )
            else:
                print("INSERTING DOCUMENT IN EXISTING VECTOR DB")
                self.vectorstore.add_documents(semantic_chunks)


            print(f" Uploaded and ingested {len(semantic_chunks)} new chunks.")
        except Exception as e:
            print(e)
            # if document is not embedded into the vectorstore: then delete the pdf
            os.remove(file_path)




    def get_retriever(self):
        """Return retriever for querying the vector store"""
        # .as_retriever(search_type="mmr", search_kwargs={"k": 3})
        if self.vectorstore is None:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding
            )
        return self.vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 1, "fetch_k": 5})



