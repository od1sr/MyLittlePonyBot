from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from .core import loadPDF, split_for_chanks
from ..debug import *

from time import time

def get_all_pdf_files(path: str) -> list[str]:
    import os
    files = []
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            files.append(file)
    return files

def create_vector_db(data_base_path: str, db_path: str):
    files = get_all_pdf_files(data_base_path)
    start_vectorize()
    for file in files:
        vectorize_file(file)
        _st = time()
        text = loadPDF(data_base_path + file)
        chunks = split_for_chanks(1000, 200, text)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        db = Chroma.from_texts(chunks, embeddings, persist_directory=db_path)
        db.persist()
        _et = time()
        vectorize_finish(_et - _st)
    return db

def get_db(db_path: str):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    return db