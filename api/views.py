from flask import request, Blueprint
import api.extractors.audio as audio_extractor

api_bp = Blueprint('api', __name__)

@api_bp.route('/speechToText', methods=['POST'])
def speech_to_text():
    link = request.json['audioUrl']
    transcription = audio_extractor.process_audio(link)
    return {"transcription": transcription,"status": "success"}