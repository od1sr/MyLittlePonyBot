from langchain.chains import RetrievalQA
from langchain_community.llms import ollama
from langchain_community.vectorstores import Chroma

def set_qa_chain(db):
    # 1. Инициализация языковой модели
    llm = ollama.Ollama(model="mistral")
    
    # 2. Создание QA цепочки
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True  # Опционально: возвращать исходные документы
    )
    return qa_chain

def get_answer(qa_chain, question: str) -> str:
    result = qa_chain({"query": question})
    return result["result"]