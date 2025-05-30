from vosk import Model, KaldiRecognizer
import wave
import os

# Путь к модели
model_path = r"data\voice_messages\vosk-model-small-ru-0.22"

# Проверка существования папки
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Папка модели не найдена: {model_path}")

# Загрузка модели
model = Model(model_path)
if not model:
    raise ValueError("Не удалось загрузить модель. Проверьте содержимое папки.")

# Конвертация аудио
input_audio = r"data\voices\voice_30-05-2025_15-27-27.ogg"
os.system(f"ffmpeg -i \"{input_audio}\" -ar 16000 -ac 1 voice_message.wav")

# Распознавание
with wave.open("voice_message.wav", "rb") as wf:
    rec = KaldiRecognizer(model, wf.getframerate())
    
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())

    # Получение финального результата
    print(rec.FinalResult())