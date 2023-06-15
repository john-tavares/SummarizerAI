import requests
import os

HOST = "https://jonathantavares-all-a580a.http.msging.net"
CONTENT_SUCCESS = "Prontinho! Aqui está um resumo para você:\n{text}"
CONTENT_ERRO = "Tivemos um problema!\n\nInfelizmente não consegui processar esse conteúdo."

def send_message(api_key:str, action:str, reciver_id:str, text:str):
    url = f"{HOST}/messages"
    if action == "success":
        message = CONTENT_SUCCESS.format(text=text)
    else:
        message = CONTENT_ERRO

    payload = {  
        "id": "1234",
        "to": reciver_id,
        "type": "text/plain",
        "content": message
    }
    response = requests.post(url, headers={"Authorization": api_key}, json=payload)
    return response

def transform_identifier_in_reciver_id(identifier, source):
    if source == 'Instagram':
        complement = 'instagram.gw.msging.net'
    elif source == 'Telegram':
        complement = 'telegram.gw.msging.net'
    
    return f'{identifier}@{complement}'

def send_raw_message(api_key:str, reciver_id:str, message:str):
    url = f"{HOST}/messages"
    
    payload = {  
        "id": "1234",
        "to": reciver_id,
        "type": "text/plain",
        "content": message
    }
    response = requests.post(url, headers={"Authorization": api_key}, json=payload)
    return response

def get_contact(api_key:str, identity: str):

    url = 'https://http.msging.net/commands'

    body = {
        'id': '1',
        'method': 'get',
        'uri': f'/contacts/{identity}'
    }

    response = requests.post(url, headers={"Authorization": api_key}, json=body).json()
    return response

def update_contact(api_key:str, identity:str, stripe_id:str):
    '''
        This function update a contact information
    '''
    url = 'https://http.msging.net/commands'

    body = {
        'id': '1',
        'method': 'set',
        'uri': '/contacts',
        'type': 'application/vnd.lime.contact+json',
        'resource': ''
    }
    resource = get_contact(api_key, identity)['resource']
    
    if not resource.get('extras'):
        resource['extras'] = {}
    
    resource['extras']['stripeId'] = stripe_id
    body['resource'] = resource
    
    response = requests.post(url, headers={"Authorization": api_key}, json=body).json()
    return response

def last_messages(api_key:str, reciver_id:str):
    url = f"{HOST}/commands"

    payload = {  
        "id": "1234",
        "method": "get",
        "uri": f"/threads/{reciver_id}?refreshExpiredMedia=true"
    }
    response = requests.post(url, headers={"Authorization": api_key}, json=payload).json()
    return response