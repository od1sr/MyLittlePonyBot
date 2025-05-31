import sys

# Добавляем текущую директорию в путь для импорта
sys.path.append('./')

# Импорт необходимых библиотек для работы с ChromaDB
from chromadb.utils import embedding_functions
from chromadb import Client, api, db, PersistentClient
from chromadb.config import Settings
import json

# Библиотеки для работы с PDF и прогресс-баром
import PyPDF2
from tqdm import tqdm

# Типизация для Python
from typing import List, Optional

# Импорт функций отладки
from src.debug import *

import os

# Конфигурация для конвертации и хранения данных
class ConvertingConfig:
    PDF_FOLDER = "data"  # Папка с PDF файлами
    CHROMA_COLLECTION = "nutrition_rag"  # Название коллекции в ChromaDB
    CHUNK_SIZE = 1000  # Размер чанка для разбиения текста
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Модель для создания эмбеддингов
    CHROMA_DB_PATH = "db/sessions"  # Путь к базе данных ChromaDB



def load_and_process_pdfs(folder_path: str) -> List[str]:
    """Загружает PDF-файлы и извлекает текст"""
    texts = []
    # Получаем список всех PDF файлов в указанной папке
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    if not pdf_files:
        raise FileNotFoundError(f"В папке {folder_path} не найдено PDF-файлов")
    
    DEBUG_founded_pdfs(len(pdf_files))

    DEBUG_start_pdf_loading()

    DEBUG_pdf_mathing()

    # Обрабатываем каждый PDF файл
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
    """Разделяет текст на чанки указанного размера"""
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]



def is_db_created(path: str = "./") -> bool:
    """Проверяет, создана ли база данных по указанному пути"""
    return os.path.exists(path)



def get_db_collection() -> api.Collection:
    """Возвращает существующую коллекцию из базы данных"""
    DEBUG_connect_to_data_base(ConvertingConfig.CHROMA_DB_PATH)
    client = PersistentClient(path=ConvertingConfig.CHROMA_DB_PATH)
    DEBUG_connect_succes()
    return client.get_collection(
        name=ConvertingConfig.CHROMA_COLLECTION,
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name = ConvertingConfig.EMBEDDING_MODEL
        )
    )



def create_vector_db(texts: List[str]) -> Client:
    """Создает векторную базу данных из списка текстов"""
    # Инициализируем клиент ChromaDB
    client = PersistentClient(path=ConvertingConfig.CHROMA_DB_PATH)
    # Настраиваем функцию для создания эмбеддингов
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=ConvertingConfig.EMBEDDING_MODEL
    )
    
    # Проверяем существование коллекции
    existing_collections = [col.name for col in client.list_collections()]
    if ConvertingConfig.CHROMA_COLLECTION in existing_collections:
        collection = client.get_collection(
            name=ConvertingConfig.CHROMA_COLLECTION,
            embedding_function=embedding_func
        )
        return collection
    
    # Создаем новую коллекцию если не существует
    collection = client.create_collection(
        name=ConvertingConfig.CHROMA_COLLECTION,
        embedding_function=embedding_func
    )
    
    # Подготовка данных для добавления в коллекцию
    all_chunks = []
    doc_ids = []
    metadata = []
    
    DEBUG_prepare_chunks()
    # Разбиваем каждый текст на чанки
    for i, text in enumerate(tqdm(texts, desc="Обработка текста")):
        chunks = chunk_text(text)
        all_chunks.extend(chunks)
        doc_ids.extend([f"doc_{i}_chunk_{j}" for j in range(len(chunks))])
        metadata.extend([{"source": f"doc_{i}"} for _ in chunks])
    
    # Добавляем данные в коллекцию батчами
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

    # Обработка JSON файлов
    json_path = "data/jsons"
    if os.path.exists(json_path):
        json_files = [f for f in os.listdir(json_path) if f.endswith('.json')]
        
        for json_file in tqdm(json_files, desc="Обработка JSON файлов"):
            with open(os.path.join(json_path, json_file), 'r', encoding='utf-8') as f:
                try:
                    # Загружаем JSON данные
                    json_data = json.load(f)
                    
                    # Преобразуем JSON в текст
                    text_content = json.dumps(json_data, ensure_ascii=False, indent=2)
                    
                    # Разбиваем на чанки
                    chunks = chunk_text(text_content)
                    
                    # Генерируем идентификаторы и метаданные
                    chunk_ids = [f"json_{json_file}_chunk_{j}" for j in range(len(chunks))]
                    chunk_metadata = [{"source": f"json_{json_file}"} for _ in chunks]
                    
                    # Добавляем данные батчами
                    for i in range(0, len(chunks), batch_size):
                        batch_chunks = chunks[i:i + batch_size]
                        batch_ids = chunk_ids[i:i + batch_size]
                        batch_metadata = chunk_metadata[i:i + batch_size]
                        
                        collection.add(
                            documents=batch_chunks,
                            ids=batch_ids,
                            metadatas=batch_metadata
                        )
                except json.JSONDecodeError:
                    print(f"Ошибка при обработке файла {json_file}")
    
    
    return collection



def rag_answer(question: str, collection: Client) -> Optional[str]:
    """Возвращает промт на вопрос с использованием RAG (Retrieval-Augmented Generation)"""

    # Получаем наиболее релевантные документы для вопроса
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    # Формируем контекст из найденных документов
    context = "\n\n---\n\n".join([
        f"Источник: {meta['source']}\nТекст: {text}"
        for text, meta in zip(results['documents'][0], results['metadatas'][0])
    ])

    # Создаем промт для модели
    prompt = f"""Ты - эксперт по питанию и диетологии

Контекст:
{context}

Вопрос: {question}

Ответ должен быть четким, структурированным и если в контексте нет ответа на вопрос то можно немного пофантазировать).
Ответ:"""

    return prompt



def init_db():
    """Инициализирует базу данных: создает новую или возвращает существующую"""
    if not is_db_created(ConvertingConfig.CHROMA_DB_PATH):
        text = load_and_process_pdfs(ConvertingConfig.PDF_FOLDER)
        client = create_vector_db(text)
    else:
        client = get_db_collection()

    return client