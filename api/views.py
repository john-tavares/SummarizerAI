from flask import request, Blueprint
from api.extractors.audio import AudioExtractor
import api.extractors.youtube as youtube_extractor
import api.extractors.pdf as pdf_extractor
import api.libs.gpt as gpt
import api.libs.blip as blip
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/transcribe', methods=['POST'])
def transcribe():
    url = request.json['fileUrl']
    file_type = request.json['fileType']
    
    if 'audio' in file_type:
        file = AudioExtractor(url, file_type)

    transcription = file.transcribe()
    return {"transcription": transcription,"status": "success"}

@api_bp.route('/summary', methods=['POST'])
def speech_summarize():
    url = request.json['fileUrl']
    file_type = request.json['fileType']
    contact = request.json['contactId']
    
    try:
        if 'audio' in file_type:
            file = AudioExtractor(url, file_type)
        
        transcription = file.transcribe()
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

@api_bp.route('/pdf/summary', methods=['POST'])
def pdf_summarize():
    link = request.json['pdfUrl']
    contact = request.json['contactId']
    
    try:
        messages = pdf_extractor.process(link)
        summary = gpt.summarize_pdf(os.environ['OPENAI_APIKEY'], messages)
        status = "success"
        blip.send_message(os.environ['BLIP_APIKEY'], status, contact, summary)
        return {"summary": summary,"status": status}
    
    except Exception as e:
        status = "false"
        blip.send_message(os.environ['BLIP_APIKEY'], status, contact, "")
        return {"summary": "","status": status}