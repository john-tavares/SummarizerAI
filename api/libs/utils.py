SUMMARIZE_PROMPT = """
Atue como uma Inteligência Artificial curiosa e fofoqueira e leia este texto extraído de um {content_type}:
{text}
Gere um resumo objetivo e de fácil compreensão desse aúdio de WhatsApp, no idioma {language}.
Sempre referencie qualquer individuo como pessoa ou individuo e a pessoa que falou como individuo.
"""

TOPICS_PROMPT = """
Com base nesse texto extraído de um conteúdo de {content_type}:
{text}
Quero um resumo em tópicos desse conteúdo, no idioma {language}.
"""

def generate_prompt(action:str, text:str, content_type:str, language:str="english")->str:
    if action == "summarize":
        base_prompt = SUMMARIZE_PROMPT
    elif action == "topics":
        base_prompt = TOPICS_PROMPT
    
    prompt = base_prompt.format(content_type=content_type, text=text, language=language)
    return prompt