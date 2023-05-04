import api.libs.utils as utils

def transcribe(messages:list):
    messages.reverse()
    prompt_message = {"role": "system", "content": utils.PROMPT_CHAT}
    gpt_messages = [prompt_message]
    for message in messages:
        if message['direction'] == "sent":
            role = "assistant"
        else:
            role = "user"
        gpt_message = {"role": role, "content": message['content']}
        gpt_messages.append(gpt_message)
        tokens = utils.num_tokens_from_messages(gpt_messages)
        if tokens > 4096:
            gpt_messages.pop()
            break
    return gpt_messages