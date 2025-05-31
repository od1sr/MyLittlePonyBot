import sys

sys.path.append('./')

from utils import *
from src.ai_base.ai import *

if not is_db_created('C:\\Users\\WhoIsWho\\Desktop\\MyLittlePonyBot\\'):
    text = load_and_process_pdfs(ConvertingConfig.PDF_FOLDER)
    client = create_vector_db(text)
else:
    client = get_db_collection()


while True:
    q = input("Press enter: ")
    promt = rag_answer(q, client)
    print(request_with_gemini(promt, API_KEY, PROXY))
