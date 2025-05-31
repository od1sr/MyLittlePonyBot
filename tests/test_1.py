import sys

sys.path.append('./')

from src.ai_base.utils import *
from src.ai_base.ai import *
from src.ai_base.cutting import *


# todo подключение к db
if not is_db_created('C:\\Users\\WhoIsWho\\Desktop\\MyLittlePonyBot\\'):
    text = load_and_process_pdfs(ConvertingConfig.PDF_FOLDER)
    client = create_vector_db(text)
else:
    client = get_db_collection()


# пример
promt = rag_answer("что такое нутриенты", client)
print(request_with_gemini(promt, API_KEY, PROXY))


data = generate_ration_for_week(55, 170, 18, "Мужчина", "средняя активность", "Цель: закадрить девушку", "Без глютена")

print(data)



print(generate_retion_for_day("Понедельник", 55, 170, 18, "Мужчина", "средняя активность", "Цель: закадрить девушку", "Без глютена"))