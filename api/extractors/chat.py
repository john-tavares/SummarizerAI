import libs.utils as utils

def convert_message(message:dict):
    if message['type'] == "text/plain":
        return message['content']
    elif message['text'] == "Instagram Story Mention":
        return '<Evento: Mencionou você em um stories do Instagram>'
    elif message['text'] == "Instagram Story Reply":
        return '<Evento: Respondeu o seu stories do Instagram>'
    else:
        return f"<Conteúdo {message['content'].get('type', 'weblink')}>"

def convert_contact_info_in_message(contact):
    return {"role": 'system', "content": f'Nome do Usuário: {contact.get("name", "Usuário")}'}

def transcribe(messages:list, contact_info):
    messages.reverse()
    prompt_message = {"role": "system", "content": utils.PROMPT_CHAT}
    gpt_messages = [prompt_message, convert_contact_info_in_message(contact_info)]
    for message in messages:
        if message['direction'] == "sent":
            role = "assistant"
        else:
            role = "user"
        content = convert_message(message)
        gpt_message = {"role": role, "content": content}
        gpt_messages.append(gpt_message)
        tokens = utils.num_tokens_from_messages(gpt_messages)
        if tokens > 4096:
            gpt_messages.pop()
            break
    return gpt_messages