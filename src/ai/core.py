from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma



def loadPDF(file_path: str):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return pages


def split_for_chanks(chunk_size: int, chunk_overlap: int, pages):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(pages)
    return chunks

