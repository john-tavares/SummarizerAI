from flask import request, Blueprint
import api.extractors.audio as audio_extractor
import api.libs.gpt as gpt
import api.libs.blip as blip
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/speechToText', methods=['POST'])
def speech_to_text():
    link = request.json['audioUrl']
    transcription = audio_extractor.process_audio(link)
    return {"transcription": transcription,"status": "success"}

@api_bp.route('/speechSummarize', methods=['POST'])
def speech_summarize():
    link = request.json['audioUrl']
    contact = request.json['contactId']
    print(f'Nova requisição de: {contact}')
    
    try:
        transcription = audio_extractor.process_audio(link)
        summary = gpt.summarize(os.environ['OPENAI_APIKEY'], "summarize", transcription, "Aúdio do WhatsApp")
        status = "success"
        blip.send_message(os.environ['BLIP_APIKEY'], status, contact, summary)
        return {"summary": summary,"status": status}
    
    except:
        status = "false"
        blip.send_message(os.environ['BLIP_APIKEY'], status, contact, "")
        return {"summary": "","status": status}