from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


from typing import Any


def loadPDF(file_path: str):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return pages


def split_for_chanks(chunk_size: int, chunk_overlap: int, pages):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(pages)
    return chunks


PDF = loadPDF("data\eatwell_guide_annex_1.pdf")
PDF_CHUNKS = split_for_chanks(chunk_size=500, chunk_overlap=100, pages=PDF)


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma.from_documents(PDF_CHUNKS, embeddings, persist_directory="db")