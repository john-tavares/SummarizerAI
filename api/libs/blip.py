import requests
import os

HOST = "https://jonathantavares-all-a580a.http.msging.net"

def send_message(api_key:str,reciver_id:str, text:str):
    url = f"{HOST}/messages"
    payload = {  
        "id": "1234",
        "to": reciver_id,
        "type": "text/plain",
        "content": f"Prontinho! Aqui está um resumo para você:\n{text}"
    }
    response = requests.post(url, headers={"Authorization": api_key}, json=payload)
    return response