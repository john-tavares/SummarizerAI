from pydub import AudioSegment
import speech_recognition as sr
import requests
import tempfile
import os
from api.models.extractor import Extractor

class AudioExtractor(Extractor):
    def download(self):
        response = requests.get(self.url)
        
        with tempfile.NamedTemporaryFile(delete=False) as audio_file:
            audio_file.write(response.content)
            audio_file.flush()
            return audio_file.name

    def __convert_audio_format(self, audio_file_path):
        with tempfile.NamedTemporaryFile(suffix=f".wav", delete=False) as wav_file:
            AudioSegment.from_file(audio_file_path).export(wav_file.name, format="wav")
            wav_file.flush()
            return wav_file.name

    def transcribe(self):
        audio_file_path = self.download()
        wav_file_path = self.__convert_audio_format(audio_file_path)
        
        r = sr.Recognizer()
        
        with sr.AudioFile(wav_file_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio_data=audio, language=self.language)
        
        os.remove(audio_file_path)
        os.remove(wav_file_path)
        
        return text