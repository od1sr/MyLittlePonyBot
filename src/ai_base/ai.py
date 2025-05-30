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
                                                    
                                                