import sys

sys.path.append('./')

from utils import *
from src.ai_base.ai import *

text = load_and_process_pdfs(ConvertingConfig.PDF_FOLDER)

client = create_vector_db(text)

while True:
    question = input("Enter question: ")
    if question == "exit":
        break
    prompt = rag_answer(question, client)

    print(request_with_gemini(prompt, API_KEY, PROXY))
