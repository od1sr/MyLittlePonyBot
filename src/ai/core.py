from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



from typing import Any


def loadPDF(file_path: str) -> str:
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    text = ""
    for page in pages:
        text += page.page_content
    return text


def split_for_chanks(chunk_size: int, chunk_overlap: int, text: str) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                   chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks
