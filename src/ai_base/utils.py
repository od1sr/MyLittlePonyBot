import sys

sys.path.append('./')

from chromadb.utils import embedding_functions
from chromadb import Client, api

import PyPDF2
from tqdm import tqdm


from typing import List, Optional

from src.debug import *

import os

class ConvertingConfig:
    PDF_FOLDER = "data" 
    CHROMA_COLLECTION = "nutrition_rag"
    CHUNK_SIZE = 1000
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_and_process_pdfs(folder_path: str) -> List[str]:
    """Загружает PDF-файлы и извлекает текст"""
    texts = []
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    if not pdf_files:
        raise FileNotFoundError(f"В папке {folder_path} не найдено PDF-файлов")
    
    DEBUG_founded_pdfs(len(pdf_files))

    DEBUG_start_pdf_loading()

    DEBUG_pdf_mathing()

    for filename in tqdm(pdf_files, desc="Обработка PDF"):
        try:
            with open(os.path.join(folder_path, filename), 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        texts.append(text)
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {str(e)}")

    return texts



def chunk_text(text: str, chunk_size: int = ConvertingConfig.CHUNK_SIZE) -> List[str]:
    """Разделяет текст на чанки"""
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]




def create_vector_db(texts: List[str]) -> Client:
    """Создает векторную базу данных"""
    client = Client()
    # Используем встроенную функцию для эмбеддингов
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=ConvertingConfig.EMBEDDING_MODEL
    )
    
    # Удаляем старую коллекцию, если существует
    if ConvertingConfig.CHROMA_COLLECTION in [col.name for col in client.list_collections()]:
        client.delete_collection(ConvertingConfig.CHROMA_COLLECTION)
    
    # Создаем новую коллекцию
    collection = client.create_collection(
        name=ConvertingConfig.CHROMA_COLLECTION,
        embedding_function=embedding_func
    )
    
    # Разбиваем тексты на чанки и добавляем в коллекцию
    all_chunks = []
    doc_ids = []
    metadata = []
    
    DEBUG_prepare_chunks()
    for i, text in enumerate(tqdm(texts, desc="Обработка текста")):
        chunks = chunk_text(text)
        all_chunks.extend(chunks)
        doc_ids.extend([f"doc_{i}_chunk_{j}" for j in range(len(chunks))])
        metadata.extend([{"source": f"doc_{i}"} for _ in chunks])
    
    # Добавляем пачками по 100 для больших коллекций
    batch_size = 100
    DEBUG_prepare_indexing(len(all_chunks))
    for i in tqdm(range(0, len(all_chunks), batch_size), desc="Индексация в ChromaDB"):
        batch_chunks = all_chunks[i:i + batch_size]
        batch_ids = doc_ids[i:i + batch_size]
        batch_metadata = metadata[i:i + batch_size]
        
        collection.add(
            documents=batch_chunks,
            ids=batch_ids,
            metadatas=batch_metadata
        )
    
    return collection


def rag_answer(question: str, collection: Client) -> Optional[str]:
    """Возвращает промт на вопрос с использованием RAG"""

    results = collection.query(
        query_texts=[question],
        n_results=3
    )


    context = "\n\n---\n\n".join([
        f"Источник: {meta['source']}\nТекст: {text}"
        for text, meta in zip(results['documents'][0], results['metadatas'][0])
    ])

    prompt = f"""Ты - эксперт по питанию и диетологии. Ответь на вопрос, используя только предоставленную информацию.
Если информации для ответа недостаточно, то можешь ее чутка додумать или скажи "В моих материалах нет точного ответа на этот вопрос".

Контекст:
{context}

Вопрос: {question}

Ответ должен быть четким, структурированным и если в контексте нет ответа на вопрос то можно немного пофантазировать).
Ответ:"""

    return prompt
    


