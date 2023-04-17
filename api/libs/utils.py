SUMMARIZE_PROMPT = """
Atue como uma Inteligência Artificial curiosa e fofoqueira e leia este texto extraído de um {content_type}:
{text}
Gere um resumo objetivo e de fácil compreensão desse aúdio de WhatsApp, no idioma {language}.
Sempre referencie qualquer individuo como pessoa ou individuo e a pessoa que falou como individuo.
"""

YOUTUBE_PROMPT = """
Resuma este vídeo do Youtube:

Title: {video_title}
Channel: {video_channel}
Legenda: {video_caption}
"""

def generate_prompt(action:str, text:str, content_type:str, language:str="english")->str:
    if action == "summarize":
        base_prompt = SUMMARIZE_PROMPT

    prompt = base_prompt.format(content_type=content_type, text=text, language=language)
    return prompt

def generate_youtube_prompt(video:dict)->str:
    prompt = YOUTUBE_PROMPT.format(video_title=video['title'], video_channel=video['channel'], video_caption=video['captions'])
    return prompt