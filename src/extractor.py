from vosk import Model, KaldiRecognizer
import wave
import json
import soundfile as sf
import librosa

def extract_text_from_audio(audio_file_path, model_path="vosk-model-small-ru"):
    # Load the model
    model = Model(model_path)

    # Convert OGG to WAV format
    audio_data, sample_rate = librosa.load(audio_file_path)
    wav_path = audio_file_path.rsplit('.', 1)[0] + '.wav'
    sf.write(wav_path, audio_data, sample_rate)

    # Open the audio file
    wf = wave.open(wav_path, "rb")

    # Create recognizer
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # Process audio file
    text_result = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if 'text' in result:
                text_result.append(result['text'])

    # Get final result
    final = json.loads(rec.FinalResult())
    if 'text' in final:
        text_result.append(final['text'])

    # Close audio file
    wf.close()
    # Remove temporary WAV file
    import os
    os.remove(wav_path)
    os.remove(audio_file_path)
    
    
    # Return extracted text
    return ' '.join(text_result)

# Example usage:
# text = extract_text_from_audio("audio.wav")
# print(text)

print(extract_text_from_audio('audio_2025-05-31_12-14-26.ogg', 'vosk-model-small-ru-0.22'))