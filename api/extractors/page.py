from bs4 import BeautifulSoup
import requests
import api.libs.utils as utils

def transcribe(url:str)->list:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.text
    body = soup.body.text
    
    prompt = {"role": "user", "content": "Leia o texto a página da Web e dê um resumo objetivo."}
    complement = {"role": "user", "content": f"Titulo da Página: {title}"}
    words = body.split()    
    text = ""

    for word in words:
        text += word + " "
        message = {"role": "user", "content": text}
        messages = [prompt, complement, message]
        tokens = utils.num_tokens_from_messages(messages)
        
        if tokens > 4096:
            messages.pop()
            break

    return messages

def process(link):
    messages = transcribe(link)
    return messages