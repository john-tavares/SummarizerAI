from flask import request, Blueprint
import api.extractors.audio as audio_extractor
import api.extractors.youtube as youtube_extractor
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

@api_bp.route('/youtube/summary', methods=['POST'])
def youtube_summarize():
    link = request.json['videoUrl']
    contact = request.json['contactId']
    
    try:
        video = youtube_extractor.get_video_info(link)
        summary = gpt.summarize_youtube(os.environ['OPENAI_APIKEY'], video)
        status = "success"
        blip.send_message(os.environ['BLIP_APIKEY'], status, contact, summary)
        return {"summary": summary,"status": status}
    
    except Exception as e:
        status = "false"
        blip.send_message(os.environ['BLIP_APIKEY'], status, contact, "")
        return {"summary": "","status": status}