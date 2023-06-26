from flask import request, Blueprint
from api.extractors.audio import AudioExtractor
import api.extractors.youtube as youtube_extractor
import api.extractors.pdf as pdf_extractor
import api.extractors.page as page_extractor
import api.extractors.chat as chat_extractor
import libs.gpt as gpt
import libs.blip as blip
import os
import payments.views as payments
import libs.utils as utils

FREE_ACTIONS_LIMIT = 10

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
    profile = get_profile(receiver_id)

    if profile['payment_status'] == 'active' or profile['actions_counter'] <= FREE_ACTIONS_LIMIT:
        messages = blip.last_messages(os.environ['BLIP_APIKEY'], receiver_id)['resource']['items'][0:3]
        gpt_messages = chat_extractor.transcribe(messages)
        response = gpt.chat(os.environ['OPENAI_APIKEY'], gpt_messages)
        blip.create_event(os.environ['BLIP_APIKEY'], receiver_id, "chat")
    else:
        response = utils.MESSAGE_LIMIT_REACHED
    return {"response": response,"status": "success"}

@api_bp.route('/profile/<contact_id>', methods=['GET'])
def get_profile(contact_id):
    receiver_id = contact_id
    contact_info = blip.get_contact(os.environ['BLIP_APIKEY'], receiver_id)['resource']
    subscription_id = contact_info['extras'].get('stripeId')
    payments_status = payments.verify(subscription_id)['status']
    response = blip.get_event_counters(os.environ['BLIP_APIKEY'], receiver_id)
    return {'identity': receiver_id, 'actions_counter': response, 'payment_status': payments_status, 'contact': contact_info}