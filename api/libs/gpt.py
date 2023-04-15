import openai
import api.libs.utils as utils

def summarize(api_key:str, action:str, text:str, content_type:str, language:str="pt-BR"):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=utils.generate_prompt(action, text, content_type, language),
        temperature=0.1,
        max_tokens=2048,
        n=1,
        stop=None
    )

    return response["choices"][0]["text"]