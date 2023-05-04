from flask import request, Blueprint
import api.extractors.audio as audio_extractor
import api.extractors.youtube as youtube_extractor
import api.extractors.pdf as pdf_extractor
import api.extractors.page as page_extractor
import api.extractors.chat as chat_extractor
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

@api_bp.route('/page/summary', methods=['POST'])
def page_summarize():
    link = request.json['pageUrl']
    contact = request.json['contactId']
    
    try:
        messages = page_extractor.process(link)
        summary = gpt.summarize_pdf(os.environ['OPENAI_APIKEY'], messages)
        status = "success"
        blip.send_message(os.environ['BLIP_APIKEY'], status, contact, summary)
        return {"summary": summary,"status": status}
    
    except Exception as e:
        status = "false"
        blip.send_message(os.environ['BLIP_APIKEY'], status, contact, "")
        return {"summary": "","status": status}
    
@api_bp.route('/chat/continue', methods=['POST'])
def chat_continue():
    receiver_id = request.json['contactId']
    messages = blip.last_messages("Key c29waGlhdGVzdGVzOk9WMGloSkFmWExuUHloblk3Tkc4", receiver_id)['resource']['items'][0:10]
    gpt_messages = chat_extractor.transcribe(messages)
    response = gpt.chat(os.environ['OPENAI_APIKEY'], gpt_messages)
    return {"response": response,"status": "success"}