from langchain_community.chains import PebbloRetrievalQA
from langchain_community.llms import ollama
from langchain_community.vectorstores import Chroma

def set_qa_chain(db_path: str, embeding_function):
    db = Chroma(persist_directory=db_path, embedding_function=embeding_function)
    llm = ollama.Ollama(model="mistral")
    qa_chain = PebbloRetrievalQA(llm=llm, retriever=db.as_retriever())
    return qa_chain

def get_answer(qa_chain, question: str) -> str:
    result = qa_chain({"query": question})
    return result["result"]