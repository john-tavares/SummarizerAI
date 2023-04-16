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