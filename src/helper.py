import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

#Extract text from pdf files
def load_pdf(data):
    documents = []
    for file in os.listdir(data):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data, file))
            documents.extend(loader.load())
    return documents


extracted_data = load_pdf("/Users/mac/Medical-ChatBot/data")

#Create text chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks

text_chunks = text_split(extracted_data)

#download embedding model
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

embeddings = download_hugging_face_embeddings()