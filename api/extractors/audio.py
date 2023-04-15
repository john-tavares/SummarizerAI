from pydub import AudioSegment
import speech_recognition as sr
import requests
import tempfile
import os

def download_audio(link):
    response = requests.get(link)
    with tempfile.NamedTemporaryFile(delete=False) as opus_file:
        opus_file.write(response.content)
        opus_file.flush()
        return opus_file.name

def convert_audio_format(audio_file_path):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav_file:
        AudioSegment.from_file(audio_file_path).export(wav_file.name, format="wav")
        wav_file.flush()
        return wav_file.name

def transcribe_audio(audio_file_path, language="pt-BR"):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = r.record(source)
        text = r.recognize_google(audio_data=audio, language=language)
        return text

def process_audio(link, language="pt-BR"):
    opus_file_path = download_audio(link)
    wav_file_path = convert_audio_format(opus_file_path)
    text = transcribe_audio(wav_file_path, language)
    os.remove(opus_file_path)
    os.remove(wav_file_path)
    return text