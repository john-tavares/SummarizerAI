import PyPDF2
import requests
import tempfile
import os
import api.libs.utils as utils

def download(link):
    response = requests.get(link)
    with tempfile.NamedTemporaryFile(delete=False) as pdf_file:
        pdf_file.write(response.content)
        pdf_file.flush()
        return pdf_file.name

def transcribe(filename:str)->list:
    messages = [{"role": "user", "content": "Analise o texto a seguir extraido de um PDF e dê um resumo objetivo."}]
    
    with open(filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        
        for i in range(num_pages):
            page = reader.pages[i]
            message = {"role": "user", "content": f"Página {i+1}\n\n"+page.extract_text()} 
            
            messages.append(message)
            tokens = utils.num_tokens_from_messages(messages)
            
            if tokens > 4096:
                messages.pop()
                break

    return messages

def process(link):
    pdf_file_path = download(link)
    messages = transcribe(pdf_file_path)
    os.remove(pdf_file_path)
    return messages