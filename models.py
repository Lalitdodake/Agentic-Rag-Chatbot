# from langchain_community.embeddings import OllamaEmbeddings

from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from langchain_ollama import ChatOllama


# OllamaEmbeddings Model Definition
embedding_model = OllamaEmbeddings(model='all-minilm:22m')
print("Embedding Model", embedding_model)


#  LLm model
llm_model = ChatOllama(model = "deepseek-r1:1.5b", temperature=0.3, streaming=True)

