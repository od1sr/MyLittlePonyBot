import requests
import json
import os
import dotenv

dotenv.load_dotenv()

PROXY = {
    'http': f'http://{os.getenv("PROXY_LOGIN")}@{os.getenv("PROXY_HOST")}:{os.getenv("PROXY_PORT_HTTP")}',
    'https': f'http://{os.getenv("PROXY_LOGIN")}@{os.getenv("PROXY_HOST")}:{os.getenv("PROXY_PORT_HTTPS")}',
}

API_KEY = os.getenv("GEMINI_API_KEY")

RESTERICTIONS = {
    1: "без лактозы", 2: "без глютена", 3: "вегетарианское"
}



def request_with_gemini(prompt: str, api_key: str, proxies: dict = None) -> str:
    """Отправляет запрос к Gemini API с обработкой ошибок"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            proxies=proxies,
            timeout=30
        )
        response.raise_for_status()

        response_data = response.json()
        if "candidates" in response_data and response_data["candidates"]:
            return response_data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        ...
                                                    
def generate_ration_for_week(mass: float, height: float, age: int, gender: str, activity: str, purpose: str, resteriction = None )-> str:
    """Генерирует рацион для человека"""
    prompt = f"""
    Составьте рацион на неделю для человека с такими параметрами (ограничения {resteriction}):
    Масса тела: {mass} кг
    Рост: {height} см
    Возраст: {age} лет
    Пол: {gender}
    Уровень активности: {activity}
    Цель: {purpose}

    отправь ответ в формате в формате:
    Завтрак:
    Обед:
    Ужин:
    Перекус:
    После тренировки:
    После сна:

    в начале пиши день недели
    для каждого продукта пропиши калорийность и БЖУ
    разделяй дни используя символ '-'

    ===
    тут выведи дополнительные рекомендации

    не пиши ничего лишнего не добавляй никаких лишних символов
    """
    return request_with_gemini(prompt, API_KEY, PROXY)


def get_data_for_ration_with_week(string: str):
    """Извлекает данные из строки"""
    data = {}
    parts = string.split("===")
    days = parts[0].strip().split("-")
    recommendations = parts[1].strip() if len(parts) > 1 else ""
    
    for day in days:
        day_lines = day.strip().split("\n")
        day_name = day_lines[0].strip()
        data[day_name] = {}
        
        for meal in day_lines[1:]:
            meal = meal.strip()
            if not meal:
                continue
                
            for meal_type in ["Завтрак", "Обед", "Ужин", "Перекус", "После тренировки", "После сна"]:
                if meal.startswith(meal_type):
                    try:
                        data[day_name][meal_type] = meal.split(": ", 1)[1].strip()
                    except IndexError:
                        data[day_name][meal_type] = ""
                        
    if recommendations:
        data["recommendations"] = recommendations
        
    return data


def generate_retion_for_day(day: str, mass: float, height: float, age: int, gender: str, activity: str, purpose: str, resteriction = None)-> str:
    """Генерирует рацион для человека"""
    prompt = f"""
    Составьте рацион на день для человека с такими параметрами (ограничения {resteriction}):
    День недели: {day}
    Масса тела: {mass} кг
    Рост: {height} см
    Возраст: {age} лет
    Пол: {gender}
    Уровень активности: {activity}
    Цель: {purpose}

    отправь ответ в формате в формате:
    Завтрак: название продукта(калорийность,БЖУ)
    Обед: ...
    Ужин: ..
    Перекус: ...
    После тренировки: ...
    После сна: ...

    для каждого продукта пропиши калорийность и БЖУ

    ===

    тут выведи дополнительные рекомендации


    не пиши ничего лишнего не добавляй никаких лишних символов
    только по делу

"""
    return request_with_gemini(prompt, API_KEY, PROXY)

def get_data_for_ration_with_one_day(string: str):
    """Извлекает данные из строки"""
    data = {}
    parts = string.split("===")
    days = parts[0].strip().split("-")
    recommendations = parts[1].strip() if len(parts) > 1 else "" 
    day = days[0].strip()
    data[day] = {}
    for meal in days[1:]:
        meal = meal.strip()
        if not meal:
            continue

        for meal_type in ["Завтрак", "Обед", "Ужин", "Перекус", "После тренировки", "После сна"]:
            if meal.startswith(meal_type):
                try:
                    data[day][meal_type] = meal.split(": ", 1)[1].strip()
                except IndexError:
                    data[day][meal_type] = ""
                    
    if recommendations:
        data["recommendations"] = recommendations

    return data