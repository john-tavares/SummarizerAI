import libs.utils as utils

def convert_message(message:dict):
    if message['type'] == "text/plain":
        return message['content']
    elif message['text'] == "Instagram Story Mention":
        return '<Evento: Mencionou você em um stories>'
    elif message['text'] == "Instagram Story Reply":
        return '<Evento: Respondeu seu próprio stories>'
    else:
        return f"<Conteúdo {message['content'].get('type', 'weblink')}>"

def transcribe(messages:list):
    messages.reverse()
    prompt_message = {"role": "system", "content": utils.PROMPT_CHAT}
    gpt_messages = [prompt_message]
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