from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from .core import loadPDF, split_for_chanks

def get_all_pdf_files(path: str) -> list[str]:
    import os
    files = []
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            files.append(file)
    return files

def create_vector_db(data_base_path: str, db_path: str):
    files = get_all_pdf_files(data_base_path)
    for file in files:
        text = loadPDF(data_base_path + file)
        chunks = split_for_chanks(1000, 200, text)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        db = Chroma.from_texts(chunks, embeddings, persist_directory=db_path)
        db.persist()
    return db, embeddings